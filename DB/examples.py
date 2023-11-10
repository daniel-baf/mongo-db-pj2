from DB import DBDict
from datetime import datetime


def print_data():
    # find on DB
    print("---- MANAGERS ----")
    # all maangers
    list(map(lambda _doc: print(_doc), DBDict.find_managers()))
    print("---- SERVICES ----")
    # all services
    list(map(lambda _doc: print(_doc), DBDict.find_services()))
    print("---- PROJECTS ----")
    # all projects
    list(map(lambda _doc: print(_doc), DBDict.find_projects()))
    print("")


def insert_examples():
    # MANAGERS
    DBDict.insert_manager("Daniel Bautista", "Calle xxxxxxxxx", "12345678")
    DBDict.insert_managers([{"name": "Pablo COti", "address": "Calle yyyyyyyyy", "dpi": "09876543"},
                            {"name": "Angel Cotoc", "address": "Calle zzzzzzz", "dpi": "6758493920"}])

    # PROJECT
    # recover ID
    manager_id = DBDict.find_managers({"_id": 1}, {"dpi": "12345678"})[0]["_id"]  # return only id for DPI = x
    family_members = [{"name": "Pepe", "age": 25},
                      {"name": "Anacleto", "age": 19}]
    service_id = DBDict.find_services(None, {"service": "AGUA" })[0]  # return only id for service = agua
    project_details = [{"quantity": 2, "service": {"_id": service_id["_id"], "service": service_id["service"]}}]
    DBDict.insert_project("Project no. 1", datetime.now(),  1540022.21, manager_id, "Street A 12B x zone 2", 8942.20, "Sinforoso", family_members, project_details, False)


def run():
    DBDict.reset_setup()
    insert_examples()

    # print_data()
