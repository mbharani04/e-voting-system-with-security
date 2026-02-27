import customtkinter as ctk
import tkinter.messagebox as messagebox
import oracledb

DB_USER = "voting_schema"
DB_PASS = "voting123"
DSN = "localhost:1521/XEPDB1"

ctk.set_appearance_mode("DARK")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("E-Voting System - Voter Login")
        self.geometry("700x700")
        self.resizable(False, False)
        
        # CORRECTED: Main root window has no '.parent'. 
        # We define the font directly on 'self'.
        self.name_font = ctk.CTkFont(family="Helvetica", size=12)
        self.login_page()

    # ================= DATABASE CONNECTION FUNCTION =================
    # Indented to be a method of App
    def get_connection(self):
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

    # ============= login PAGE =====================
    def login_page(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        loginheader = ctk.CTkLabel(self.login_frame, text="LOGIN",
                                   font=ctk.CTkFont(family="Times New Roman", size=35, weight="bold"))
        loginheader.grid(row=0, column=0, columnspan=2, pady=30)

        # Name
        ctk.CTkLabel(self.login_frame, text="Name:", font=self.name_font).grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.usernameEntry = ctk.CTkEntry(self.login_frame, width=250, placeholder_text="enter username", font=self.name_font)
        self.usernameEntry.grid(row=1, column=1, padx=20, pady=10)

        # Password 
        ctk.CTkLabel(self.login_frame, text="Password:", font=self.name_font).grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.passwordEntry = ctk.CTkEntry(self.login_frame, show="*", width=250, placeholder_text="password", font=self.name_font)
        self.passwordEntry.grid(row=2, column=1, padx=20, pady=10)

        # Login button
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=150, font=self.name_font, command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=25)

    def login(self):
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        if username == "admin": 
            self.login_frame.destroy()
            admin_page(self)
        else:
            connection = self.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                        SELECT user_name FROM v_user_detail 
                        WHERE user_name = :uname AND password = :pwd
                    """, {"uname": username, "pwd": password})

                    if cursor.fetchone():
                        self.login_frame.destroy()
                        messagebox.showinfo("Success", "Voter Login Successful")
                    else:
                        messagebox.showerror("Login Failed", "Invalid Username or Password")
                finally:
                    connection.close()

# -------------------------------- ADMIN PAGE CLASS --------------------------------#
class admin_page:
    def __init__(self, parent):
        self.parent = parent
        # Main Frame setup
        self.admin_frame = ctk.CTkFrame(parent, width=850, height=850)
        self.admin_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Grid Configuration to control spacing
        self.admin_frame.columnconfigure((0, 1), weight=1)

        # --- TOP CENTRE: Parties + Vote Counts ---
        # Party 1
        ctk.CTkLabel(self.admin_frame, text="Party 1:", font=self.parent.name_font).grid(row=0, column=0, padx=20, pady=10, sticky="e")
        self.count_1 = ctk.CTkLabel(self.admin_frame, text="0", fg_color="gray30", width=300, corner_radius=6)
        self.count_1.grid(row=0, column=1, padx=10, pady=10, sticky="sw")

        # Party 2
        ctk.CTkLabel(self.admin_frame, text="Party 2:", font=self.parent.name_font).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.count_2 = ctk.CTkLabel(self.admin_frame, text="0", fg_color="gray30", width=300, corner_radius=6)
        self.count_2.grid(row=1, column=1, padx=10, pady=10, sticky="sw")

        # Party 3
        ctk.CTkLabel(self.admin_frame, text="Party 3:", font=self.parent.name_font).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        self.count_3 = ctk.CTkLabel(self.admin_frame, text="0", fg_color="gray30", width=300, corner_radius=6)
        self.count_3.grid(row=2, column=1, padx=10, pady=10, sticky="sw")

        # --- MID CENTRE: Result Button ---
        self.result_btn = ctk.CTkButton(self.admin_frame, text="RESULT", command=self.result, 
                                        fg_color="green", hover_color="darkgreen", width=100, height=30)
        self.result_btn.grid(row=3, column=0, columnspan=2, pady=50)

        # --- FOOTER: Back (Left) and Others (Right) ---
        back_btn = ctk.CTkButton(self.admin_frame, text="Back", width=100, command=self.go_back)
        back_btn.grid(row=4, column=0, padx=20, pady=20, sticky="sw")

        others_btn = ctk.CTkButton(self.admin_frame, text="Others", width=100, command=self.others)
        others_btn.grid(row=4, column=1, padx=20, pady=20, sticky="se")

    def result(self):
        # Placeholder logic to update counts
        self.count_1.configure(text="")
        self.count_2.configure(text="")
        self.count_3.configure(text="")
        print("Results Published")

    def others(self):
        print("Redirecting to other settings...")

    def go_back(self):
        self.admin_frame.destroy()
        self.parent.login_page()

if __name__ == "__main__":
    app = App()
    app.mainloop()
