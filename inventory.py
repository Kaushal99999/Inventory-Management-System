import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(filename='project.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

def create_connection():
    """ Create a database connection """
    try:
        connection = mysql.connector.connect(host="localhost", user="root", passwd="himanshu", db="project")
        if connection.is_connected():
            logging.info("Connected to MySQL database")
            return connection
    except Error as e:
        logging.error(f"Error while connecting to MySQL: {e}")
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """ Close database connection """
    if connection.is_connected():
        connection.close()
        logging.info("MySQL connection is closed")

def execute_query(connection, query, data=None):
    """ Execute a query and commit changes """
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        logging.info(f"Query executed: {query}")
    except Error as e:
        logging.error(f"Error executing query: {query}, Error: {e}")
        print(f"Error: {e}")

def fetch_query(connection, query):
    """ Fetch results from a query """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        logging.info(f"Query fetched: {query}")
        return result
    except Error as e:
        logging.error(f"Error fetching query: {query}, Error: {e}")
        print(f"Error: {e}")
        return None

def products(connection):
    L = ['Model NO.', 'Brand', 'Launch Date', 'OS', 'Processor', 'Ram and Rom', 'Camera Quality', 'Battery', 'Price', 'Overall rating', 'Quantity']
    
    while True:
        choice = int(input("Enter your choice \n1. Add data of new product \n2. Update data of any model \n3. Delete data \n4. Display the available products with specifications \n5. Perform search on products \n6. Quit\n"))
        
        if choice == 1:
            x = []
            print("Data to be entered \n", L)
            for i in range(len(L)):
                x.append(input(f"Enter the value for {L[i]}: "))
            query = "INSERT INTO mobiles (ModelNo, Brand, LaunchDate, OS, Processor, RamRom, CameraQuality, Battery, Price, OverallRating, Quantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            execute_query(connection, query, x)
        
        elif choice == 2:
            print(L)
            field = input("Enter the field to be updated: ")
            model_no = input("Enter the model no in which changes are to be made: ")
            new_value = input("Enter the new value to be replaced: ")
            query = f"UPDATE mobiles SET {field} = %s WHERE ModelNo = %s"
            execute_query(connection, query, (new_value, model_no))
        
        elif choice == 3:
            model_no = input("Enter the model no to be deleted: ")
            query = "DELETE FROM mobiles WHERE ModelNo = %s"
            execute_query(connection, query, (model_no,))
        
        elif choice == 4:
            query = "SELECT * FROM mobiles"
            results = fetch_query(connection, query)
            for i, result in enumerate(results):
                print(f"PRODUCT {i + 1}")
                for j, field in enumerate(L):
                    print(f"{field} = {result[j]}")
        
        elif choice == 5:
            model_no = input("Enter the model no. whose data is to be searched: ")
            sub_choice = int(input("Enter 1 to display all the data, 2 to display data of a particular field: "))
            if sub_choice == 1:
                query = "SELECT * FROM mobiles WHERE ModelNo = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
            elif sub_choice == 2:
                print(L)
                field = input("Enter the field to be displayed: ")
                query = f"SELECT {field} FROM mobiles WHERE ModelNo = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
        
        else:
            break

def customers(connection):
    L = ['Name', 'CustomerID', 'DateOfPurchase', 'ModelNo', 'Discount', 'AmountPaid', 'WarrantyPeriod', 'ContactNo']
    
    while True:
        choice = int(input("Enter your choice \n1. Add data of new customer \n2. Update data of any customer \n3. Delete data \n4. Display the record of customers \n5. Search about customers \n6. Quit\n"))
        
        if choice == 1:
            x = []
            print("Data to be entered \n", L)
            for i in range(len(L)):
                x.append(input(f"Enter the value for {L[i]}: "))
            query = "INSERT INTO record (Name, CustomerID, DateOfPurchase, ModelNo, Discount, AmountPaid, WarrantyPeriod, ContactNo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            execute_query(connection, query, x)
            update_query = "UPDATE mobiles SET Quantity = Quantity - 1 WHERE ModelNo = %s"
            execute_query(connection, update_query, (x[3],))
        
        elif choice == 2:
            print(L)
            field = input("Enter the field to be updated: ")
            customer_id = input("Enter the customer ID in which changes are to be made: ")
            new_value = input("Enter the new value to be replaced: ")
            query = f"UPDATE record SET {field} = %s WHERE CustomerID = %s"
            execute_query(connection, query, (new_value, customer_id))
        
        elif choice == 3:
            customer_id = input("Enter the customer ID to be deleted: ")
            query = "DELETE FROM record WHERE CustomerID = %s"
            execute_query(connection, query, (customer_id,))
        
        elif choice == 4:
            query = "SELECT * FROM record"
            results = fetch_query(connection, query)
            for i, result in enumerate(results):
                print(f"CUSTOMER {i + 1}")
                for j, field in enumerate(L):
                    print(f"{field} = {result[j]}")
        
        elif choice == 5:
            customer_id = input("Enter the customer ID whose data is to be searched: ")
            sub_choice = int(input("Enter 1 to display all the data, 2 to display data of a particular field: "))
            if sub_choice == 1:
                query = "SELECT * FROM record WHERE CustomerID = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
            elif sub_choice == 2:
                print(L)
                field = input("Enter the field to be displayed: ")
                query = f"SELECT {field} FROM record WHERE CustomerID = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
        
        else:
            break

def sales(connection):
    L = ['totalsoldproducts', 'TotalCustomers', 'Date', 'MostSoldModel', 'TotalProfit', 'INCorDEC_per']
    
    while True:
        choice = int(input("Enter your choice \n1. Add new data \n2. Update data of any date \n3. Delete data \n4. Display the daily sales \n5. Search about sales \n6. Quit\n"))
        
        if choice == 1:
            x = []
            print("Data to be entered \n", L)
            for i in range(5):
                x.append(input(f"Enter the value for {L[i]}: "))
            query = "SELECT DATE_ADD(%s, INTERVAL -1 DAY)"
            prev_date = fetch_query(connection, query, (x[2],))[0][0]
            query = "SELECT TotalProfit FROM sale WHERE Date = %s"
            prev_profit = fetch_query(connection, query, (prev_date,))
            if prev_profit:
                prev_profit = prev_profit[0][0]
                difference = int(x[4]) - int(prev_profit)
                if difference > 0:
                    change_percent = (difference / int(prev_profit)) * 100
                    x.append(f"inc{change_percent}")
                elif difference < 0:
                    change_percent = (-difference / int(prev_profit)) * 100
                    x.append(f"dec{change_percent}")
            else:
                x.append(0)
            query = "INSERT INTO sale (totalsoldproducts, TotalCustomers, Date, MostSoldModel, TotalProfit, INCorDEC_per) VALUES (%s, %s, %s, %s, %s, %s)"
            execute_query(connection, query, x)
        
        elif choice == 2:
            print(L)
            field = input("Enter the field to be updated: ")
            date = input("Enter the date whose value is to be changed: ")
            new_value = input("Enter the new value to be replaced: ")
            query = f"UPDATE sale SET {field} = %s WHERE Date = %s"
            execute_query(connection, query, (new_value, date))
        
        elif choice == 3:
            date = input("Enter the date to be deleted: ")
            query = "DELETE FROM sale WHERE Date = %s"
            execute_query(connection, query, (date,))
        
        elif choice == 4:
            query = "SELECT * FROM sale"
            results = fetch_query(connection, query)
            for i, result in enumerate(results):
                print(f"DAY {i + 1}")
                for j, field in enumerate(L):
                    print(f"{field} = {result[j]}")
        
        elif choice == 5:
            date = input("Enter the date whose data is to be searched: ")
            sub_choice = int(input("Enter 1 to display all the data, 2 to display data of a particular field: "))
            if sub_choice == 1:
                query = "SELECT * FROM sale WHERE Date = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
            elif sub_choice == 2:
                print(L)
                field = input("Enter the field to be displayed: ")
                query = f"SELECT {field} FROM sale WHERE Date = %s"
                results = fetch_query(connection, query)
                for result in results:
                    print(result)
        
        else:
            break

def main():
    connection = create_connection()
    if not connection:
        print("Failed to connect to database")
        return
    
    while True:
        choice = int(input("Enter your choice \n1. For the record of products \n2. For the record of customers \n3. For the record of sale \n4. Quit\n"))
        if choice == 1:
            products(connection)
        elif choice == 2:
            customers(connection)
        elif choice == 3:
            sales(connection)
        else:
            print("Goodbye")
            break
    
    close_connection(connection)

if __name__ == "__main__":
    print("WELCOME")
    main()
