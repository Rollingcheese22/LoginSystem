from contextlib import closing
import subprocess # Improtant here this is so we
import sqlite3
import hashlib
import uuid
import hmac
import ast
import os


Front_End_Process = subprocess.Popen(["python", "front_end.py"],
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True,)


establish_connection = sqlite3.connect("Users.db")
tool_entry = establish_connection.cursor()
tool_entry.execute('''CREATE TABLE IF NOT EXISTS Users (
user_id varchar(255) NOT NULL,
username TEXT UNIQUE PRIMARY KEY NOT NULL,
password BLOB NOT NULL,
salt BLOB NOT NULL);''')
establish_connection.commit()
establish_connection.close()

def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)
    incoming = password.encode('utf-8')
    incoming_hash = hashlib.scrypt(
        password=incoming,
        salt=salt,
        n=65536,
        r=8,
        p=1,
        maxmem= 1024 * 1024 * 128

    )
    return incoming_hash, salt


def create(username: str,
           password: str): #Create user account
    with closing(sqlite3.connect("Users.db")) as tool:
        with tool:
            search = tool.execute('''SELECT username from Users 
                                         WHERE username = ? COLLATE NOCASE''',
                                  (username,))
            already_exists = search.fetchone()
            if already_exists:
                return "ERROR: USER_ALREADY_EXISTS"
            else:
                hash_format = hash_password(password)
                password = hash_format[0]
                user_salt = hash_format[1]
                user_id = str(uuid.uuid4())
                tool.execute('''INSERT INTO Users 
                             (username, password, salt, user_id) VALUES 
                             (?, ?, ?, ?)''',
                             (username, password, user_salt, user_id)
                             )
            return "ACCOUNT_CREATED"

def login(username: str,
          password: str):
    with closing(sqlite3.connect("Users.db")) as tool:
        with tool:
            account = tool.execute('''SELECT * from Users 
                                        WHERE username = ?''', (username,))
            exists = account.fetchone()
            if exists:
                incoming = password.encode('utf-8')
                current_salt = exists[3]
                current_password = exists[2]
                inbound: bytes = hashlib.scrypt(
                    password=incoming,
                    salt=current_salt,
                    n=65536,
                    r=8,
                    p=1,
                    maxmem= 1024 * 1024 * 128,
                )
                if hmac.compare_digest(current_password, inbound):
                    return "LOGGED_IN"
                else:
                    return "Incorrect Password or Username"
            else:
                return "Incorrect Password or Username"


exit_code = Front_End_Process.returncode
with Front_End_Process.stdout as signal:
    with signal:
        for messages in signal:
            if messages.rstrip():
                message = ast.literal_eval(messages.rstrip())
                if message[0] == "REQUEST: Account":
                    user_setup = message
                    if create(user_setup[1], user_setup[2]) != "ACCOUNT_CREATED":
                        Front_End_Process.stdin.write("ERROR: Account_Exists\n")
                        Front_End_Process.stdin.flush()
                        print("ERROR: Account_Exists")
                    else:
                        Front_End_Process.stdin.write("ACCOUNT_CREATED\n")
                        Front_End_Process.stdin.flush()
                        print("SUCCESS")
                else:
                    print("BAD")



if exit_code:
    print("Failure Occurred")
else:
    print("User Exited.")