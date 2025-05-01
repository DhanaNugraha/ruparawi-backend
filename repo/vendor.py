from instance.database import db
from models.user import UserRole, VendorProfile, VendorStatus


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
