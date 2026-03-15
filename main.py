import customtkinter as ctk
import tkinter.messagebox as messagebox
import oracledb
import qrcode
from PIL import Image
import os
import properties
import access
import qrGeneratorService

ctk.set_appearance_mode("DARK")      
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("E-Voting System - Voter Login")   
        self.geometry("700x700")
        self.resizable(False, False)
        
        # Define shared fonts here so other classes can see them
        self.name_font = ctk.CTkFont(family="Helvetica", size=12)
        
        self.login_page()

    def login_page(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        loginheader = ctk.CTkLabel(self.login_frame, text="LOGIN",
                                   font=ctk.CTkFont(family="Times New Roman", size=35, weight="bold"))
        loginheader.grid(row=0, column=0, columnspan=2, pady=30)
        
        # Name
        ctk.CTkLabel(self.login_frame, text="Name:", font=self.name_font).grid(row=1, column=0, padx=10, pady=20, sticky="e")
        self.usernameEntry = ctk.CTkEntry(self.login_frame, width=250, placeholder_text="enter username")
        self.usernameEntry.grid(row=1, column=1, padx=20, pady=10)

        # Password
        ctk.CTkLabel(self.login_frame, text="Password:", font=self.name_font).grid(row=2, column=0, padx=10, pady=20, sticky="e")
        self.passwordEntry = ctk.CTkEntry(self.login_frame, show="*", width=250, placeholder_text="password")
        self.passwordEntry.grid(row=2, column=1, padx=20, pady=10)

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=150, command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=25)

    def login(self):    
        username = self.usernameEntry.get().strip()
        password = self.passwordEntry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        connection,cursor = access.dbUtils.get_connection(self)
        cursor.execute(properties.get_user, {
            "uname": username,
            "pwd": password
        })

        result = cursor.fetchone()

        if result:
            cursor.execute(properties.update_user_lastlogin, {"uname": username})
            connection.commit()
            # messagebox.showinfo("Success", "Login Successful")
            # self.voter_status_page()
            v_voter_status(self) # Correct way to switch classes
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

        access.dbUtils.close_connection(self)

# ================= VOTER STATUS PAGE CLASS =================
class v_voter_status:  
    def __init__(self, parent):
        self.parent = parent
        self.status_frame = ctk.CTkFrame(parent)
        self.status_frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(self.status_frame, text="VOTER STATUS",
                             font=ctk.CTkFont(family="Times New Roman", size=30, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Voter ID Entry
        ctk.CTkLabel(self.status_frame, text="Enter Voter ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.voterid_Entry = ctk.CTkEntry(self.status_frame, width=250)
        self.voterid_Entry.grid(row=1, column=1, padx=20, pady=10)

        # Buttons
        self.search_btn = ctk.CTkButton(self.status_frame, text="Search", command=self.user_search)
        self.search_btn.grid(row=2, column=0, pady=15)

        self.reset_btn = ctk.CTkButton(self.status_frame, text="Reset", fg_color="gray", command=self.reset_fields)
        self.reset_btn.grid(row=2, column=1, pady=15)

        self.result_label = ctk.CTkLabel(self.status_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.qr_label = ctk.CTkLabel(self.status_frame, text="QR Code Area", width=200, height=200, fg_color="gray20")
        self.qr_label.grid(row=4, column=0, columnspan=2, pady=15)
            
        self.Gqr_btn = ctk.CTkButton(self.status_frame, text="Generate QR", state="disabled", command=self.generate_qr)
        self.Gqr_btn.grid(row=5, column=0, columnspan=2, pady=10)
                                    
        self.back_btn = ctk.CTkButton(self.status_frame, text="Logout", command=self.back_to_login)
        self.back_btn.grid(row=6, column=0, columnspan=2, pady=15)

    def reset_fields(self):
        self.voterid_Entry.delete(0, 'end')
        self.result_label.configure(text="", text_color="white")
        self.qr_label.configure(image="", text="QR Code Area")
        self.Gqr_btn.configure(state="disabled")

    def user_search(self):
        
        self.voter_id = self.voterid_Entry.get().strip().upper()
        if not self.voter_id:
            messagebox.showerror("Error", "Enter Voter ID")
            return
        else:
            connection,cursor = access.dbUtils.get_connection(self)
            cursor.execute(properties.get_voter_details, {"voterId": self.voter_id
        })
        result = cursor.fetchone()
        print(result)
        if result:
            print("there is result")
            if result[3] == 'Y':
                print("value is Y")
                self.result_label.configure(text="Already Polled", text_color="#E74C3C")
                self.Gqr_btn.configure(state="disabled")
            else:
                print("go a head")
                self.result_label.configure(text=f"NAME: {result[1]}\nBooth: {result[2]}\nSTATUS: ELIGIBLE", text_color="#2ECC71")
                self.Gqr_btn.configure(state="normal")    
        else:
            print("no result")
            self.result_label.configure(text="Voter Not Found", text_color="#E74C3C")
            self.Gqr_btn.configure(state="disabled")

    def generate_qr(self):
        voter_id = self.voterid_Entry.get().strip().upper()
        file_path = qrGeneratorService.qrGeneratorService.generate_qr(self,voter_id)
        img = ctk.CTkImage(Image.open(file_path), size=(200, 200))
        self.qr_label.configure(image=img, text="")
        self.qr_label.image = img 

    def back_to_login(self):
        self.status_frame.destroy()
        self.parent.login_page()

if __name__ == "__main__":
    app = App()
    app.mainloop()

