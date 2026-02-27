import oracledb

DB_USER = "voting_schema"
DB_PASS = "voting123"
DSN = "localhost:1521/XEPDB1"    

voter_n = [
    "Arjun Kumar",
    "Priya Sharma",
    "Rahul Verma",
    "Sneha Reddy",
    "Karthik Raj",
    "Divya Lakshmi",
    "Vikram Singh",
    "Meena Krishnan",
    "Suresh Babu",
    "Anitha Devi",
    "Rohan Patel",
    "Aishwarya Nair",
    "Manoj Kumar",
    "Pooja Gupta",
    "Harish Kumar",
    "Deepika Iyer",
    "Naveen Kumar",
    "Swathi Menon",
    "Ajay Prakash",
    "Lakshmi Narayanan"
]


def get_connection():
    try:
        connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASS,
        dsn=DSN
        )
        return connection
    except oracledb.Error as e:
        messagebox.showerror("Database Error", f"Cannot connect to Oracle: {str(e)}")
        return None
        
        
if __name__ == "__main__":
    con = get_connection()
    if con:
        try:
            cursor = con.cursor()
            for i in range (1,21):
                cursor.execute("""
                    INSERT INTO v_voterid_stored_data 
                    (voter_id, voter_name, booth_name, pincode)
                    VALUES (:vid, :vname, :bname, :pin)
                """, {
                    "vid": "RSA000"+str(i),
                    "vname": voter_n[0],
                    "bname": "Chennai",
                    "pin": "600078"
            })
            
            con.commit()