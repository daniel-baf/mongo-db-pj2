import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_name = "modelado"  # db name
database = db_client[db_name]  # create DB instance


# create a collection, call this method if needed
# insert function create the collection even if collection doesn't exist
# return True if created, False if collection already exists, exception if error while execution
def create_collection(collection_name: str):
    global database
    try:
        # check if collection exists
        collection_list = database.list_collection_names()
        if collection_name in collection_list: return False  # collection exists
        db_collection = database[collection_name]
        return True
    except Exception as ex:
        raise Exception(f"Error creating collection {collection_name}\nError: {ex}")


def drop_collection(collection_name: str):
    global database
    try:
        database[collection_name].drop()
    except Exception as ex:
        raise Exception(f"Error trying to drop collection {collection_name}\nError: {ex}")


# insert a value into <collection_name>
# send the collection and the row to insert as a JSON / dictionary
# return inserted_id value if inserted, this is the new id
# ej. { key: value, key2, value }
def insert_into_collection(collection_name: str, collection_row: dict):
    global database
    try:
        db_status = database[collection_name].insert_one(collection_row)
        return db_status.inserted_id
    except Exception as ex:
        raise Exception(f"Unable to insert row into {database[collection_name]}\nError: {ex}")


# insert a group of rows into <collection_name>
# send the collection and the row to insert as a JSON / dictionary
# return the list of inserted_ids
# ej. [{ key: value, key2, value }, { key: value, key2, value }]
def insert_many_into_collection(collection_name: str, collection_list_to_insert: list[dict]):
    try:
        db_status = database[collection_name].insert_many(collection_list_to_insert)
        return db_status.inserted_ids
    except Exception as ex:
        raise Exception(f"Unable to insert row into {database[collection_name]}\nError: {ex}")


# get the first occurrence in <collection_name>, raises error if mongoBD internal error
def find_one(collection_name: str):
    try:
        return database[collection_name].find_one()
    except Exception as ex:
        raise Exception(f"Unable to find first occurrence {database[collection_name]}\nError: {ex}")


# search all documents into mongoDB collection
# send parameter user filter true and filters if fiter search
# use_filter = false -> all documents
# use_filter = true $ query = {key: value, key2:value} -> rows with filter match
# query can include a regex, ej: { "address": { "$regex": "^S" } }
def find_all(collection_name: str, use_filter=False, query=None, args=None):
    try:
        if use_filter is False: return database[collection_name].find()
        else: return database[collection_name].find(args, query)
    except Exception as ex:
        raise Exception(f"Unable to find all occurrences for {database[collection_name]}\nError: {ex}")


# delete the first match with query at <collection_name> collection
# send filters as a query, query can include regex
# this method can be used to delete many, just set optional parameter as True
# set <use_delete_many> True and query to empty to delete all documents
# return the deleted file
def delete(collection_name: str, query={}, use_delete_many=False):
    try:
        if not use_delete_many: return database[collection_name].delete_one(query)
        else: return database[collection_name].delete_many(query)
    except Exception as ex:
        raise Exception(f"Unable to delete occurrence {database[collection_name]}\nError: {ex}")


# update a document from a collection
# send the query and new parameters as a dictionary, ej: {key: value}
# enable use_update_many to update multiple documents where query matches
def update(collection_name: str, query: dict, new_values: dict, use_update_many=False):
    try:
        if not use_update_many: return database[collection_name].update_one(query, new_values)
        else: return database[collection_name].update_many(query)
    except Exception as ex:
        raise Exception(f"Unable to delete occurrence {database[collection_name]}\nError: {ex}")
