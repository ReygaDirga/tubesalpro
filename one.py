import mysql.connector
import matplotlib.pyplot as plt
from prettytable import PrettyTable

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
    cursor.execute('SELECT * FROM menu')
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
    
def print_table(data):
    table = PrettyTable()
    table.field_names = ["ID Menu", "Nama Menu", "Stok", "Harga", "ID Kategori", "ID Rasa"]
    for row in data:
        table.add_row(row)
    print(table)

def display_menu():
    print("\n=== Menu Manajemen Restoran ===")
    print("1. Insert Data")
    print("2. Show Data")
    print("3. Update Data")
    print("4. Hapus Data")
    print("5. Search Menu")
    print("6. Filter Menu Berdasarkan Kategori")
    print("7. Visualisasi Stok Menu")
    print("8. Keluar")
    return input("Pilih opsi (1-8): ")

if __name__ == "__main__":
    setup_database()

    while True:
        choice = display_menu()

        if choice == '1':
            nama_menu = input("Masukkan nama menu: ")
            stok = int(input("Masukkan stok: "))
            harga = float(input("Masukkan harga: "))
            id_kategori = int(input("Masukkan ID kategori: "))
            id_rasa = int(input("Masukkan ID rasa: "))
            create_menu(nama_menu, stok, harga, id_kategori, id_rasa)
            print("Menu berhasil ditambahkan!")

        elif choice == '2':
            print("\n=== Daftar Menu ===")
            menus = get_all_menu()
            print_table(menus)

        elif choice == '3':
            id_menu = int(input("Masukkan ID menu yang ingin diupdate: "))
            nama_menu = input("Masukkan nama menu baru: ")
            stok = int(input("Masukkan stok baru: "))
            harga = float(input("Masukkan harga baru: "))
            id_kategori = int(input("Masukkan ID kategori baru: "))
            id_rasa = int(input("Masukkan ID rasa baru: "))
            update_menu(id_menu, nama_menu, stok, harga, id_kategori, id_rasa)
            print("Menu berhasil diupdate!")

        elif choice == '4':
            id_menu = int(input("Masukkan ID menu yang ingin dihapus: "))
            delete_menu(id_menu)
            print("Menu berhasil dihapus!")

        elif choice == '5':
            nama_menu = input("Masukkan nama menu yang dicari: ")
            print("\n=== Hasil Pencarian ===")
            for menu in search_menu(nama_menu):
                print(menu)

        elif choice == '6':
            id_kategori = int(input("Masukkan ID kategori: "))
            print("\n=== Menu dengan Kategori Tertentu ===")
            for menu in filter_menu_by_kategori(id_kategori):
                print(menu)

        elif choice == '7':
            visualize_menu_stok()

        elif choice == '8':
            print("Keluar dari program. Sampai jumpa!")
            break

        else:
            print("Pilihan tidak valid, coba lagi!")
