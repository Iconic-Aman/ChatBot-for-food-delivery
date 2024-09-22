import mysql.connector
global cnx
cnx = mysql.connector.connect(
        host=  'localhost',
        user='root',
        password= 'mysql.Aman@123',
        database= 'my_food_database'
)
def get_order_status(order_id: int):
    #create a cursor object
    cursor = cnx.cursor()

    #write the sql query
    query = ('SELECT status FROM order_tracking WHERE order_id = %s')

    #execute the query
    cursor.execute(query, (order_id,))

    #fetch the result
    result = cursor.fetchone()

    #close the cursor
    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None
    

def get_next_order_id():
    cursor =  cnx.cursor()

    #below query will give the next order ID
    query = "SELECT max(order_id) FROM orders"
    cursor.execute(query)

    #fetching the result
    result = cursor.fetchone()[0]

    #closing the cursor
    cursor.close()

    #returning the next available id
    if result is None:
        return 1
    else:
        return result + 1

def insert_order_in_db(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        #stored items
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        #commit changes
        cnx.commit()
        cursor.close()
        print('order item insert successfully')

        return 1
    
    except mysql.connector.Error as  err:
        print('error inserting order item', err)

        #rollback change if necessary
        cnx.rollback()
        return -1

    except Exception as e:
        print('an error occured')
        cnx.rollback()
        return -1

        

def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # query to get total price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    #fetching the result
    result = cursor.fetchone()[0]

    cursor.close()
    return result

def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    #inserting the record into the order_tracking table
    insert_query = 'INSERT into order_tracking (order_id, status) VALUES (%s, %s)'
    cursor.execute(insert_query, (order_id, status))

    #commit change
    cnx.commit()
    cursor.close()
    


# def get_order_status(order_id:int):
    

#     try:
#         # Connect to the MySQL server
#         connection = mysql.connector.connect(**db_config)

#         # Create a cursor object to execute queries
#         cursor = connection.cursor()

#         # Define the SQL query to fetch status for the given order_id
#         query = "SELECT status FROM order_tracking WHERE order_id = %s"

#         # Execute the query with the provided order_id
#         cursor.execute(query, (order_id,))

#         # Fetch the result (assuming order_id is a primary key, there should be at most one result)
#         result = cursor.fetchone()

#         if result:
#             order_status = result[0]
#             print(f"Status for order_id {order_id}: {order_status}")
#         else:
#             print(f"No order found with order_id {order_id}")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         # Close the cursor and connection
#         if 'cursor' in locals() and cursor is not None:
#             cursor.close()

#         if 'connection' in locals() and connection.is_connected():
#             connection.close()

# # Example usage:
# order_id_input = input("Enter the order_id: ")
# get_order_status(order_id_input)



