from models.database import db
import mysql.connector
import datetime
from datetime import datetime

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        users = []
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()
    
    userid = None
    try:
        cursor.execute("""SELECT userid from users WHERE username = %(username)s""", {'username': username})
        users = cursor.fetchall()
        if(len(users)):
            userid = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor()
    username = None
    try:
        cursor.execute("""SELECT username from users WHERE userid =%(userid)s""", {'userid': userid})
        users = cursor.fetchall()
        if len(users):
            username = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return username

def get_salt(username):
    "get salt for pasword"
    db.connect()
    cursor = db.cursor()
    salt = "123"
    try:
        cursor.execute("""SELECT userid, salt from users where username =%(username)s""",
         {'username': username})
        salts = cursor.fetchall()
        if len(salts):
            salt = salts[0][1]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return salt

def set_anti_csrf(username, anti_csrf):
    "set anti_csrf"
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET anti_csrf = %(anti_csrf)s WHERE username =%(username)s""",
        {'anti_csrf' : anti_csrf, 'username': username})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_anti_csrf(username):
    "set anti_csrf"
    db.connect()
    cursor = db.cursor()
    anti_csrf = "false"
    try:
        cursor.execute("""SELECT username, anti_csrf FROM users WHERE username =%(username)s""",
        {'username': username})
        anti_csrf = cursor.fetchall()
        return anti_csrf[0][1]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return anti_csrf

def match_user(username, password):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    db.connect()
    cursor = db.cursor()
    user = None
    try:
        cursor.execute("""SELECT userid, username, mail_verified from users where username =%(username)s and password =%(password)s""", {'username': username, 'password': password})
        users = cursor.fetchall()
        if len(users):
            user = users[0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user

def validate_mail(username, mail_verified):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT username, mail_verified from users where username =%(username)s and mail_verified =%(mail_verified)s""",
         {'username': username, 'mail_verified': mail_verified})
        users = cursor.fetchall()
        if len(users):
            cursor.execute("""UPDATE users SET mail_verified = %(true)s WHERE username =%(username)s""", {'username': username, 'true' : "true"})
            db.commit()
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return False   

def set_temp_password(username, mail, temp):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT username from users where username =%(username)s and email =%(mail)s""",
         {'username': username, 'mail': mail})
        users = cursor.fetchall()
        if len(users):
            cursor.execute("""UPDATE users SET temp_password = %(temp)s WHERE username =%(username)s""",
            {'temp' : temp, 'username': username})
            db.commit()
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return False   

def change_password(username, temp, new):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""SELECT username from users where username =%(username)s and temp_password =%(temp)s""",
         {'username': username, 'temp': temp})
        users = cursor.fetchall()
        if len(users):
            cursor.execute("""UPDATE users SET password = %(new)s, temp_password=%(new_temp)s WHERE username =%(username)s""",
            {'new' : new,'new_temp' : new, 'username': username})
            db.commit()
            return True
        else:
            return False 
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return False            

def get_twoauth_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()

    twoauth = ""
    try:
        cursor.execute("""SELECT twoauth from users WHERE username =%(username)s""", {'username': username})
        users = cursor.fetchall()
        if(len(users)):
            twoauth = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return twoauth

def insert_twoauth_by_name(username, twoauth):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET twoauth=%(twoauth)s WHERE username =%(username)s""", {'username': username, 'twoauth': twoauth})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def get_bad_login_by_name(username):
    """
    Get the number of bad logins of the unique username
        :param username: Name of the user
        :return: The number of bad logins of the user
    """
    db.connect()
    cursor = db.cursor()

    bad_login = None
    try:
        cursor.execute("""SELECT bad_login from users WHERE username= %(username)s""", {'username': username})
        users = cursor.fetchall()
        if(len(users)):
            bad_login = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return bad_login

def get_last_login_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()

    last_login = 0
    try:
        cursor.execute("""SELECT last_login from users WHERE username= %(username)s""", {'username': username})
        users = cursor.fetchall()
        if(len(users)):
            last_login = users[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
    return last_login

def update_login_info_by_username(username):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET bad_login=0, last_login = UNIX_TIMESTAMP() WHERE username= %(username)s""", {'username': username})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def increment_bad_login_by_username(username):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET bad_login = bad_login +1 WHERE username = %(username)s""", {'username': username})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def reset_bad_login_by_username(username):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET bad_login = 0 WHERE username = %(username)s""", {'username': username})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()

def update_last_login_by_username(username):
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""UPDATE users SET last_login = UNIX_TIMESTAMP() WHERE username= %(username)s""", {'username': username})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
