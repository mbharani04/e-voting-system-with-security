import oracledb
import properties
#BS Code developed by Mullaivendha K
class dbUtils:
    def get_connection(self): #Create connection to the database and return
        try:
            self.connection = oracledb.connect(
                user=properties.DB_USER,
                password=properties.DB_PASS,
                dsn=properties.DSN
            )
            self.cursor = self.connection.cursor()
            return self.connection, self.cursor
        
        except oracledb.Error as e:
            error_obj, = e.args
            messagebox.showerror(
                "Database Error",
                f"Oracle Error {error_obj.code}\n{error_obj.message}"
            )
            return None,None
    #Method to close the connection
    def close_connection(self):
        if 'cursor' in locals():
            self.cursor.close()
        if 'connection' in locals():
            self.connection.close()
