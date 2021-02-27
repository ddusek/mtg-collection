from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import HashingError, VerificationError, VerifyMismatchError, InvalidHash
from pymongo.database import Database  # TODO remove this
from mtg_collection.database import logger


class Authenticator:
    """Class for registration and login of users.
    """
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
        return '@' in login

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
                {'username': user.username},
                {'$set': {'password': new_hashed_pwd}})
        except HashingError as err:
            logger.exception(err)

    def register_user(self, username: str, password: str, email: str) -> (bool, str):
        """Register a new user.

        :param username: Username of user.
        :type username: str
        :param password: Password of user.
        :type password: str
        :param email: Email of user.
        :type email: str
        :return: bool with message about failed/success login.
        :rtype: (bool, str)
        """
        exists = self._mongo_db.users.count_documents(
            {'$or':
                [{'username': username}, {'email': email}]},
            {'limit': 1})
        if any(exists):
            return (False, 'Username or email already registered.')
        try:
            hashed_pwd = self._pwd_hasher.hash(password)
            self._mongo_db.users.insert_one(
                {'username': username,
                 'password': hashed_pwd,
                 'email': email,
                 'created': datetime.now(),
                 'last_login': datetime.now()
                 })
            return (True, 'success')
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
        user = self._mongo_db.users.find_one({'email': login}) \
            if self._is_email(login) else \
            self._mongo_db.users.find_one({'username': login})

        try:
            if self._pwd_hasher.verify(user.password, password):
                # If user was verified, rehash password if it's needed.
                if self._pwd_hasher.check_needs_rehash(user.password):
                    self._rehash_password(user, password)
                return {'success': True, 'user': user._id, 'error': ''}
            return {'success': False, 'user': 0, 'error': 'Failed to verify password.'}

        except (VerificationError, VerifyMismatchError) as err:
            logger.info(err)
        except InvalidHash as err:
            logger.exception(err)
