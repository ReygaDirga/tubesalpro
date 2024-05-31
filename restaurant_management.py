import customtkinter as ctk
import mysql.connector
from tkinter import ttk
import matplotlib.pyplot as plt
ctk.set_appearance_mode("light")


def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_db")
    cursor.execute("USE restaurant_db")
    cursor.execute('''CREATE TABLE IF NOT EXISTS kategori (
                        id_kategori INT AUTO_INCREMENT PRIMARY KEY,
                        nama_kategori VARCHAR(100) NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rasa (
                        id_rasa INT AUTO_INCREMENT PRIMARY KEY,
                        nama_rasa VARCHAR(100) NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                        id_menu INT AUTO_INCREMENT PRIMARY KEY,
                        nama_menu VARCHAR(100) NOT NULL,
                        stok INT NOT NULL,
                        harga DECIMAL(10, 2) NOT NULL,
                        id_kategori INT,
                        id_rasa INT,
                        FOREIGN KEY (id_kategori) REFERENCES kategori(id_kategori),
                        FOREIGN KEY (id_rasa) REFERENCES rasa(id_rasa))''')
    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="restaurant_db"
    )
    return conn

def create_menu(nama_menu, stok, harga, id_kategori, id_rasa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO menu (nama_menu, stok, harga, id_kategori, id_rasa) 
                      VALUES (%s, %s, %s, %s, %s)''', (nama_menu, stok, harga, id_kategori, id_rasa))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_menu():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select menu.id_menu, menu.nama_menu, menu.harga, menu.stok, kategori.nama_kategori, rasa.nama_rasa from menu join kategori on kategori.id_kategori = menu.id_kategori join rasa on rasa.id_rasa = menu.id_rasa order by menu.id_menu asc')
    menus = cursor.fetchall()
    cursor.close()
    conn.close()
    return menus

def update_menu(id_menu, nama_menu, stok, harga, id_kategori, id_rasa):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE menu 
                      SET nama_menu = %s, stok = %s, harga = %s, id_kategori = %s, id_rasa = %s 
                      WHERE id_menu = %s''', (nama_menu, stok, harga, id_kategori, id_rasa, id_menu))
    conn.commit()
    cursor.close()
    conn.close()

def delete_menu(id_menu):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM menu WHERE id_menu = %s', (id_menu,))
    conn.commit()
    cursor.close()
    conn.close()

def search_menuid(id_menu):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE id_menu = %s', (id_menu,))
    delete = cursor.fetchall()
    cursor.close()
    conn.close()
    return delete

def search_menu(nama_menu):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE nama_menu LIKE %s', ('%' + nama_menu + '%',))
    menus = cursor.fetchall()
    cursor.close()
    conn.close()
    return menus

def filter_menu_by_kategori(id_kategori):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE id_kategori = %s', (id_kategori,))
    menus = cursor.fetchall()
    cursor.close()
    conn.close()
    return menus

def visualize_menu_stok():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT kategori.nama_kategori, SUM(menu.stok) as total_stok 
                      FROM menu 
                      JOIN kategori ON menu.id_kategori = kategori.id_kategori 
                      GROUP BY kategori.nama_kategori''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    nama_kategori = [row[0] for row in data]
    total_stok = [row[1] for row in data]
    total_stok_sum = sum(total_stok)
    stok_persen = [(stok / total_stok_sum) * 100 for stok in total_stok]
    plt.pie(stok_persen, labels=nama_kategori, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Persentase Stok Menu per Kategori')
    plt.show()  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Flavor Wings")
        self.geometry("1500x800")
        self.configure(fg_color="white")
        self.sidebar = ctk.CTkFrame(self, width=200,fg_color="#20232A",bg_color="#20232A")
        self.sidebar.pack(side="left", fill="y")
        
        self.content = ctk.CTkFrame(self, width=400,fg_color="white")
        self.content.pack(side="right", fill="both", expand=True)
        
        self.setup_sidebar()
        self.display_home()

    def setup_sidebar(self):
        label = ctk.CTkLabel(self.sidebar, text="Manajemen Menu", font=("Arial", 24),text_color="white")
        label.pack(pady=10)
        label = ctk.CTkLabel(self.sidebar, text="Restaurant", font=("Arial", 24),text_color="white")
        label.pack(pady=10)
        buttons = [
            ("Home", self.display_home),
            ("Insert Data", self.display_insert_data),
            ("Update Data", self.display_update_data),
            ("Hapus Data", self.display_delete_data),
            ("Search Menu", self.display_search_menu),
            ("Filter Menu Berdasarkan Kategori", self.display_filter_menu),
            ("Visualisasi Stok Menu", self.display_visualize_stok)
        ]
        
        for (text, command) in buttons:
            button = ctk.CTkButton(self.sidebar, text=text, command=command,font=("Arial", 18), width=200, height=50)
            button.pack(fill="x", pady=10)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def display_home(self):
        self.clear_content()
        label = ctk.CTkLabel(self.content, text="Selamat Datang di Flavor Wings!", font=("Arial", 24),text_color="black")
        label.pack(pady=20)

        menus = get_all_menu()
        if not menus:
            ctk.CTkLabel(self.content, text="Tidak ada data untuk ditampilkan.", font=("Arial", 24)).pack(pady=20)
        else:
            style = ttk.Style()
            style.configure("Treeview", 
                            background="white", 
                            foreground="black", 
                            rowheight=25, 
                            fieldbackground="white",)
            style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
            tree = ttk.Treeview(self.content, columns=("ID", "Nama Menu", "Harga", "Stok", "Kategori"), show='headings')
            tree.heading("ID", text="ID Menu")
            tree.heading("Nama Menu", text="Nama Menu")
            tree.heading("Harga", text="Harga")
            tree.heading("Stok", text="Stok")
            tree.heading("Kategori", text="Kategori")
            tree.column("#0", width=100)
            for menu in menus:
                tree.insert("", "end", values=menu)
                
            tree.pack(fill="both", expand=True, pady=10)

    def display_insert_data(self):
        self.clear_content()
        
        def submit_data():
            nama_menu = entry_nama.get()
            stok = int(entry_stok.get())
            harga = float(entry_harga.get())
            id_kategori = int(entry_id_kategori.get())
            id_rasa = int(entry_id_rasa.get())
            create_menu(nama_menu, stok, harga, id_kategori, id_rasa)
            ctk.CTkLabel(self.content, text="Menu berhasil ditambahkan!", text_color="green", font=("Arial", 20)).pack(pady=10)

        label = ctk.CTkLabel(self.content, text="Insert Data Menu Restaurant Flavor Wings!", font=("Arial", 24))
        label.pack(pady=20)

        ctk.CTkLabel(self.content, text="Masukkan nama menu", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_nama = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_nama.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan stok", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_stok = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_stok.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan harga", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_harga = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_harga.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan ID kategori", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_id_kategori = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_id_kategori.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan ID rasa", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_id_rasa = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_id_rasa.pack(pady=5)

        submit_button = ctk.CTkButton(self.content, text="Submit", command=submit_data, font=("Arial", 20),  width=1200, height=40)
        submit_button.pack(pady=20)

    def display_update_data(self):
        self.clear_content()
        
        def submit_update():
            id_menu = int(entry_id_menu.get())
            nama_menu = entry_nama.get()
            stok = int(entry_stok.get())
            harga = float(entry_harga.get())
            id_kategori = int(entry_id_kategori.get())
            id_rasa = int(entry_id_rasa.get())
            update_menu(id_menu, nama_menu, stok, harga, id_kategori, id_rasa)
            ctk.CTkLabel(self.content, text="Menu berhasil diupdate!", text_color="green", font=("Arial", 20)).pack(pady=10)

        ctk.CTkLabel(self.content, text="Masukkan ID menu yang ingin diupdate:").pack(pady=5)
        entry_id_menu = ctk.CTkEntry(self.content)
        entry_id_menu.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan nama menu baru:").pack(pady=5)
        entry_nama = ctk.CTkEntry(self.content)
        entry_nama.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan stok baru:").pack(pady=5)
        entry_stok = ctk.CTkEntry(self.content)
        entry_stok.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan harga baru:").pack(pady=5)
        entry_harga = ctk.CTkEntry(self.content)
        entry_harga.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan ID kategori baru:").pack(pady=5)
        entry_id_kategori = ctk.CTkEntry(self.content)
        entry_id_kategori.pack(pady=5)

        ctk.CTkLabel(self.content, text="Masukkan ID rasa baru:").pack(pady=5)
        entry_id_rasa = ctk.CTkEntry(self.content)
        entry_id_rasa.pack(pady=5)

        submit_button = ctk.CTkButton(self.content, text="Update", command=submit_update)
        submit_button.pack(pady=20)

    def display_delete_data(self):
        self.clear_content()
        label = ctk.CTkLabel(self.content, text="Hapus Menu", font=("Arial", 24))
        label.pack(pady=20)
        def delet():
            delet_menu = entry_id_menu.get()
            delete_menu(delet_menu)
            ctk.CTkLabel(self.content, text="Menu berhasil dihapus!", text_color="red").pack(pady=10)
        def submit_delete():
            id_menu = entry_id_menu.get()
            delete = search_menuid(id_menu)
            if not delete:
                ctk.CTkLabel(self.content, text="Tidak ada data untuk ditampilkan.", font=("Arial", 24)).pack(pady=20)
            else:
                style = ttk.Style()
                style.configure("Treeview", 
                                background="white", 
                                foreground="black", 
                                rowheight=25, 
                                fieldbackground="white",)
                style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
                tree = ttk.Treeview(self.content, columns=("ID", "Nama Menu", "Harga", "Stok", "Kategori"), show='headings')
                tree.heading("ID", text="ID Menu")
                tree.heading("Nama Menu", text="Nama Menu")
                tree.heading("Harga", text="Harga")
                tree.heading("Stok", text="Stok")
                tree.heading("Kategori", text="Kategori")
            
                for menu in delete:
                    tree.insert("", "end", values=menu)
                    
                tree.pack(fill="both", expand=True, pady=10)
            submit_button = ctk.CTkButton(self.content, text="Hapus", command=delet, font=("Arial", 20),  width=1200, height=40)
            submit_button.pack(pady=20)   
            
        
        ctk.CTkLabel(self.content, text="Masukkan ID menu yang ingin dihapus", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_id_menu = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_id_menu.pack(pady=5)

        submit_button = ctk.CTkButton(self.content, text="Search", command=submit_delete, font=("Arial", 20),  width=1200, height=40)
        submit_button.pack(pady=20)

    def display_search_menu(self):
        self.clear_content()
        label = ctk.CTkLabel(self.content, text="Search Menu", font=("Arial", 24))
        label.pack(pady=20)
        def submit_search():
            nama_menu = entry_nama.get()
            menus = search_menu(nama_menu)
            if not menus:
                ctk.CTkLabel(self.content, text="Tidak ada data untuk ditampilkan.", font=("Arial", 24)).pack(pady=20)
            else:
                style = ttk.Style()
                style.configure("Treeview", 
                                background="white", 
                                foreground="black", 
                                rowheight=25, 
                                fieldbackground="white",)
                style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
                tree = ttk.Treeview(self.content, columns=("ID", "Nama Menu", "Harga", "Stok", "Kategori"), show='headings')
                tree.heading("ID", text="ID Menu")
                tree.heading("Nama Menu", text="Nama Menu")
                tree.heading("Harga", text="Harga")
                tree.heading("Stok", text="Stok")
                tree.heading("Kategori", text="Kategori")
            
                for menu in menus:
                    tree.insert("", "end", values=menu)
                    
                tree.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(self.content, text="Search Menu", font=("Arial", 20)).pack(anchor="w", pady=5, padx=10)
        entry_nama = ctk.CTkEntry(self.content,  width=1200, height=40, font=("Arial", 15))
        entry_nama.pack(pady=5)

        submit_button = ctk.CTkButton(self.content, text="Search", command=submit_search, font=("Arial", 20),  width=1200, height=40)
        submit_button.pack(pady=20)

    def display_filter_menu(self):
        self.clear_content()

        def submit_filter(id_kategori):
            menus = filter_menu_by_kategori(id_kategori)
            for menu in menus:
                ctk.CTkLabel(self.content, text=str(menu)).pack(pady=2)
        label = ctk.CTkLabel(self.content, text="Filterasi Menu Restaurant Flavor Wings!", font=("Arial", 24))
        label.pack(pady=20)
        button_width = 20
        button_height = 2
        button_padding_x = 10
        button_padding_y = 20
        start_x = 10
        start_y = 100
        spacing_x = button_width + button_padding_x

        button1 = ctk.CTkButton(self.content, text="Paket Kombo", command=lambda: submit_filter(1), width=button_width, height=button_height)
        button1.place(x=start_x, y=start_y)

        button2 = ctk.CTkButton(self.content, text="Paket Keluarga", command=lambda: submit_filter(2), width=button_width, height=button_height)
        button2.place(x=button1.winfo_x() + spacing_x, y=start_y)

        button3 = ctk.CTkButton(self.content, text="Minuman", command=lambda: submit_filter(3), width=button_width, height=button_height)
        button3.place(x=button2.winfo_x() + spacing_x, y=start_y)

        button4 = ctk.CTkButton(self.content, text="Dessert", command=lambda: submit_filter(4), width=button_width, height=button_height)
        button4.place(x=start_x, y=button1.winfo_y() + button1.winfo_reqheight() + button_padding_y)

        button5 = ctk.CTkButton(self.content, text="Burger", command=lambda: submit_filter(5), width=button_width, height=button_height)
        button5.place(x=button4.winfo_x() + spacing_x, y=button1.winfo_y() + button1.winfo_reqheight() + button_padding_y)

        button6 = ctk.CTkButton(self.content, text="Sides", command=lambda: submit_filter(6), width=button_width, height=button_height)
        button6.place(x=button5.winfo_x() + spacing_x, y=button1.winfo_y() + button1.winfo_reqheight() + button_padding_y)

    def display_visualize_stok(self):
        self.clear_content()
        visualize_menu_stok()

if __name__ == "__main__":
    setup_database()
    app = App()
    app.mainloop()
