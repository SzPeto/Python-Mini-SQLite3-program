import sqlite3

def create_connection(db_name):
    try:
        connection = sqlite3.connect(db_name)
        print("Database created!")
        return connection
    except Exception as e:
        print(f"Something went wrong, error message : {e}")

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

# Main method **************************************************************************************
def main():

    # Creating the connection
    connection = create_connection("Databases\\employees.db")
    cursor = connection.cursor()

    # Creating the table
    create_table(cursor)

    # Creating a mini program to add to the database
    request = int(input("Please choose an option : 1:Add, 2:Delete, 3:Show database, 4:Update, 5:Search : "))
    if request == 1:
        try:
            id = int(input("Enter the employee id : "))
            name = str(input("Enter the employee name : "))
            age = int(input("Enter the employee age : "))
            position = str(input("Enter the employee position : "))
            show_all(cursor)
        except Exception as e:
            print(f"Something went wrong with inputting the values : {e}")
        insert_employee(cursor, id, name, age, position)
        connection.commit()
    elif request == 3:
        show_all(cursor)


    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()