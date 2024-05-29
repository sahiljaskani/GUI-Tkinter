import sqlite3
import pandas as pd

# Kobler til SQLite database (elelr lager en hvis den ikke eksisterer)
conn = sqlite3.connect("kunder.db")
cursor = conn.cursor()

# Lager "kunder" tabellen
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS kunder (
    fname TEXT NOT NULL,
    ename TEXT NOT NULL,
    epost TEXT NOT NULL,
    tlf INTEGER,
    postnummer INTEGER,
    kundenummer INTEGER
)
"""
)

# Leser CSV-Fil
csv_fil = "randomskunder.csv"
df = pd.read_csv(csv_fil)

# Setter inn data i databasen
for index, row in df.iterrows():
    cursor.execute(
        """
    INSERT OR IGNORE INTO kunder (fname, ename, epost, tlf, postnummer, kundenummer) 
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            row["fname"],
            row["ename"],
            row["epost"],
            int(row["tlf"]),
            int(row["postnummer"]),
            int(row["kundenummer"]),
        ),
    )

# Commiter endringene og avslutter koblingen
conn.commit()
conn.close()
