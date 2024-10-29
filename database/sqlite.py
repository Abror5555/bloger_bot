from datetime import datetime
import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    ##################################### FOR USERS ######################################
    
    # Adding user
    def add_user(self, id: int, name: str, phone_number: str = None, bloger_id: int = None, social_media: str = None):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO main_user(id, name, phone_number, bloger_id, created, social_media) VALUES(?, ?, ?, ?, ?, ?)"""
        self.execute(sql, parameters=(id, name, phone_number, bloger_id, current_datetime, social_media), commit=True)

    #Selecting all users
    def select_all_users(self):
        
        sql = """SELECT * FROM main_user"""
        return self.execute(sql, fetchall=True)

    # Get a user
    def select_user(self, **kwargs):
        
        sql = "SELECT * FROM main_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    #Counting users
    def count_users(self):
        
        return self.execute("SELECT COUNT(*) FROM main_user;", fetchone=True)

    #Update user phone_number
    def update_user_phone_number(self, phone_number, id):

        sql = f"""UPDATE main_user SET phone_number=? WHERE id=?"""
        return self.execute(sql, parameters=(phone_number, id), commit=True)
    
    # Update user bloger_id
    def update_user_bloger_id(self, bloger_id, id):
        sql = f"""UPDATE main_user SET bloger_id=? WHERE id=?"""
        return self.execute(sql, parameters=(bloger_id, id), commit=True)

    # Deleting users 
    def delete_users(self):
        self.execute("DELETE FROM main_user WHERE TRUE", commit=True)
        
        
    ##################################### FOR BLOGERS ######################################
    
    # Adding bloger
    def add_bloger(self, name: str):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M')
        sql = """INSERT INTO main_bloger(name, created) VALUES(?, ?)"""
        self.execute(sql, parameters=(name, current_datetime), commit=True)

    #Selecting all blogers
    def select_all_bloger(self):
        
        sql = """SELECT * FROM main_bloger"""
        return self.execute(sql, fetchall=True)

    # Get a bloger
    def select_blog(self, **kwargs):
        
        sql = "SELECT * FROM main_bloger WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    #Counting blogers
    def count_blogers(self):
        
        return self.execute("SELECT COUNT(*) FROM main_bloger;", fetchone=True)

    #Update bloger name
    def update_bloger_name(self, name, id):

        sql = f"""UPDATE main_bloger SET name=? WHERE id=?"""
        return self.execute(sql, parameters=(name, id), commit=True)
    
    
    #Update bloger user
    def update_bloger_user(self, user_id, id):

        sql = f"""UPDATE main_bloger SET user_id=? WHERE id=?"""
        return self.execute(sql, parameters=(user_id, id), commit=True)
    
   
    # Deleting blogers 
    def delete_blogers(self):
        self.execute("DELETE FROM main_bloger WHERE TRUE", commit=True)
        
        
    #Counting users
    def count_users_with_filter(self, **kwargs):
        print(kwargs)
        
        sql = "SELECT COUNT(*) FROM main_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
        
        # return self.execute("SELECT COUNT(*) FROM main_user WHERE bloger_id=?;", parameters=(bloger_id, ), fetchone=True)


def logger(statement):
    print(
f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")