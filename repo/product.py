from instance.database import db
from models.product import Product, ProductCategory, ProductImage, SustainabilityAttribute, ProductTag, Wishlist
from sqlalchemy.orm import joinedload


def create_product_repo(product_data, user_id):
    product = Product(
        name = product_data.name,
        description=product_data.description,
        price=float(product_data.price),  # Convert Decimal for SQLAlchemy
        category_id=product_data.category_id,
        vendor_id=user_id,
        stock_quantity=product_data.stock_quantity,
        min_order_quantity=product_data.min_order_quantity
    )

    db.session.add(product)
    # flush will insert data to db to get id but not commit yet
    db.session.flush()

    return product

def process_product_images_repo(primary_image, images_list, product_id):
    for image_url in images_list:
        product_image = ProductImage(
            product_id=product_id,
            image_url=image_url,
        )

        db.session.add(product_image)

    product_image = ProductImage(
        product_id=product_id,
        image_url=primary_image,
        is_primary=True
    )

    db.session.add(product_image)


def process_tags_repo(tags_list, product): 
    for tag_name in tags_list:
        tag = db.session.execute(
            db.select(ProductTag).filter_by(name=tag_name)
        ).scalar_one_or_none()

        if not tag:
            tag = ProductTag(name=tag_name)
            db.session.add(tag)

        # create many to many bi-directional relationship
        # appends product.id and tag.id to association table
        product.tags.append(tag)


def process_sustainability_repo(sustainability_attributes, product):
    for sustainability_attribute in sustainability_attributes:
        attribute = db.session.execute(
            db.select(SustainabilityAttribute).filter_by(name=sustainability_attribute)
        ).scalar_one_or_none()
        
        if not attribute:
            attribute = SustainabilityAttribute(name=sustainability_attribute)
            db.session.add(attribute)

        # create many to many bi-directional relationship
        # appends product.id and attribute.id to association table
        product.sustainability_attributes.append(attribute)


def get_products_list_repo(product_filter, request_args):
    # base query
    products = db.select(Product).filter_by(is_active=True)
    
    # extra filters if any
    if product_filter.category_id:
        products = products.filter_by(category_id=product_filter.category_id)

    if product_filter.tags:
        # assuming that it joins with the help of association
        products = products.join(Product.tags, isouter=True).filter(ProductTag.name.in_(product_filter.tags))

    if product_filter.min_price:
        products = products.filter(Product.price >= product_filter.min_price)

    if product_filter.max_price:
        products = products.filter(Product.price <= product_filter.max_price)

    # prevent duplicates from join
    products = products.group_by(Product.id)

    # pagination of query
    paginated_products = db.paginate(products)

    return paginated_products


def get_product_detail_repo(product_id):
    return db.one_or_404(
        db.select(Product).filter_by(id=product_id),
        description=f"No product with id '{product_id}'.",
    )


def update_product_repo(user_id, product_id, update_data):
    # Verify product exists and belongs to current vendor
    product = db.one_or_404(
        db.select(Product).filter_by(id=product_id, vendor_id=user_id),
        description=f"No product with id '{product_id}' and vendor id '{user_id}'.",    
    )

    # Apply updates
    if update_data.name is not None:
        product.name = update_data.name

    if update_data.description is not None:
        product.description = update_data.description

    if update_data.price is not None:
        product.price = float(
            update_data.price
        )  # Convert Decimal to float for SQLAlchemy

    if update_data.category_id is not None:
        product.category_id = update_data.category_id

    if update_data.is_active is not None:
        product.is_active = update_data.is_active

    if update_data.stock_quantity is not None:
        product.stock_quantity = update_data.stock_quantity

    if update_data.min_order_quantity is not None:
        product.min_order_quantity = update_data.min_order_quantity

    return product


def soft_delete_product_repo(product):
    product.is_active = False
    db.session.commit()


# ----------------------------------------------------------- Wishlist -----------------------------------------------------------


def add_product_to_wishlist_by_user_id_repo(user_id, product):
    wishlist = db.session.execute(
        db.select(Wishlist).filter_by(user_id=user_id)
    ).scalar_one_or_none()

    if not wishlist:
        wishlist = Wishlist(user_id=user_id)
        db.session.add(wishlist)

    if wishlist.add_product(product):
        db.session.commit()

        return wishlist
    
    else:
        return None
    

def remove_product_from_wishlist_repo(wishlist, product):
    if wishlist.remove_product(product):
        db.session.commit()

        return wishlist
    
    else:
        return None
    

def get_wishlist_by_user_id_repo(user_id):
    return db.one_or_404(
        db.select(Wishlist).filter_by(user_id=user_id),
        description=f"No wishlist with user id '{user_id}'.",
    )


def get_product_primary_image_repo(product_id):
    return db.session.execute(
        db.select(ProductImage.image_url)
        .filter_by(product_id=product_id, is_primary=True)
    ).scalar_one_or_none()



# ----------------------------------------------------------- Categories -----------------------------------------------------------


def get_top_level_categories_repo():
    return (
        db.session.execute(
            db.select(ProductCategory).filter_by(
                parent_category_id=None, is_active=True
            )
        )
        .scalars()
        .all()
    )


def get_category_by_id_repo(category_id):
    return db.one_or_404(
        db.select(ProductCategory).filter_by(id=category_id),
        description=f"Category does not exist '{category_id}'.",
    )


def get_vendor_products_repo(user_id):
    products = db.select(Product).filter_by(vendor_id=user_id)

    paginated_products = db.paginate(products)
    return paginated_products


def verify_product_repo(product, requested_quantity):
    if product.stock_quantity < requested_quantity:
        return ("Not enough stock", False)

    if product.is_active is False:
        return ("Product is inactive", False)

    return ("", True)