from sqlalchemy import distinct, extract, func
from instance.database import db
from models.order import Order, OrderItem
from models.product import Product
from models.user import User, UserRole, VendorProfile, VendorStatus
from shared.time import now



def vendor_register_repo(user, vendor_data_validated):
    vendor_profile = VendorProfile(
        user_id=user.id,
        business_name=vendor_data_validated.business_name,
        business_description=vendor_data_validated.business_description,
        business_address=vendor_data_validated.business_address,
        business_phone=vendor_data_validated.business_phone,
        business_email=vendor_data_validated.business_email,
        business_logo_url=vendor_data_validated.business_logo_url,
        vendor_status=VendorStatus.PENDING.value,
    )

    vendor_role = db.one_or_404(
        db.select(UserRole).filter_by(name="vendor"),
        description="No role with id 'vendor'.",
    )

    user.role.append(vendor_role)

    db.session.add(vendor_profile)
    db.session.commit()


def vendor_profile_by_user_id_repo(user_id):
    return db.one_or_404(
        db.select(VendorProfile).filter_by(user_id=user_id),
        description=f"No vendor with id '{user_id}'.",
    )


def get_vendors_repo():
    pending_vendors = db.paginate(
        db.select(VendorProfile).filter_by(vendor_status=VendorStatus.PENDING.value)
    )

    approved_vendors = db.paginate(
        db.select(VendorProfile).filter_by(vendor_status=VendorStatus.APPROVED.value)
    )

    rejected_vendors = db.paginate(
        db.select(VendorProfile).filter_by(vendor_status=VendorStatus.REJECTED.value)
    )

    return (pending_vendors, approved_vendors, rejected_vendors)


def process_vendor_application_repo(vendor_profile, review_request_validated):
    action = review_request_validated.action

    if action == "approve":
        vendor_profile.vendor_status = VendorStatus.APPROVED.value

    elif action == "reject":
        vendor_profile.vendor_status = VendorStatus.REJECTED.value

    db.session.commit()


def update_vendor_profile_repo(vendor_profile, vendor_data_validated):

    for field, value in vendor_data_validated.model_dump().items():
        # only update the field if it is not None
        if value is not None:
            setattr(vendor_profile, field, value)

    db.session.commit()

    return vendor_profile


# ----------------------------------------------------------- Stats -----------------------------------------------------------


def get_vendor_stats_repo(user_id_):
    now_ = now()
    current_year = now_.year

    # total orders = sum of order items
    # total sales = sum of order items * quantity
    # total revenue = sum of total price
    # total customers = count of distinct users in order

    all_time_stats = (
        db.session.query(
            func.sum(OrderItem.total_price).label("total_revenue"),
            func.sum(OrderItem.quantity).label("total_sales"),
            func.count(OrderItem.id).label("total_orders"),
            func.count(distinct(Order.user_id)).label("total_customers"),
        )
        .join(Order, OrderItem.order_id == Order.id)
        .filter(OrderItem.vendor_id == user_id_)
        .first()
    )

    monthly_revenue = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.sum(OrderItem.total_price).label('total_revenue'),
    ).join(
        OrderItem, Order.id == OrderItem.order_id
    ).filter(
        OrderItem.vendor_id == user_id_,
        extract('year', Order.created_at) == current_year,
    ).group_by(
        extract('month', Order.created_at)
    ).order_by(
        extract('month', Order.created_at)
    ).all()

    monthly_orders = db.session.query(
        extract('month', Order.created_at).label('month'),
        func.count(Order.id).label('total_orders'),
    ).join(
        OrderItem, Order.id == OrderItem.order_id
    ).filter(
        OrderItem.vendor_id == user_id_,
        extract('year', Order.created_at) == current_year,
    ).group_by(
        extract('month', Order.created_at)
    ).order_by(
        extract('month', Order.created_at)
    ).all()

    return {
        "total_revenue": round(float(all_time_stats.total_revenue), 2) if all_time_stats.total_revenue else 0.0, 
        "total_sales": int(all_time_stats.total_sales) if all_time_stats.total_sales else 0,
        "total_orders": int(all_time_stats.total_orders) if all_time_stats.total_orders else 0,
        "total_customers": int(all_time_stats.total_customers) if all_time_stats.total_customers else 0, 
        "monthly_revenue": [
            {
                "month": int(sale.month),
                "total_revenue": round(float(sale.total_revenue), 2)
                if sale.total_revenue
                else 0.0,
            }
            for sale in monthly_revenue
        ],
        "monthly_orders": [
            {
                "month": int(sale.month),
                "total_orders": int(sale.total_orders)
                if sale.total_orders
                else 0,
            }
            for sale in monthly_orders
        ],
    }


# ----------------------------------------------------------------------------------------------------------------------------- vendor recent orders -----------------------------------------------------------------------------------------------------------------------------


def get_vendor_recent_orders_repo(user):
    # return specific needed fields only to speed up query
    return (
        db.session.query(
            Order.id,
            Order.created_at,
            Order.status,
            Product.name.label("product_name"),
            User.username.label("customer_username"),
            OrderItem.quantity,
            OrderItem.total_price,
        )
        .join(OrderItem, Order.id == OrderItem.order_id)
        .join(Product, OrderItem.product_id == Product.id)
        .join(User, Order.user_id == User.id)
        .filter(OrderItem.vendor_id == user.id)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )