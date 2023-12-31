import pymysql
import base64



def conn():
    try:
        connection_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password123',
        }

        # Connect to MySQL server without specifying a database
        connect = pymysql.connect(**connection_params)
        cursor = connect.cursor()

        # Create the database if it doesn't exist
        database_name = 'Manager'
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        # Switch to the specified database
        cursor.execute(f"USE {database_name}")

    except Exception as e:
        print(e)
        return None

    return connect
def reset():
    connect = conn()
    cursor = connect.cursor()
    print("Resetting Database")
    
    print("Warning: This will delete all your data")
    print("Press y to continue any other key to exit")
    if input() != "y":
        print("Going back to the main menu")
        return
    # Delete all entries from Accounts table
    cursor.execute("DELETE FROM Accounts;")
    
    # Delete all entries from Master table
    cursor.execute("DELETE FROM Master;")
    
    # Delete all entries from SecretKey table
    cursor.execute("DELETE FROM SecretKey;")

    connect.commit()
    
def create_table():
    connect = conn()
    cursor = connect.cursor()

    # Create Accounts table
    create_accounts_table = """ CREATE TABLE IF NOT EXISTS Accounts (
        Password VARCHAR(255) PRIMARY KEY,
        Email BLOB NOT NULL,
        Username BLOB NOT NULL,
        Url BLOB,
        Service TEXT NOT NULL,
        tag VARCHAR(255) NOT NULL
    ); """
    cursor.execute(create_accounts_table)

    # Create Master table
    create_master_table = """ CREATE TABLE IF NOT EXISTS Master (
        MasterHash VARCHAR(64) PRIMARY KEY
    ); """
    cursor.execute(create_master_table)

    # Create Key table
    create_key_table = """ CREATE TABLE IF NOT EXISTS SecretKey ( `Key` VARCHAR(512) PRIMARY KEY ); """

    cursor.execute(create_key_table)

    connect.commit()

def fetch_master_hash():
    connect = conn()
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT MasterHash FROM Master;")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(e)
        return None
    finally:
        connect.close()
def fetch_secret_key():
    connect = conn()
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT `Key` FROM SecretKey;")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(e)
        return None
    finally:
        cursor.close()
        connect.close()

def store_master_hash(master_hash):
    connect = conn()
    cursor = connect.cursor()
    insert_command = """INSERT INTO Master (MasterHash) VALUES (%s);"""
    data_to_insert = (master_hash,)
    cursor.execute(insert_command, data_to_insert)
    connect.commit()

def store_secret_key(secret_key):
    connect = conn()
    cursor = connect.cursor()
    try:
        # Explicitly encode the key before storing
        
        insert_command = """INSERT INTO SecretKey (`Key`) VALUES (%s);"""
        data_to_insert = (secret_key,)
        cursor.execute(insert_command, data_to_insert)
        connect.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connect.close()


def store_password(password, email, username, siteurl, service,tag):
    connect = conn()
    cursor = connect.cursor()
    insertCommand = """INSERT INTO Accounts (Password, Email, Username, Url, Service,tag) VALUES (%s, %s, %s, %s, %s,%s);"""
    dataToInsert = (password, email, username, siteurl, service,tag)
    cursor.execute(insertCommand, dataToInsert)
    connect.commit()

def find_password(serviceName):
    connect = conn()
    cursor = connect.cursor()
    search = "SELECT * FROM Accounts WHERE Service LIKE %s"
    cursor.execute(search, ('%' + serviceName + '%',))
    results = cursor.fetchall()
    connect.commit()
    if not results:
        return ""
    passw = results[0][0]
    tag=results[0][5]
    
    return passw,tag

def find_using_email(email):
    connect = conn()
    cursor = connect.cursor()
    search = 'SELECT * FROM Accounts WHERE Email = %s'
    cursor.execute(search, (email,))
    results = cursor.fetchall()
    connect.commit()
    return results

     