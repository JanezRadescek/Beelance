from models.database import db
import mysql.connector

def set_user(username, password, salt, mail_verified, full_name, company, email, 
        street_address, city, state, postal_code, country):
    """
    Register a new user in the database
        :param username: The users unique user name
        :param password: The password
        :param full_name: The users full name
        :param company: The company the user represents
        :param email: The users email address
        :param street_address: The street address of the user
        :param city: The city where the user lives
        :param state: The state where the user lives
        :param postal_code: The corresponding postal code
        :param country: The users country
        :type username: str
        :type password: str
        :type full_name: str
        :type company: str
        :type email: str
        :type street_address: str
        :type city: str
        :type state: str
        :type postal_code: str
        :type country: str
    """
    db.connect()
    cursor = db.cursor()
    try:
        cursor.execute("""INSERT INTO users (userid, username, password, salt, mail_verified, temp_password, anti_csrf, full_name, company, email, street_address, city, state, postal_code, country, bad_login, last_login) VALUES (NULL, %(username)s, 
             %(password)s , %(salt)s, %(mail_verified)s, %(temp_password)s, %(anti_csrf)s, %(full_name)s , %(company)s ,
             %(email)s, %(street_address)s, %(city)s,
             %(state)s , %(postal_code)s ,%(country)s,
             0, UNIX_TIMESTAMP() )""",
                       {'username': username, 'password': password, 'salt': salt, 'mail_verified': mail_verified,
                        'temp_password': password, 'anti_csrf':"123", 'full_name': full_name , 'company': company ,
                        'email': email, 'street_address': street_address, 'city': city,
                        'state':state , 'postal_code': postal_code ,'country': country})
        db.commit()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        cursor.fetchall()
        exit(1)
    finally:
        cursor.close()
        db.close()
