import sqlite3
from sqlite3 import Error
import socket


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        return conn
    except Error as e:
        print(e)

    return None


def query_with_string(conn, query):
    cur = conn.cursor()
    result = ""
    try:
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            tempStr = ''.join(str(row))
            result = result + "\n" + tempStr
        return result
    except:
        result = "error"
        return result


def create_connection_to_db():
    database = "ServerDB.db"
    # create a database connection
    conn = create_connection(database)
    return conn


def server_func(db_conn):
    # get the localHost
    host = '127.0.0.1'
    port = 5000  # initialize port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    server_socket.bind((host, port))  # bind host address and port together

    # Start to listen port which bind before
    server_socket.listen(2)
    connection = False
    while True:
        if (connection == False):
            conn, address = server_socket.accept()  # accept connection from Client
            print("Connection from: " + str(address))
            connection = True

        # receive the SQL Query Text
        query_text = conn.recv(1024).decode()
        if not query_text:
            # if data is not received break
            break

        if query_text == 'exit':
            conn.send("ok".encode())
            conn.close()
            conn = None
            connection = False
            continue

        # Send query to Db and take result
        query_result = query_with_string(db_conn, query_text)
        query_result_str = ''.join(query_result)
        # Send query result to Client
        conn.send(query_result.encode())
    conn.close()  # close the connection


def main():
    # create a database connection
    conn = create_connection_to_db()

    # Server start
    server_func(conn)


if __name__ == '__main__':
    main()
