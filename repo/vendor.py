from instance.database import db
from models.user import UserRole, VendorProfile


def vendor_register_repo(user, vendor_data_validated):
    vendor_profile = VendorProfile(
        user_id=user.id,
        business_name=vendor_data_validated.business_name,
        business_description=vendor_data_validated.business_description,
        business_address=vendor_data_validated.business_address,
        business_phone=vendor_data_validated.business_phone,
        business_email=vendor_data_validated.business_email,
        business_logo_url=vendor_data_validated.business_logo_url,
    )

    user.role = UserRole.VENDOR.value
    user.vendor_status = "pending"

    db.session.add(vendor_profile)
    db.session.commit()


