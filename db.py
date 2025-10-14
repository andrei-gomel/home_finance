import pymysql
from config import host, user, password, db_name

flag_connection = False

def connection_db():
    global flag_connection
    global connection
    if flag_connection == False:
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor)
            print("Successfuly connected to database...")
            flag_connection = True
        except Exception as e:
            print(f"Connection error: {e.args[1]}")
            exit()
    return connection
    

def get_categories():
    connection = connection_db()
    all_data = {'accordance':{}, 'names':[]}
    # try:   
    with connection.cursor() as cursor:
        select_all_query = "SELECT * FROM `categories`"
        cursor.execute(select_all_query)
        result = cursor.fetchall()
        for x in result:
            all_data['accordance'].update({x["name"]:x["id"]})
            all_data['names'].append(x["name"])
    # finally:
    #     connection.close()
    return all_data


def insert_new_payment(insert_data):
    connection = connection_db()
    # try:        
    #     with connection.cursor() as cursor:
    #         insert_query = "INSERT INTO `payment` (category_id, data, price) VALUES (%s, %s, %s)"
    #         cursor.execute(insert_query, insert_data)
    #         connection.commit()
    #         print(cursor.rowcount, "was inserted.")
    # finally:
    #     connection.close()
    success = False
    with connection.cursor() as cursor:
        insert_query = "INSERT INTO `payment` (category_id, data, price) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, insert_data)
        connection.commit()
        print(cursor.rowcount, "was inserted.")
        success = True
    return success


def get_list_payments():
    connection = connection_db()
    with connection.cursor() as cursor:
        select_list_payments = """
                            SELECT payment.id, data, price, categories.name 
                            FROM `payment` 
                            JOIN categories 
                            ON payment.category_id=categories.id
                            ORDER BY payment.id ASC
        """
        cursor.execute(select_list_payments)
        result = cursor.fetchall()
    return result


def select_one(id):
    with connection.cursor() as cursor:
            select_one_query = """
                    SELECT payment.id, payment.data, payment.price, categories.name 
                    FROM `payment` JOIN `categories` 
                    ON payment.category_id=categories.id 
                    WHERE payment.id=%s
                    """
            cursor.execute(select_one_query, (id,))
            # cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            # print(result)
            # print('#' * 20)
    # try:        
    #     with connection.cursor() as cursor:
    #         select_one_query = "SELECT * FROM `users` WHERE `id`=%s"
    #         cursor.execute(select_one_query, (id,))
    #         result = cursor.fetchone()
    #         print(result)
    #         print('#' * 20)        
    # finally:
    #     connection.close()
    return result
        

def get_total_sum():
    connection = connection_db()
    with connection.cursor() as cursor:
        query = "SELECT SUM(price) AS Total FROM `payment`"
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def get_most_rich_item():
    connection = connection_db()
    with connection.cursor() as cursor:
        query = """SELECT SUM(`price`) AS total, categories.name 
                    FROM `payment` JOIN categories 
                    ON payment.category_id=categories.id 
                    GROUP BY categories.name 
                    ORDER BY total DESC LIMIT 1
    """
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def get_most_popular_item():
    connection = connection_db()
    with connection.cursor() as cursor:
        query = """SELECT COUNT(categories.name) AS total, categories.name 
                    FROM `payment` JOIN categories 
                    ON payment.category_id=categories.id 
                    GROUP BY categories.name ORDER BY `total` DESC LIMIT 1
    """
        cursor.execute(query)
        result = cursor.fetchone()
    return result