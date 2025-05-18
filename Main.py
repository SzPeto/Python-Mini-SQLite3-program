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
        for i in range(0, len(result)):
            print(result[i])
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
            is_exit = True
        print("\n")



    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()