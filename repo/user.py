from instance.database import db
from models.user import User, UserAddress, UserPaymentMethod, UserRole
from shared.time import now, datetime_from_string

def user_by_id_repo(user_id):
    return db.one_or_404(
        db.select(User).filter_by(id=user_id),
        description=f"No user with id '{user_id}'.",
    )


def user_by_email_repo(email):
    return db.one_or_404(
        db.select(User).filter_by(email=email),
        description=f"No user with email '{email}'.",
    )


def register_user_repo(user_data):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        # for testing, created_at and updated_at are added
        # just using now() doesnt work for testing
        created_at=datetime_from_string(str(now())),
        updated_at=datetime_from_string(str(now()))
    )

    new_user.password = user_data.password

    db.session.add(new_user)

    buyer_role = db.one_or_404(
        db.select(UserRole).filter_by(name="buyer"),
        description="No role with name 'buyer'.",
    )

    new_user.role.append(buyer_role)

    db.session.commit()


def update_last_login_repo(queried_user):
    queried_user.last_login = datetime_from_string(str(now()))
    db.session.commit()


def update_user_repo(user, user_data):
    if user_data.bio:
        user.bio = user_data.bio

    if user_data.profile_image_url:
        user.profile_image_url = user_data.profile_image_url

    if user_data.first_name:
        user.first_name = user_data.first_name

    if user_data.last_name:
        user.last_name = user_data.last_name

    if user_data.password:
        user.password = user_data.password

    db.session.commit()


def add_address_repo(user, address):
    # set all other addresses to not default if new address is default
    if address.is_default:
        db.session.execute(
            db.update(UserAddress)
            .where(UserAddress.user_id == user.id, UserAddress.is_default == True)  # noqa: E712
            .values(is_default=False)
        )

    new_address = UserAddress(user_id=user.id, **address.model_dump())

    db.session.add(new_address)
    db.session.commit()

    return new_address


def delete_address_repo(user, address_id):
    address = db.one_or_404(
        db.select(UserAddress).filter_by(id=address_id, user_id=user.id),
        description=f"No address with id '{address_id}' and user id '{user.id}'.",
    )

    db.session.delete(address)
    db.session.commit()


def update_address_repo(user, address_data, address_id):
    # set all other addresses to not default if new address is default
    if address_data.is_default:
        db.session.execute(
            db.update(UserAddress)
            .where(UserAddress.user_id == user.id, UserAddress.is_default == True)  # noqa: E712
            .values(is_default=False)
        )

    # get address
    address = db.one_or_404(
        db.select(UserAddress).filter_by(id=address_id, user_id=user.id),
        description=f"No address with id '{address_id}' and user id '{user.id}'.",
    )

    for field, value in address_data.model_dump().items():
        # only update the field if it is not None
        if value is not None:
            setattr(address, field, value)

    db.session.commit()

    return address


def get_all_address_repo(user):
    return (
        db.session.execute(
            db.select(UserAddress).filter_by(user_id=user.id)
        )
        .scalars()
    )


def add_payment_method_repo(user, payment_method_data):
    # set all other payment methods to not default if new payment method is default
    if payment_method_data.is_default:
        db.session.execute(
            db.update(UserPaymentMethod)
            .where(
                UserPaymentMethod.user_id == user.id,
                UserPaymentMethod.is_default == True,  # noqa: E712
            )
            .values(is_default=False)
        )

    new_payment_method = UserPaymentMethod(
        user_id=user.id, 
        payment_type=payment_method_data.payment_type,
        provider=payment_method_data.provider,
        account_number=payment_method_data.account_number,
        expiry_date=payment_method_data.expiry_date,
        is_default=payment_method_data.is_default
    )


    db.session.add(new_payment_method)
    db.session.commit()

    return new_payment_method


def update_payment_method_repo(user, payment_method_data, payment_method_id):
    # set all other payment methods to not default if new payment method is default
    if payment_method_data.is_default:
        db.session.execute(
            db.update(UserPaymentMethod)
            .where(
                UserPaymentMethod.user_id == user.id,
                UserPaymentMethod.is_default == True,  # noqa: E712
            )
            .values(is_default=False)
        )

    # get payment method
    payment_method = db.one_or_404(
        db.select(UserPaymentMethod).filter_by(id=payment_method_id, user_id=user.id),
        description=f"No payment method with id '{payment_method_id}' and user id '{user.id}'.",
    )

    for field, value in payment_method_data.model_dump().items():
        # only update the field if it is not None
        if value is not None:
            setattr(payment_method, field, value)

    db.session.commit()

    return payment_method


def delete_payment_method_repo(user, payment_method_id):
    payment_method = db.one_or_404(
        db.select(UserPaymentMethod).filter_by(id=payment_method_id, user_id=user.id),
        description=f"No payment method with id '{payment_method_id}' and user id '{user.id}'.",
    )

    db.session.delete(payment_method)
    db.session.commit()
