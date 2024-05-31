import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

# Koneksi ke database MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tkinter"
)
cursor = conn.cursor()

# Function buat tambah data
def tambah_dataa():
    nama = entry_nama.get()
    umur = entry_umur.get()
    if nama and umur:
        cursor.execute("INSERT INTO users (id, nama, umur) VALUES (%s, %s, %s)", (nama, umur))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil ditambah!")
        entry_nama.delete(0, ctk.END)
        entry_umur.delete(0, ctk.END)
        tampil_data()
    else:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")

# Function buat tampil data
def tampil_data():
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()
    listbox.delete(0, ctk.END)
    for record in records:
        listbox.insert(ctk.END, f"ID: {record[0]}, Nama: {record[1]}, Umur: {record[2]}")

# Function buat hapus data
def hapus_data():
    selected_item = listbox.curselection()
    if selected_item:
        data = listbox.get(selected_item)
        user_id = data.split(", ")[0].split(": ")[1]
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        tampil_data()
    else:
        messagebox.showwarning("Peringatan", "Pilih data yang mau dihapus!")

# Setup UI
root = ctk.CTk()
root.title("CustomTkinter CRUD App")

ctk.CTkLabel(root, text="Nama:").grid(row=0, column=0)
entry_nama = ctk.CTkEntry(root)
entry_nama.grid(row=0, column=1)

ctk.CTkLabel(root, text="Umur:").grid(row=1, column=0)
entry_umur = ctk.CTkEntry(root)
entry_umur.grid(row=1, column=1)

def tambah_data():
    # Tambahin logic buat tambah data di sini
    print("Data ditambah")

def hapus_data():
    # Tambahin logic buat hapus data di sini
    print("Data dihapus")

ctk.CTkButton(root, text="Tambah Data", command=tambah_dataa).grid(row=2, column=0, columnspan=2)
ctk.CTkButton(root, text="Hapus Data", command=hapus_data).grid(row=3, column=0, columnspan=2)

root.mainloop()

# Jangan lupa tutup koneksi
cursor.close()
conn.close()
