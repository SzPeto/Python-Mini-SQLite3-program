import os.path
import sqlite3
import sys


def create_connection(db_name):

    try:
        dir_name = os.path.dirname(db_name)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"Directory : {dir_name} successfully created")
    except Exception as e:
        print(f"Something went wrong creating the directory : {e}")
        sys.exit(1)

    try:
        connection = sqlite3.connect(db_name)
        print("Connection established!")
        return connection
    except Exception as e:
        print(f"Something went wrong connecting to the database: {e}")
        sys.exit(1)

def create_table(cursor):
    # IF NOT EXISTS - this is a statement on its own
    query = """
            CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY UNIQUE,
                name TEXT NOT NULL,
                age INTEGER,
                position TEXT
            )
        """
    cursor.execute(query)

def insert_employee(cursor, id: int, name: str, age: int, position: str):
    query = "INSERT INTO employees (id, name, age, position) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(query, (id, name, age, position))
        print("Values inserted")
    except Exception as e:
        print(f"Something went wring while inserting : {e}")

def show_all(cursor):
    query = "SELECT * FROM employees"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for i in range(0, len(result)):
                print(result[i])
        else:
            print("Empty database")
    except Exception as e:
        print(f"Something went wrong with showing the database : {e}")

def search(cursor, column, keyword):
    query = f"SELECT * FROM employees WHERE {column} = ?"
    try:
        cursor.execute(query, (keyword,)) # Put a comma here to treat it as tuple
        result = cursor.fetchall()
        for i in range(0, len(result)):
            print(result[i])
    except Exception as e:
        print(f"Something went wrong with searching the keyword : {e}")

def update_user(cursor, column_select, column_modify, value_select, value_modify):
    print(f"cselect : {column_select}, cmodify : {column_modify}, vselect : {value_select}, vmodify : {value_modify}")
    query = f"UPDATE employees SET {column_modify} = ? WHERE {column_select} = ?"

    try:
        cursor.execute(query, (value_modify, value_select))
        print(f"Employees entry of {column_select} : {value_select} has been updated. The new value of {column_modify} "
              f"has been updated to : {value_modify}")
        show_all(cursor)
    except Exception as e:
        print(f"Something went wrong during updating the database : {e}")

def delete(cursor, column, keyword):
    query = f"DELETE FROM employees WHERE {column} = ?"

    try:
        cursor.execute(query, (keyword,)) # Put a comma here to treat it as tuple
        show_all(cursor)
        print(f"{column} : {keyword} successfully deleted")
    except Exception as e:
        print(f"Something went wrong while deleting : {e}")


# Main method **************************************************************************************
def main():

    is_exit = False
    is_valid_delete = False
    is_valid_search = False
    is_valid_id = False
    is_valid_age = False
    # Creating the connection
    connection = create_connection("Databases\\employees.db")
    cursor = connection.cursor()

    # Creating the table
    create_table(cursor)

    # Creating a mini program to add to the database
    while not is_exit:
        name = ""
        position = ""
        is_valid_search = False
        is_valid_delete = False
        is_valid_age = False
        is_valid_id = False
        is_valid_update = False
        is_valid_value_select = False
        is_valid_value_modify = False
        request = input("Please choose an option : 1:Add, 2:Delete, 3:Show database, 4:Update, 5:Search, 6:Exit : ")
        if request.isdigit():
            request = int(request)
            if request < 1 or request > 6:
                print("Please enter a number in valid range")
                continue

        else:
            print("Please enter a valid number")
            continue

        if request == 1:
            try:
                while not is_valid_id:
                    id = input("Enter the employee id : ")
                    if id.isdigit():
                        id = int(id)
                        is_valid_id = True
                    else:
                        print("You must enter a number")
                        continue
                while not name:
                    name = str(input("Enter the employee name and surname: "))
                    if not name:
                        print("Name cannot be empty")
                while not is_valid_age:
                    age = input("Enter the employee age : ")
                    if age.isdigit():
                        age = int(age)
                        is_valid_age = True
                    else:
                        print("You must enter a number")
                while not position:
                    position = str(input("Enter the employee position : "))
                    if not position:
                        print("Position cannot be empty")
                insert_employee(cursor, id, name, age, position)
                connection.commit()
                show_all(cursor)
            except Exception as e:
                print(f"Something went wrong with inputting the values : {e}")
        elif request == 2:
            while not is_valid_delete:
                type_delete = input("What keyword would you like to use for delete? 1:id, 2:name, 3:age, 4:position : ")
                if type_delete.isdigit():
                    type_delete = int(type_delete)
                    if type_delete < 1 or type_delete > 4:
                        print("You must enter a number in valid range")
                        continue
                    is_valid_delete = True
                else:
                    print("You must enter a number")

            if type_delete == 1:
                column = "id"
                keyword = int(input("Please enter the id to delete : "))
            elif type_delete == 2:
                column = "name"
                keyword = str(input("Please enter the name to delete : "))
            elif type_delete == 3:
                column = "age"
                keyword = int(input("Please enter the age to delete : "))
            elif type_delete == 4:
                column = "position"
                keyword = str(input("Please enter the position to delete : "))
            delete(cursor, column, keyword)
            connection.commit()
        elif request == 3:
            show_all(cursor)
        elif request == 4:
            while not is_valid_update:
                is_valid_update = False

                # Configuring the selection *************
                update_request_select = input(
                    f"What keyword would you like to use to select the entry for modification? "
                    f"1:id, 2:name, 3:age, 4:position")
                if update_request_select.isdigit():
                    update_request_select = int(update_request_select)
                    if update_request_select < 1 or update_request_select > 4:
                        print("You have to enter a number between 1 and 4")
                        continue
                else:
                    print("You have to enter a number")
                    continue

                if update_request_select == 1:
                    column_select = "id"
                    is_valid_value_select = False
                    while not is_valid_value_select:
                        is_valid_value_select = False
                        value_select = input("Please enter the id of the entry to modify : ")
                        if value_select.isdigit():
                            value_select = int(value_select)
                            is_valid_value_select = True
                        else:
                            print("You must enter a number")
                            continue
                elif update_request_select == 2:
                    column_select = "name"
                    value_select = input("Please enter the name of the entry to modify : ")
                elif update_request_select == 3:
                    column_select = "age"
                    is_valid_value_select = False
                    while not is_valid_value_select:
                        is_valid_value_select = False
                        value_select = input("Please enter the age of the entry to modify : ")
                        if value_select.isdigit():
                            value_select = int(value_select)
                            is_valid_value_select = True
                        else:
                            print("You must enter a number")
                            continue
                elif update_request_select == 4:
                    column_select = "position"
                    value_select = input("Please enter the position of the entry to modify : ")

                # Configuring the modification *************
                update_request_modify = input(
                    f"Which field of the selected entry would you like to modify? "
                    f"1:id, 2:name, 3:age, 4:position")
                if update_request_modify.isdigit():
                    update_request_modify = int(update_request_modify)
                    if update_request_modify < 1 or update_request_modify > 4:
                        print("You have to enter a number between 1 and 4")
                        continue
                else:
                    print("You have to enter a number")
                    continue

                if update_request_modify == 1:
                    column_modify = "id"
                    is_valid_value_modify = False
                    while not is_valid_value_modify:
                        is_valid_value_modify = False
                        value_modify = input("Please enter the id of the entry to modify : ")
                        if value_modify.isdigit():
                            value_modify = int(value_modify)
                            is_valid_value_modify = True
                        else:
                            print("You must enter a number")
                            continue
                elif update_request_modify == 2:
                    column_modify = "name"
                    value_modify = input("Please enter the name of the entry to modify : ")
                elif update_request_modify == 3:
                    column_modify = "age"
                    is_valid_value_modify = False
                    while not is_valid_value_modify:
                        is_valid_value_modify = False
                        value_modify = input("Please enter the age of the entry to modify : ")
                        if value_modify.isdigit():
                            value_modify = int(value_modify)
                            is_valid_value_modify = True
                        else:
                            print("You must enter a number")
                            continue
                elif update_request_modify == 4:
                    column_modify = "position"
                    value_modify = input("Please enter the position of the entry to modify : ")
                is_valid_update = True
            update_user(cursor, column_select, column_modify, value_select, value_modify)
            connection.commit()

        elif request == 5:
            while not is_valid_search:
                type_search = input("What keyword would you like to use for search? 1:id, 2:name, 3:age, 4:position : ")
                if type_search.isdigit():
                    type_search = int(type_search)
                    if type_search < 1 or type_search > 4:
                        print("You must enter a number in valid range")
                        continue
                    is_valid_search = True
                else:
                    print("You must enter a number")

            if type_search == 1:
                column = "id"
                keyword = int(input("Please enter the id to search : "))
                search(cursor, column, keyword)
            elif type_search == 2:
                column = "name"
                keyword = str(input("Please enter the name to search : "))
                search(cursor, column, keyword)
            elif type_search == 3:
                column = "age"
                keyword = int(input("Please enter the age to search : "))
                search(cursor, column, keyword)
            elif type_search == 4:
                column = "position"
                keyword = str(input("Please enter the position to search : "))
                search(cursor, column, keyword)
        elif request == 6:
            print("Exiting...")
            is_exit = True
        print("\n")



    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()