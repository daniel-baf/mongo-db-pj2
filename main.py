from DB import DBDict
from datetime import datetime, timedelta


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
    DBDict.insert_managers([{"name": "Pablo COti", "adress": "Calle yyyyyyyyy", "dpi": "09876543"},
                            {"name": "Angel Cotoc", "adress": "Calle zzzzzzz", "dpi": "6758493920"}])
    # SERVICES
    DBDict.insert_service({"service": "agua", "price": 45, "quantity": 0})
    DBDict.insert_service({"service": "agua", "price": 45, "quantity": 0})  # ignored by code, no duplicates

    # PROJECT
    # recover ID
    manager_id = DBDict.find_managers({"_id": 1}, {"dpi": "12345678"})[0]["_id"]  # return only id for DPI = x
    family_members = [{"name": "Pepe", "last_name": "El pollo", "age": 25},
                      {"name": "Anacleto", "last_name": "Sinforoso", "age": 19}]
    service_id = DBDict.find_services({"_id": 1}, {"service": "agua"})[0]["_id"]  # return only id for service = agua
    project_details = [{"quantity": 2, "service_id": service_id}]
    DBDict.insert_project("Project no. 1", datetime.now(), datetime.now() + timedelta(days=365 * 3), 1540022.21,
                          manager_id, "Street A 12B x zone 2", 8942.20, family_members, project_details, False)


def run():
    DBDict.reset_setup()
    insert_examples()

    print_data()
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
