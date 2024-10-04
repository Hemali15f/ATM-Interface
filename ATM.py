import tkinter as tk
from tkinter import messagebox

class ATM:
    MAX_WITHDRAWAL = 50000
    MAX_TRANSFER = 20000

    def __init__(self):
        self.balance = 100000  # Starting balance
        self.transaction_history = []

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        elif amount > self.MAX_WITHDRAWAL:
            return f"Maximum withdrawal amount exceeded (₹{self.MAX_WITHDRAWAL})"
        else:
            self.balance -= amount
            self.transaction_history.append(("Withdraw", amount))
            return "Withdrawal successful. Remaining balance: ₹" + str(self.balance)

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(("Deposit", amount))
        return "Deposit successful. New balance: ₹" + str(self.balance)

    def transfer(self, amount, username, pin):
        if amount > self.balance:
            return "Insufficient funds!"
        elif amount > self.MAX_TRANSFER:
            return f"Maximum transfer amount exceeded (₹{self.MAX_TRANSFER})"
        elif pin != "1234":
            return "Invalid PIN. Transfer failed."
        else:
            self.balance -= amount
            self.transaction_history.append(("Transfer to " + username, amount))
            return f"Transfer to {username} successful. Remaining balance: ₹{self.balance}"

    def display_transaction_history(self):
        transaction_history = "Transaction History:\n"
        for transaction in self.transaction_history:
            transaction_history += transaction[0] + " - ₹" + str(transaction[1]) + "\n"
        return transaction_history

class ATMInterface:
    def __init__(self, master):
        self.master = master
        master.title("ATM Interface")
        master.geometry("400x400")  # Set window size
        master.configure(bg='#FFE4E1')  # Set background color to light pink-peach

        self.logged_in = False

        self.atm = ATM()

        self.login_frame = tk.Frame(master, bg='#FFE4E1')  # Set background color to light pink-peach
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", bg='#FFE4E1')  # Set background color to light pink-peach
        self.username_label.grid(row=0, column=0)

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.pin_label = tk.Label(self.login_frame, text="PIN:", bg='#FFE4E1')  # Set background color to light pink-peach
        self.pin_label.grid(row=1, column=0)

        self.pin_entry = tk.Entry(self.login_frame, show="*")
        self.pin_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.operations_frame = tk.Frame(master, bg='#FFE4E1')  # Set background color to light pink-peach
        self.operations_frame.pack()

        self.label = tk.Label(self.operations_frame, text="Welcome to the ATM", bg='#FFE4E1', anchor='center')  # Set background color to light pink-peach, align text to center
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')  # Make the label expand horizontally to fill the frame and align at top

    def login(self):
        valid_username = "user"
        valid_pin = "1234"
        entered_username = self.username_entry.get()
        entered_pin = self.pin_entry.get()

        if entered_username == valid_username and entered_pin == valid_pin:
            self.logged_in = True
            self.login_frame.pack_forget()  # Hide the login frame
            self.label.config(text="Welcome, " + entered_username)
            self.show_buttons()
        else:
            messagebox.showerror("Login Failed", "Invalid username or PIN. Please try again.")

    def show_buttons(self):
        buttons = [
            ("Check Balance", self.check_balance),
            ("Withdraw", self.open_withdraw_window),
            ("Deposit", self.open_deposit_window),
            ("Transfer", self.open_transfer_window),
            ("Transaction History", self.display_transaction_history)
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(self.operations_frame, text=text, font=("Arial", 12), width=15, command=command)
            button.grid(row=i+1, column=0, padx=10, pady=5)  # Buttons in vertical manner
            button.config(bg="black", fg="white")  # Change button color and font color

        exit_button = tk.Button(self.operations_frame, text="Exit", font=("Arial", 12), width=15, command=self.exit_button)
        exit_button.grid(row=len(buttons)+1, column=0, pady=10)  # Exit button at the bottom
        exit_button.config(bg="black", fg="white")  # Change button color and font color

    def check_balance(self):
        if self.logged_in:
            self.display_message("Your balance is: ₹" + str(self.atm.balance))
        else:
            messagebox.showerror("Access Denied", "Please login to access this feature.")

    def open_withdraw_window(self):
        if self.logged_in:
            self.withdraw_window = tk.Toplevel(self.master)
            self.withdraw_window.title("Withdraw")
            tk.Label(self.withdraw_window, text="Enter the amount to withdraw: ").pack()
            self.withdraw_amount_entry = tk.Entry(self.withdraw_window)
            self.withdraw_amount_entry.pack()
            withdraw_button = tk.Button(self.withdraw_window, text="Withdraw", command=self.do_withdraw)
            withdraw_button.pack()
        else:
            messagebox.showerror("Access Denied", "Please login to access this feature.")

    def do_withdraw(self):
        amount = float(self.withdraw_amount_entry.get())
        result = self.atm.withdraw(amount)
        if result.startswith("Withdrawal successful"):
            self.display_message(f"Withdrawal successful. Remaining balance: ₹{self.atm.balance}")
            self.update_balance_label()
            self.withdraw_window.destroy()
        else:
            messagebox.showerror("Withdrawal Failed", result)

    def open_deposit_window(self):
        if self.logged_in:
            self.deposit_window = tk.Toplevel(self.master)
            self.deposit_window.title("Deposit")
            tk.Label(self.deposit_window, text="Enter the amount to deposit: ").pack()
            self.deposit_amount_entry = tk.Entry(self.deposit_window)
            self.deposit_amount_entry.pack()
            deposit_button = tk.Button(self.deposit_window, text="Deposit", command=self.do_deposit)
            deposit_button.pack()
        else:
            messagebox.showerror("Access Denied", "Please login to access this feature.")

    def do_deposit(self):
        amount = float(self.deposit_amount_entry.get())
        result = self.atm.deposit(amount)
        if result.startswith("Deposit successful"):
            self.display_message(f"Deposit successful. New balance: ₹{self.atm.balance}")
            self.update_balance_label()
            self.deposit_window.destroy()
        else:
            messagebox.showerror("Deposit Failed", result)

    def open_transfer_window(self):
        if self.logged_in:
            self.transfer_window = tk.Toplevel(self.master)
            self.transfer_window.title("Transfer")
            tk.Label(self.transfer_window, text="Enter the amount to transfer: ").pack()
            self.transfer_amount_entry = tk.Entry(self.transfer_window)
            self.transfer_amount_entry.pack()
            tk.Label(self.transfer_window, text="Enter the username to transfer to: ").pack()
            self.transfer_username_entry = tk.Entry(self.transfer_window)
            self.transfer_username_entry.pack()
            tk.Label(self.transfer_window, text="Enter your PIN: ").pack()
            self.transfer_pin_entry = tk.Entry(self.transfer_window, show="*")
            self.transfer_pin_entry.pack()
            transfer_button = tk.Button(self.transfer_window, text="Transfer", command=self.do_transfer)
            transfer_button.pack()
        else:
            messagebox.showerror("Access Denied", "Please login to access this feature.")

    def do_transfer(self):
        amount = float(self.transfer_amount_entry.get())
        username = self.transfer_username_entry.get()
        pin = self.transfer_pin_entry.get()
        result = self.atm.transfer(amount, username, pin)
        if result.startswith("Transfer to"):
            self.display_message(f"Transfer to {username} successful. Remaining balance: ₹{self.atm.balance}")
            self.update_balance_label()
            self.transfer_window.destroy()
        else:
            messagebox.showerror("Transfer Failed", result)

    def display_transaction_history(self):
        if self.logged_in:
            messagebox.showinfo("Transaction History", self.atm.display_transaction_history())
        else:
            messagebox.showerror("Access Denied", "Please login to access this feature.")

    def display_message(self, message):
        self.label.config(text=message)

    def update_balance_label(self):
        self.label.config(text="Balance now is: ₹" + str(self.atm.balance))

    def exit_button(self):
        self.master.withdraw()  # Hide the main window
        self.exit_window = tk.Toplevel(self.master)
        self.exit_window.title("Thank You")
        tk.Label(self.exit_window, text="Thank you for using our ATM!", font=("Arial", 14), pady=20).pack()
        tk.Button(self.exit_window, text="OK", command=self.master.quit).pack(pady=20)  # Exit button in center

def main():
    root = tk.Tk()
    atm_interface = ATMInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
