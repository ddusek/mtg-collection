from bson.objectid import ObjectId
from pymongo.database import Database  # TODO remove this
from mtg_collection.database import logger


def add_card_to_mongo(
    mongo: Database, user: str, collection: str, card: str, edition: str, units: int
) -> object:
    """Add card to mongo.

    :param mongo: Mongo database.
    :type mongo: Database
    :param collection: Collection where to add card.
    :type collection: str
    :param card: Card to add.
    :type card: str
    :param edition: Edition of card to add.
    :type edition: str
    :param units: Number of units to add.
    :type units: int
    :return: {"success": bool, "message": info about fail}
    :rtype: object
    """
    collection_key = f"collections.{collection}"
    exists = mongo.users.count_documents(
        {
            "username": user,
            collection_key: {"$elemMatch": {"card": card, "edition": edition}},
        },
        limit=1,
    )
    if exists > 0:
        return (False, "Card already added in this collection.")
    mongo.users.find_one_and_update(
        {"username": user, collection_key: {"$exists": True}},
        {
            "$push": {
                collection_key: {
                    "card": card,
                    "edition": edition,
                    "units": units,
                }
            }
        },
    )
    return {"success": True}


def add_collection_to_mongo(mongo: Database, collection: str, user: str) -> object:
    """Add new collection to mongo if does not exist yet.

    :param mongo: Mongo database.
    :type mongo: Database
    :param collection: Collection name.
    :type collection: str
    :param user: User ID.
    :type user: str
    :return: {"success": bool}
    :rtype: object
    """
    exists = mongo.users.count_documents(
        {"$and": [{"user": user}, {f"collections.{collection}": {"$exists": True}}]},
        limit=1,
    )
    if exists > 0:
        return {"success": False, "message": "Collection already exists."}
    mongo.users.update({"username": user}, {"$set": {f"collections.{collection}": []}})
    return {"success": True, "message": ""}
