import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Funksjon for å koble til databasen
def koble_til_db():
    return sqlite3.connect("kunder.db")

# Class for GUI
class KundeApp:
    def __init__(self, rot):
        self.rot = rot
        self.rot.title("Kundedatabase")  # Lager tittel til vinduet

        # Meny
        meny = tk.Menu(rot)
        rot.config(menu=meny)

        fil_meny = tk.Menu(meny)
        meny.add_cascade(label="Fil", menu=fil_meny)
        fil_meny.add_command(label="Opprett Kunde", command=self.opprett_kunde)  # Legger til kommando for å opprette kunde
        fil_meny.add_command(label="Slett Kunde", command=self.slett_kunde)  # Legger til kommando for å slette kunde

        # Søkefelt og knapp
        self.sok_etikett = tk.Label(rot, text="Kundenummer:")
        self.sok_etikett.grid(row=0, column=0, padx=10, pady=10)

        self.sok_inndata = tk.Entry(rot)
        self.sok_inndata.grid(row=0, column=1, padx=10, pady=10)

        self.sok_knapp = tk.Button(
            rot, text="Søk", command=self.sok_kunde
        )
        self.sok_knapp.grid(row=0, column=2, padx=10, pady=10)

        # Treeview for å vise kundedata
        self.tre = ttk.Treeview(
            rot,
            columns=("fornavn", "etternavn", "epost", "telefon", "postnummer", "kundenummer"),
            show="headings",
        )
        self.tre.heading("fornavn", text="Fornavn")
        self.tre.heading("etternavn", text="Etternavn")
        self.tre.heading("epost", text="E-post")
        self.tre.heading("telefon", text="Telefon")
        self.tre.heading("postnummer", text="Postnummer")
        self.tre.heading("kundenummer", text="Kundenummer")
        self.tre.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Funksjon for å søke etter en kunde
    def sok_kunde(self):
        kundenummer = self.sok_inndata.get()
        if not kundenummer.isdigit():
            messagebox.showerror("Feil", "Kundenummer må være et tall")
            return

        conn = koble_til_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fname, ename, epost, tlf, postnummer, kundenummer FROM kunder WHERE kundenummer=?",
            (kundenummer,),
        )
        resultat = cursor.fetchone()
        conn.close()

        if resultat:
            for i in self.tre.get_children():
                self.tre.delete(i)
            self.tre.insert("", "end", values=resultat)
        else:
            messagebox.showinfo("Ikke Funnet", "Kunde ikke funnet")

    # Funksjon for å opprette en ny kunde
    def opprett_kunde(self):
        self.nytt_vindu = tk.Toplevel(self.rot)
        self.nytt_vindu.title("Opprett Kunde")

        tk.Label(self.nytt_vindu, text="Fornavn:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.nytt_vindu, text="Etternavn:").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.nytt_vindu, text="E-post:").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.nytt_vindu, text="Telefon:").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self.nytt_vindu, text="Postnummer:").grid(row=4, column=0, padx=10, pady=10)
        tk.Label(self.nytt_vindu, text="Kundenummer:").grid(row=5, column=0, padx=10, pady=10)

        self.fornavn_inndata = tk.Entry(self.nytt_vindu)
        self.fornavn_inndata.grid(row=0, column=1, padx=10, pady=10)
        self.etternavn_inndata = tk.Entry(self.nytt_vindu)
        self.etternavn_inndata.grid(row=1, column=1, padx=10, pady=10)
        self.epost_inndata = tk.Entry(self.nytt_vindu)
        self.epost_inndata.grid(row=2, column=1, padx=10, pady=10)
        self.telefon_inndata = tk.Entry(self.nytt_vindu)
        self.telefon_inndata.grid(row=3, column=1, padx=10, pady=10)
        self.postnummer_inndata = tk.Entry(self.nytt_vindu)
        self.postnummer_inndata.grid(row=4, column=1, padx=10, pady=10)
        self.kundenummer_inndata = tk.Entry(self.nytt_vindu)
        self.kundenummer_inndata.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(self.nytt_vindu, text="Opprett", command=self.lagre_kunde).grid(
            row=6, column=0, columnspan=2, pady=10
        )

    # Funksjon for å lagre en ny kunde
    def lagre_kunde(self):
        fornavn = self.fornavn_inndata.get()
        etternavn = self.etternavn_inndata.get()
        epost = self.epost_inndata.get()
        telefon = self.telefon_inndata.get()
        postnummer = self.postnummer_inndata.get()
        kundenummer = self.kundenummer_inndata.get()

        if not kundenummer.isdigit():
            messagebox.showerror("Feil", "Kundenummer må være et tall")
            return

        conn = koble_til_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO kunder (fname, ename, epost, tlf, postnummer, kundenummer) VALUES (?, ?, ?, ?, ?, ?)",
                (fornavn, etternavn, epost, int(telefon), int(postnummer), int(kundenummer)),
            )
            conn.commit()
            messagebox.showinfo("Suksess", "Kunde opprettet")
            self.nytt_vindu.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Feil", "Kundenummer eksisterer allerede")
        finally:
            conn.close()

    # Funksjon for å slette en kunde
    def slett_kunde(self):
        self.slett_vindu = tk.Toplevel(self.rot)
        self.slett_vindu.title("Slett Kunde")

        tk.Label(self.slett_vindu, text="Kundenummer:").grid(row=0, column=0, padx=10, pady=10)

        self.slett_inndata = tk.Entry(self.slett_vindu)
        self.slett_inndata.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.slett_vindu, text="Slett", command=self.fjern_kunde).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    # Funksjon for å fjerne en kunde fra databasen
    def fjern_kunde(self):
        kundenummer = self.slett_inndata.get()

        if not kundenummer.isdigit():
            messagebox.showerror("Feil", "Kundenummer må være et tall")
            return

        conn = koble_til_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM kunder WHERE kundenummer=?", (kundenummer,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            messagebox.showinfo("Ikke Funnet", "Kunde ikke funnet")
        else:
            messagebox.showinfo("Suksess", "Kunde slettet")
            self.slett_vindu.destroy()

# Hoveddel av programmet
if __name__ == "__main__":
    rot = tk.Tk()  
    app = KundeApp(rot)  
    rot.mainloop()  
