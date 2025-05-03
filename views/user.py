from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.user import add_address_repo, add_payment_method_repo, delete_address_repo, delete_payment_method_repo, get_all_address_repo, update_address_repo, update_payment_method_repo, update_user_repo, user_by_id_repo
from schemas.user import PublicUserProfileResponse, UserAddressCreate, UserAddressResponse, UserAddressUpdate, UserPaymentMethodBase, UserPaymentMethodResponse, UserProfileUpdateRequest


# ------------------------------------------------------ Get Public User Profile --------------------------------------------------


def get_public_user_profile_view(user_id):
    try:
        user = user_by_id_repo(user_id)

        filtered_user_data = PublicUserProfileResponse.model_validate(user)

        return jsonify({"success": True, "user": filtered_user_data.model_dump()}), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get public user profile repo",
            }
        ), 500


# ------------------------------------------------------ Update User Profile --------------------------------------------------


def update_user_profile_view(user, user_request):
    try:
        user_data_validated = UserProfileUpdateRequest.model_validate(user_request)

        update_user_repo(user, user_data_validated)

        return jsonify(
            {"success": True, "message": "Profile updated successfully"}
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update user profile request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update user profile repo",
            }
        ), 500


# ------------------------------------------------------ Add address --------------------------------------------------


def add_address_view(user, address_request):
    try:
        address_data_validated = UserAddressCreate.model_validate(address_request)

        added_address = add_address_repo(user, address_data_validated)

        return jsonify(
            {
                "success": True,
                "message": "Address added successfully",
                "address_id": added_address.id,
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add address request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add address repo",
            }
        ), 500


# ------------------------------------------------------ delete address --------------------------------------------------


def delete_address_view(user, address_id):
    try:
        delete_address_repo(user, address_id)

        return jsonify(
            {"success": True, "message": "Address deleted successfully"}
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view delete address repo",
            }
        ), 500


# ------------------------------------------------------ Update user address --------------------------------------------------


def update_address_view(user, address_request, address_id):
    try:
        address_data_validated = UserAddressUpdate.model_validate(address_request)

        updated_address = update_address_repo(user, address_data_validated, address_id)

        return jsonify(
            {
                "success": True,
                "message": "Address updated successfully",
                "address_id": updated_address.id,
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update address request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update address repo",
            }
        ), 500


# ------------------------------------------------------ Get all addresses --------------------------------------------------


def get_all_address_view(user):
    try:
        addresses = get_all_address_repo(user)

        address_response = [UserAddressResponse.model_validate(address).model_dump() for address in addresses]

        return jsonify(
            {
                "success": True,
                "addresses": address_response,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get all address repo",
            }
        ), 500


# ------------------------------------------------------ Add payment method --------------------------------------------------


def add_payment_method_view(user, payment_method_request):
    try:
        payment_method_data_validated = UserPaymentMethodBase.model_validate(
            payment_method_request
        )

        payment_created = add_payment_method_repo(user, payment_method_data_validated)

        return jsonify(
            {
                "success": True,
                "message": UserPaymentMethodResponse.model_validate(
                    payment_created
                ).model_dump(),
            }
        ), 201

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add payment method request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view add payment method repo",
            }
        ), 500


# ------------------------------------------------------ Get all payment methods --------------------------------------------------


def get_payment_methods_view(user):
    try:
        payment_methods = user.payment_methods

        payment_methods_response = [
            UserPaymentMethodResponse.model_validate(payment_method).model_dump()
            for payment_method in payment_methods
        ]

        return jsonify(
            {
                "success": True,
                "payment_methods": payment_methods_response,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view get payment methods repo",
            }
        ), 500


# ------------------------------------------------------ update payment method --------------------------------------------------


def update_payment_method_view(user, payment_method_request, payment_method_id):
    try:
        payment_method_data_validated = UserPaymentMethodBase.model_validate(
            payment_method_request
        )

        payment_updated = update_payment_method_repo(
            user, payment_method_data_validated, payment_method_id
        )

        return jsonify(
            {
                "success": True,
                "message": UserPaymentMethodResponse.model_validate(
                    payment_updated
                ).model_dump(),
            }
        ), 200

    except ValidationError as e:
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update payment method request validation",
            }
        ), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update payment method repo",
            }
        ), 500


# ------------------------------------------------------ delete payment method --------------------------------------------------


def delete_payment_method_view(user, payment_method_id):
    try:
        delete_payment_method_repo(user, payment_method_id)

        return jsonify(
            {"success": True, "message": "Payment method deleted successfully"}
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view delete payment method repo",
            }
        ), 500