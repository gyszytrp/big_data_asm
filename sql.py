import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database
    '''

    # Get the database running
    def __init__(self, database_arg="./temp3.db"):
        self.conn = sqlite3.connect(database_arg,check_same_thread=False)
        self.cur = self.conn.cursor()


    # # SQLite 3 does not natively support multiple commands in a single statement
    # # Using this handler restores this functionality
    # # This only returns the output of the last command
    # def execute(self, sql_string):
    #     out = None
    #     for string in sql_string.split(";"):
    #         try:
    #             out = self.cur.execute(string)
    #         except:
    #             pass
    #     return out



    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self):

        # Clear the database if needed
        self.cur.execute("DROP TABLE IF EXISTS tweet")
        self.conn.commit()

        # Create the users table
        # self.cur.execute("""CREATE TABLE tweet(
        #     id TEXT,
        #     time TEXT,
        #     fulltext TEXT,
        #     hashtags TEXT,
        #     retweet_count INTEGER,
        #     favorite_count INTEGER,
        #     reply_count INTEGER,
        #     quote_count INTEGER,
        #     user_id TEXT,
        #     raw_data TEXT
        # )""")

        # self.conn.commit()

        self.cur.execute("""CREATE TABLE User(
            username TEXT,
            password TEXT
        )""")

        self.conn.commit()

        self.cur.execute("""CREATE TABLE Sessions(
            session_id TEXT,
            username TEXT,
            expiry_time TEXT
        )""")

        self.conn.commit()









    # # Add a user to the database
    def add_u(self,username,password):

        query = "INSERT INTO User (username, password) VALUES (?, ?)"

        # Execute the query with user input as a parameter

        self.cur.execute(query, (username,password,))
        self.conn.commit()


        return True







    # Check login credentials
    def get_u(self,username,password):

        query = "SELECT * FROM User where username=? and password=?"

        self.cur.execute(query,(username,password,))

        # If our query returns
        line=self.cur.fetchone()
        # print(line)
        if line:
            return line
        else:
            return False





    def add_session(self,session_id,username,expiry_time):

        query = "INSERT INTO Sessions (session_id,username,expiry_time) VALUES (?, ?, ?)"

        # print(sql_cmd)
        self.cur.execute(query, (session_id,username,expiry_time,))
        self.conn.commit()

        return True




    def retrieve_session_data(self,session_id):
        # Query the session data store to retrieve the session data associated with the session ID
        query= "SELECT * FROM Sessions WHERE session_id = ? "
        self.cur.execute(query,(session_id,))
        row = self.cur.fetchone()
        if row:
            # If the session data exists, return it as a dictionary
            session_data = {
                'session_id': row[0],
                'username': row[1],
                'expiry_time': row[2]
            }

            print(row)

            return session_data
        else:
            # If the session data does not exist, return None
            return None
    


    def remove_session_data_by_session_id(self,session_id):
        self.cur.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))

        # Commit the changes to the database and close the connection
        self.conn.commit()

    def remove_session_data_by_username(self,username):
        self.cur.execute("DELETE FROM sessions WHERE username=?", (username,))

        # Commit the changes to the database and close the connection
        self.conn.commit()

    def update_session_data(self,session_id, session_data):

        self.cur.execute('UPDATE sessions SET username = ?, expiry_time = ? WHERE session_id = ?',(session_data['username'], session_data['expiry_time'], session_id,))
        self.conn.commit()









