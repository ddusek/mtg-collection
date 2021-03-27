"""Helper methods for working with both MongoDB and Redis.
"""
from bson.objectid import ObjectId
from pymongo.database import Database  # TODO remove this
from redis import Redis


def load_user_to_redis(
    mongo_db: Database, redis: Redis, user_id: ObjectId, duration: int
) -> bool:
    """Load all user data into redis for a specified period time.

    :param mongo_db: Mongo database.
    :type mongo_db: Database
    :param redis: Redis instance.
    :type redis: Redis
    :param user_id: userID from Mongo.
    :type user_id: ObjectId
    :param duration: expiration of keys in Redis (in seconds).
    :type duration: int
    :return: True if success.
    :rtype: bool
    """
    user = mongo_db.users.find_one({"_id": user_id})
