import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import time

# --- DATA STRUCTURES ---

class Node:
    """Linked List Node for Transactions"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class TransactionLinkedList:
    """Doubly Linked List to manage history in memory efficiently"""
    def __init__(self):
        self.head = None
        self.tail = None

    def add_transaction(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('ibbl_final_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (acc_no TEXT PRIMARY KEY, pin TEXT, balance REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (acc_no TEXT, type TEXT, amount REAL, time TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS login_history 
                      (acc_no TEXT, status TEXT, time TEXT)''')
    conn.commit()
    conn.close()

# --- ALGORITHMS ---

def binary_search_user(acc_list, target_acc):
    """Binary Search Algorithm: Complexity O(log n)"""
    low = 0
    high = len(acc_list) - 1
    while low <= high:
        mid = (low + high) // 2
        if acc_list[mid][0] == target_acc:
            return acc_list[mid]
        elif acc_list[mid][0] < target_acc:
            low = mid + 1
        else:
            high = mid - 1
    return None

def quick_sort_descending(data):
    """Quick Sort: Sorts transactions by Amount (index 2) in Descending Order"""
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2][2]
    left = [x for x in data if x[2] > pivot]
    middle = [x for x in data if x[2] == pivot]
    right = [x for x in data if x[2] < pivot]
    return quick_sort_descending(left) + middle + quick_sort_descending(right)

# --- GUI CLASS ---
class AdvancedIslamicATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Islami Bank - ATM Terminal")
        self.root.geometry("540x820")
        self.root.configure(bg="#eef2ff")
        self.root.resizable(False, False)
        self.current_user = None
        self.history_list = TransactionLinkedList()
        self.root.iconbitmap(default='')
        self.btn_style = {
            "font": ("Helvetica", 12, "bold"),
            "width": 24,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "bg": "#0f766e",
            "fg": "white",
            "activebackground": "#115e59",
            "activeforeground": "white",
        }
        self.secondary_btn = {
            "font": ("Helvetica", 11, "bold"),
            "width": 22,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "bg": "#334155",
            "fg": "white",
            "activebackground": "#1f2937",
            "activeforeground": "white",
        }
        self.card_style = {"bd": 0, "highlightbackground": "#cbd5e1", "highlightthickness": 1}
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def draw_header(self, title):
        top = tk.Frame(self.root, bg="#0f766e", height=130)
        top.pack(fill="x")
        tk.Label(top, text="ISLAMI BANK", font=("Futura", 30, "bold"), fg="#ffffff", bg="#0f766e").pack(pady=(24,0))
        tk.Label(top, text=title, font=("Arial", 12, "italic"), fg="#d1fae5", bg="#0f766e").pack(pady=(4,10))
        accent = tk.Frame(self.root, bg="#10b981", height=8)
        accent.pack(fill="x")

    def main_menu(self):
        self.clear()
        self.draw_header("DUAL CURRENCY SMART TERMINAL")
        container = tk.Frame(self.root, bg="#eef2ff")
        container.pack(pady=30, padx=20, fill="both", expand=True)

        hero = tk.Frame(container, **self.card_style, bg="#ffffff")
        hero.pack(pady=(0,18), fill="x")
        tk.Label(hero, text="Welcome to Islami Bank Smart ATM", font=("Helvetica", 18, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(18,4))
        tk.Label(hero, text="Secure banking with fast withdrawals, deposits, and account monitoring.", font=("Arial", 10), fg="#475569", bg="#ffffff", wraplength=480, justify="center").pack(pady=(0,18))

        buttons_frame = tk.Frame(container, bg="#eef2ff")
        buttons_frame.pack(pady=10)
        tk.Button(buttons_frame, text="USER LOGIN", command=self.user_login, **self.btn_style).pack(pady=10)
        tk.Button(buttons_frame, text="ADMIN ACCESS", command=self.admin_auth, **self.secondary_btn).pack(pady=10)

        features = tk.Frame(container, **self.card_style, bg="#ffffff")
        features.pack(pady=16, fill="x")
        tk.Label(features, text="App Features", font=("Arial", 12, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(14,6))
        tk.Label(features, text="• Secure login with account and PIN\n• Deposit and withdraw cash easily\n• View sorted mini statements\n• Track login history", font=("Arial", 9), fg="#475569", bg="#ffffff", justify="left").pack(padx=16, pady=(0,14))

        tk.Label(self.root, text="Approved by Tanjim Ahamed Stamford", fg="#475569", bg="#eef2ff", font=("Arial", 8)).pack(side="bottom", pady=14)

    # --- ADMIN FUNCTIONS ---
    def admin_auth(self):
        pin = simpledialog.askstring("Admin", "Enter Security PIN:", show='*')
        if pin == "0000": self.admin_panel()
        elif pin: messagebox.showerror("Denied", "Incorrect Admin PIN")

    def admin_panel(self):
        self.clear()
        self.draw_header("ADMIN CONTROL PANEL")
        body = tk.Frame(self.root, bg="#eef2ff")
        body.pack(pady=30, padx=22, fill="both", expand=True)

        panel = tk.Frame(body, **self.card_style, bg="#ffffff")
        panel.pack(pady=10, fill="x")
        tk.Label(panel, text="Administrator functions", font=("Arial", 12, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(18,6))
        tk.Label(panel, text="Manage accounts and monitor system activity from the admin panel.", font=("Arial", 10), fg="#475569", bg="#ffffff", wraplength=460, justify="left").pack(padx=16, pady=(0,18))

        tk.Button(body, text="➕ Create New User", command=self.create_acc, **self.btn_style).pack(pady=10)
        tk.Button(body, text="← Back to Home", command=self.main_menu, **self.secondary_btn).pack(pady=18)

    def create_acc(self):
        acc = simpledialog.askstring("Input", "Account Number:")
        if not acc: return
        pin = simpledialog.askstring("Input", "Set 4-Digit PIN:")
        bal = simpledialog.askfloat("Input", "Initial Balance (BDT):")
        if acc and pin and bal is not None:
            conn = sqlite3.connect('ibbl_final_pro.db')
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (acc, pin, bal))
                conn.commit()
                messagebox.showinfo("Success", f"Account {acc} Created!")
            except:
                messagebox.showerror("Error", "Account already exists!")
            conn.close()

    # --- USER LOGIN (Binary Search) ---
    def user_login(self):
        self.clear()
        self.draw_header("SECURE AUTHENTICATION")
        box = tk.Frame(self.root, **self.card_style, bg="#ffffff", padx=28, pady=28)
        box.pack(pady=40, padx=22, fill="x")

        tk.Label(box, text="Welcome back!", font=("Helvetica", 16, "bold"), fg="#0f172a", bg="#ffffff").pack(pady=(0,12))
        tk.Label(box, text="Please enter your account details to continue.", font=("Arial", 10), fg="#475569", bg="#ffffff", wraplength=460, justify="center").pack(pady=(0,22))

        tk.Label(box, text="Account Number", bg="#ffffff", font=("Arial", 10, "bold"), fg="#334155").pack(anchor="w")
        self.e_acc = tk.Entry(box, font=("Arial", 14), justify='center', bd=1, relief="solid")
        self.e_acc.pack(pady=(6,16), fill="x")

        tk.Label(box, text="Secret PIN", bg="#ffffff", font=("Arial", 10, "bold"), fg="#334155").pack(anchor="w")
        self.e_pin = tk.Entry(box, font=("Arial", 14), show="*", justify='center', bd=1, relief="solid")
        self.e_pin.pack(pady=(6,24), fill="x")

        tk.Button(box, text="LOG IN", command=self.auth_logic, **self.btn_style).pack(pady=(0,12))
        tk.Button(self.root, text="← Back to Home", command=self.main_menu, **self.secondary_btn).pack(pady=10)

    def auth_logic(self):
        entered_acc = self.e_acc.get().strip()
        entered_pin = self.e_pin.get().strip()
        conn = sqlite3.connect('ibbl_final_pro.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY acc_no ASC") # Binary Search requires sorted data
        acc_list = cursor.fetchall()
        user = binary_search_user(acc_list, entered_acc)

        status = "Failed"
        if user and user[1] == entered_pin:
            status = "Success"
            self.current_user = list(user)

        cursor.execute("INSERT INTO login_history VALUES (?, ?, ?)", (entered_acc, status, time.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()

        if status == "Success":
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid Account or PIN!")

    # --- USER DASHBOARD ---
    def dashboard(self):
        self.clear()
        self.draw_header(f"ACCOUNT: {self.current_user[0]}")

        card = tk.Frame(self.root, **self.card_style, bg="#ffffff", padx=22, pady=24)
        card.pack(pady=26, padx=22, fill="x")
        tk.Label(card, text="Current Balance", fg="#0f172a", bg="#ffffff", font=("Arial", 11, "bold")).pack()
        self.lbl_bal = tk.Label(card, text=f"BDT {self.current_user[2]:,.2f}", fg="#0f766e", bg="#ffffff", font=("Arial", 30, "bold"))
        self.lbl_bal.pack(pady=10)
        tk.Label(card, text="Manage your transactions and account history below.", fg="#475569", bg="#ffffff", font=("Arial", 10), wraplength=460, justify="center").pack(pady=(0,4))

        grid = tk.Frame(self.root, bg="#eef2ff")
        grid.pack(pady=(0,10), padx=22, fill="x")

        tk.Button(grid, text="Withdraw Cash", command=lambda: self.perform_action("Withdraw"), **self.btn_style).pack(pady=8)
        tk.Button(grid, text="Deposit Cash", command=lambda: self.perform_action("Deposit"), **self.btn_style).pack(pady=8)
        tk.Button(grid, text="Mini Statement", command=self.view_history, **self.secondary_btn).pack(pady=8)
        tk.Button(grid, text="Login History", command=self.view_login_history, **self.secondary_btn).pack(pady=8)
        tk.Button(grid, text="Logout", command=self.main_menu, bg="#d1d5db", fg="#111827", width=22, height=2, bd=0, cursor="hand2").pack(pady=22)

    def perform_action(self, mode):
        amt = simpledialog.askfloat(mode, f"Enter amount to {mode} (BDT):")
        if amt and amt > 0:
            if mode == "Withdraw" and amt > self.current_user[2]:
                messagebox.showerror("Error", "Insufficient Balance!")
                return
            
            conn = sqlite3.connect('ibbl_final_pro.db')
            cursor = conn.cursor()
            new_bal = self.current_user[2] - amt if mode == "Withdraw" else self.current_user[2] + amt
            ts = time.strftime('%H:%M:%S')
            
            cursor.execute("UPDATE users SET balance=? WHERE acc_no=?", (new_bal, self.current_user[0]))
            cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (self.current_user[0], mode, amt, ts))
            conn.commit(); conn.close()
            
            self.current_user[2] = new_bal
            self.lbl_bal.config(text=f"BDT {new_bal:,.2f}")
            messagebox.showinfo("Success", f"{mode} Successful!")

    # --- MINI STATEMENT (Quick Sort + Linked List) ---
    def view_history(self):
        conn = sqlite3.connect('ibbl_final_pro.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type, time, amount FROM history WHERE acc_no=?", (self.current_user[0],))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Info", "No history found.")
            return

        # 1. Algorithm: Quick Sort (Sorting by amount descending)
        sorted_rows = quick_sort_descending(list(rows))
        
        # 2. Data Structure: Doubly Linked List (Storing sorted data)
        self.history_list = TransactionLinkedList()
        for r in sorted_rows:
            self.history_list.add_transaction(r)

        # UI for Statement
        win = tk.Toplevel(self.root)
        win.title("Sorted Statement (By Amount)")
        win.geometry("520x460")
        win.configure(bg="#eef2ff")

        header = tk.Frame(win, bg="#ffffff", bd=0, highlightbackground="#cbd5e1", highlightthickness=1)
        header.pack(fill="x", padx=12, pady=(12,6))
        tk.Label(header, text="Sorted Statement", font=("Helvetica", 13, "bold"), fg="#0f172a", bg="#ffffff").pack(side="left", padx=14, pady=12)
        tk.Label(header, text="(Highest amounts first)", font=("Arial", 9), fg="#475569", bg="#ffffff").pack(side="left", padx=8)

        style = ttk.Style(win)
        style.theme_use("default")
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", rowheight=26, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#0f766e", foreground="white")
        style.map("Treeview", background=[("selected", "#d1fae5")])

        tree = ttk.Treeview(win, columns=("T", "D", "A"), show='headings', selectmode='browse')
        tree.heading("T", text="Type")
        tree.heading("D", text="Time")
        tree.heading("A", text="Amount (BDT)")
        tree.column("T", anchor="center", width=160)
        tree.column("D", anchor="center", width=170)
        tree.column("A", anchor="e", width=160)
        tree.pack(fill="both", expand=True, padx=12, pady=12)

        # 3. Traversal: Displaying from Linked List
        current = self.history_list.head
        while current:
            tree.insert("", "end", values=current.data)
            current = current.next

    def view_login_history(self):
        conn = sqlite3.connect('ibbl_final_pro.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status, time FROM login_history WHERE acc_no=? ORDER BY time DESC", (self.current_user[0],))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Info", "No login history found for this account.")
            return

        win = tk.Toplevel(self.root)
        win.title("Login History")
        win.geometry("420x420")
        win.configure(bg="#eff6ff")

        tk.Label(win, text=f"Login history for {self.current_user[0]}", font=("Arial", 12, "bold"), fg="#0f172a", bg="#eff6ff").pack(pady=(16,8))
        summary = tk.Label(win, text=f"Total logins: {len(rows)}", font=("Arial", 10), fg="#334155", bg="#eff6ff")
        summary.pack(pady=(0,12))

        style = ttk.Style(win)
        style.theme_use("default")
        style.configure("Treeview", background="#f8fafc", fieldbackground="#f8fafc", rowheight=26, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#0f766e", foreground="white")

        tree = ttk.Treeview(win, columns=("S", "T"), show='headings', selectmode='none')
        tree.heading("S", text="Status")
        tree.heading("T", text="Timestamp")
        tree.column("S", anchor="center", width=130)
        tree.column("T", anchor="center", width=260)
        tree.pack(fill="both", expand=True, padx=12, pady=12)

        for row in rows:
            tree.insert("", "end", values=row)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = AdvancedIslamicATM(root)
    root.mainloop()