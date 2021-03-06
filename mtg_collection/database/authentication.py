from os import urandom
from base64 import b64encode
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import (
    HashingError,
    VerificationError,
    VerifyMismatchError,
    InvalidHash,
)
from bson.objectid import ObjectId
from pymongo.database import Database  # TODO remove this
from mtg_collection.database import logger


class Authenticator:
    """Class for registration and login of users."""

    def __init__(self, mongo_db: Database):
        self._mongo_db = mongo_db
        self._pwd_hasher = PasswordHasher()

    def _is_email(self, login: str) -> bool:
        """Check if login is email or username.

        :param login: login from input.
        :type login: str
        :return: true if email, false if username.
        :rtype: bool
        """
        return "@" in login

    def _rehash_password(self, user, password: str):
        """hash password again if Argon2 parameters change.

        :param user: User Document from mongo.
        :type user: Document
        :param password: Password to rehash.
        :type password: str
        """
        try:
            new_hashed_pwd = self._pwd_hasher.hash(password)
            self._mongo_db.users.update_one(
                {"username": user.username}, {"$set": {"password": new_hashed_pwd}}
            )
        except HashingError as err:
            logger.exception(err)

    def register_user(self, username: str, password: str, email: str) -> dict:
        """Register a new user.

        :param username: Username of user.
        :type username: str
        :param password: Password of user.
        :type password: str
        :param email: Email of user.
        :type email: str
        :return: bool about failed/success login, user token and userID if success.
        :rtype: (bool, str)
        """
        if not username:
            raise ValueError("cannot register user, didnt get username")
        if not password:
            raise ValueError("cannot register user, didnt get password")
        if not email:
            raise ValueError("cannot register user, didnt get email")

        exists = self._mongo_db.users.count_documents(
            {"$or": [{"username": username}, {"email": email}]}, limit=1
        )
        if exists > 0:
            return (False, "Username or email already registered.")
        try:
            token = b64encode(urandom(128)).decode("utf-8")

            _id = self._mongo_db.users.insert_one(
                {
                    "username": username,
                    "password": self._pwd_hasher.hash(password),
                    "email": email,
                    "created": datetime.now(),
                    "last_login": datetime.now(),
                    "tokens": [token],
                }
            ).inserted_id
            return {"success": True, "token": token, "id": _id}
        except HashingError as err:
            logger.exception(err)

    def login_user(self, login: str, password: str) -> dict:
        """Validate password and return dictionary according to result.

        :param login: Username or email of user.
        :type login: str
        :param password: Password of user.
        :type password: str
        :return: {success: bool, user: userID, error: str}.
        :rtype: dict
        """
        user = (
            self._mongo_db.users.find_one({"email": login})
            if self._is_email(login)
            else self._mongo_db.users.find_one({"username": login})
        )

        try:
            if self._pwd_hasher.verify(user.password, password):
                # If user was verified, rehash password if it's needed.
                if self._pwd_hasher.check_needs_rehash(user.password):
                    self._rehash_password(user, password)
                return {"success": True, "user": user._id, "error": ""}
            return {"success": False, "user": 0, "error": "Failed to verify password."}

        except (VerificationError, VerifyMismatchError) as err:
            logger.info(err)
        except InvalidHash as err:
            logger.exception(err)

    def logout_user(self, token: str, user_id: str) -> dict:
        """Logout user with deleting his login token from the database.

        :param token: Username or email of user.
        :type token: str
        :return: {success: bool, user: userID, error: str}.
        :rtype: dict
        """
        print(token, ObjectId(user_id))
        user = self._mongo_db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$pull": {"tokens": token}}
        )
        if user.modified_count < 1:
            return {"success": False, "message": "User or token not found."}
        return {"success": True, "message": "token removed from database"}
