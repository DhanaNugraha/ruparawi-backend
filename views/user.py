from flask import jsonify
from pydantic import ValidationError
from instance.database import db
from repo.user import update_user_repo, user_by_id_repo
from schemas.user import PublicUserProfileResponse, UserProfileUpdateRequest


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

    # not sure how to test
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "message": str(e),
                "success": False,
                "location": "view update user profile repo",
            }
        ), 500
