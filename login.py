import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import oracledb

# ================= DATABASE CONFIG =================
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
        
        self.voter_ids = ["VOTER001", "VOTER002", "VOTER003"]
        self.login_page()
        

        
       # ============= login PAGE =====================
    def login_page(self):
        self.login_frame =ctk.CTkFrame(self)
        self.login_frame.place(relx=0.5,rely=0.5,anchor="center")

#user login title

        loginheader= ctk.CTkLabel(self.login_frame,text="LOGIN",
                                 font=ctk.CTkFont(family="Times and roman",size=35,weight="bold"))
        loginheader.grid(row=0, column=0, columnspan=2, pady=30)

        self.name_font= ctk.CTkFont(family="Helvetica", size=12)
#username Label
        self.usernamelabel=ctk.CTkLabel( self.login_frame,text="Name:",font=self.name_font)
        self.usernamelabel.grid(row=1,column=0,padx=10, pady=20, sticky="e")
    
#username Entry
        self.usernameEntry =ctk.CTkEntry(self.login_frame,width =250,placeholder_text= "enter username", font=self.name_font)
        self.usernameEntry.grid(row=1, column=1, padx=20, pady=10)

#password Label
        self.passwordlabel=ctk.CTkLabel( self.login_frame,text="Password:",font=self.name_font)
        self.passwordlabel.grid(row=2,column=0,padx=10, pady=20, sticky="e")
       
#password Entry
        self.passwordEntry =ctk.CTkEntry(self.login_frame,show="*",width =250,placeholder_text="password",font=self.name_font)
        self.passwordEntry.grid(row=2, column=1, padx=20, pady=10)

#login button
        self.login_button=ctk.CTkButton( self.login_frame, text="Login",width=150,font=self.name_font,
            command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=25)

    def login(self):    
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()

        
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            connection = oracledb.connect(
                user=DB_USER,
                password=DB_PASS,
                dsn=DSN
            )

            cursor = connection.cursor()

            cursor.execute("""
                SELECT user_name
                FROM v_user_detail
                WHERE user_name = :uname
                  AND password = :pwd
            """, {
                "uname": username,
                "pwd": password
            })

            result = cursor.fetchone()

            if result:
                cursor.execute("""
                    UPDATE v_user_detail
                    SET last_login = SYSTIMESTAMP
                    WHERE user_name = :uname
                """, {"uname": username})

                connection.commit()

                messagebox.showinfo("Success", "Login Successful")
                self.voter_status_page()
            else:
                messagebox.showerror("Login Failed", "Invalid Username or Password")

        except oracledb.Error as e:
            error_obj, = e.args
            messagebox.showerror(
                "Database Error",
                f"Oracle Error {error_obj.code}\n{error_obj.message}"
            )

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()


        # ============= VOTER STATUS PAGE =====================

    def voter_status_page(self):
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.place(relx=0.5, rely=0.5, anchor="center")

       # voter status Title
        title = ctk.CTkLabel(self.status_frame, text="VOTER STATUS",
            font=ctk.CTkFont(family="Times and roman",size=30, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Voter ID Label
        self.voterid_label = ctk.CTkLabel(self.status_frame, text="Select Voter ID:")
        self.voterid_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        #voter ID Entry
        self.voterid_Entry=ctk.CTkEntry(self.status_frame,width =250,placeholder_text= "voterID code", font=self.name_font)
        self.voterid_Entry.grid(row=1, column=1, padx=20, pady=10)

        # Search Button
        search_btn = ctk.CTkButton(self.status_frame,text="Search",command=self.user_search)
        search_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # status Display
        self.result_label = ctk.CTkLabel(self.status_frame,text="",
            font=ctk.CTkFont(size=14))
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        # back button
        back_btn = ctk.CTkButton(self.status_frame,text="Back",command=self.back_to_login)
        back_btn.grid(row=5, column=0,padx=30,pady=15)

        #qr label

        self.qr_label = ctk.CTkLabel(self.status_frame,text="QR Code will be displayed here",width=300,height=200)
        self.qr_label.grid(row=4, column=0, columnspan=2, pady=15)

        self.qr_button =ctk.CTkButton(self.qr_frame,text="Generate QR Code",command=self.generate_qr)
        self.qr_button.grid(row=5, column=1, pady=20)
        
    def user_search(self):
        selected_id = self.voterid_entry.get()

        
        if not selected_id:
            messagebox.showerror("Error", "Enter Voter ID")
            return

        if selected_id in self.voter_ids:
            status = "ELIGIBLE"
     
        else:
            status = "NOT ELIGIBLE"

        self.result_label.configure(
            text=f"Voter ID : {selected_id}\n"
                 f"Status   : {status}"
        )
    def generate_qr(self):
        self.qr_label.configure(text="QR CODE GENERATED\n(Voter Verification)")
        messagebox.showinfo("QR Code", "QR Code generated successfully")
     

    def back_to_login(self):
         self.status_frame.destroy()
         self.login_page()
        



if __name__ == "__main__":
    app = App()
    app.mainloop()
