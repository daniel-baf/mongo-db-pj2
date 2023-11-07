from . import DB
from datetime import datetime

collection_names = ["Manager", "Project", "Service"]


# run this function to initialize and configure MongoDB
def reset_setup():
    for collection in collection_names:
        DB.drop_collection(collection)
        DB.create_collection(collection)


# -----------------------------------
#               CREATE
# -----------------------------------
# create a worker into DB
def insert_manager(name: str, address: str, dpi: str):
    return DB.insert_into_collection(collection_names[0], {"name": name, "address": address, "dpi": dpi})


# insert multiple managers into collection
# row structure {"name": x, "address": x, "dpi": x} -> [{}, {}]
def insert_managers(managers_dictionary_list: list[dict]):
    return insert_many_collection(collection_names[0], managers_dictionary_list)


# insert a project into DB, use the follow structure to send
# beneficiary family dict: {"address": "x", "monthly_income": x float, members: [] }
# members family dict: [{}, {}, {}]
# member structure dict: {"name": "x", "last_name": "x", "age": x int }
# project details structure: [{}, {}]
# project detail substructure: { "quantity": x float, service_id: "x" } ... follow data will be estimated in the method
def insert_project(name: str, init_date: datetime, end_date: datetime, budget: float, manager_id: str,
                   beneficiary_family_address: str, beneficiary_family_monthly_income: float,
                   beneficiary_family_members: dict,
                   project_detail: list[dict], is_finished=False):
    data = {"name": name, "init_date": init_date, "end_date": end_date, "budget": budget,
            "manager_id": manager_id, "is_finished": is_finished,
            "details": project_detail,
            "beneficiary_family": {
                "address": beneficiary_family_address,
                "monthly_income": beneficiary_family_monthly_income,
                "members": beneficiary_family_members
            }}
    try:
        # check if manager exists
        if not list(find_managers({"_id": 1}, {"_id": manager_id})):
            raise Exception(f"No manager with id {manager_id} unable to continue insert")
        # check if services exists and add additional data
        for _item in project_detail:
            # check if exists on DB the detail
            mongo_data = list(find_services(None, {"_id": _item["service_id"]}))
            if not mongo_data:
                raise Exception(f"No service with id {_item['service_id']} unable to continue insert")
            # add extra values based on extracted data
            # TODO update service on quantity++
            mongo_data = mongo_data[0] # valid data, work with single result
            _item["subtotal"] = mongo_data["price"] * _item["quantity"]
        # valid to insert, CREATE JSON
        return DB.insert_into_collection(collection_names[1], data)
    except Exception as ex:
        raise Exception(f"Cannot insert {data} into DB\nError: {ex}")


# example data structure: {"service": x, "price": x num, "quantity": x}
def insert_service(data: dict):
    try:
        # search if exists -> create if not
        log = list(find_services({"_id": 0}, {"service": data["service"]}))  # cast to list and check len
        if not log:
            return DB.insert_into_collection(collection_names[2], data)
    except Exception as ex:
        raise Exception(f"Cannot insert {data} into DB\nError: {ex}")


# -----------------------------------
#                READ
# -----------------------------------
# select a manager, add to query, the values to return, and args the values to apply filter
def find_managers(query=None, args=None):
    return find_all_by_collection(collection_names[0], query, args)


# select a project, add to query, the values to return, and args the values to apply filter

def find_projects(query=None, args=None):
    return find_all_by_collection(collection_names[1], query, args)


# select a service, add to query, the values to return, and args the values to apply filter
def find_services(query=None, args=None):
    return find_all_by_collection(collection_names[2], query, args)


# -----------------------------------
#            GENERIC CRUD
# -----------------------------------

def insert_many_collection(collection: str, data: list[dict]):
    return DB.insert_many_into_collection(collection, data)


# find rows into a collection for this project schema
def find_all_by_collection(collection: str, query=None, args=None):
    try:
        if (query is None) and (args is None):
            return DB.find_all(collection)
        else:
            return DB.find_all(collection, True, query, args)
    except Exception as ex:
        raise Exception(f"Cannot get {collection} into DB\nError: {ex}")
