import sqlite3, csv
try:
    conn = sqlite3.connect(r"C:\Users\User\projects\Datascience\BeeWord_Project\Bee_Project\db.sqlite3")
    cur = conn.cursor()
    inp_file = open("docs/Spell_Bee_Merged_db.csv")
    rows = csv.reader(inp_file)
    head =True
    for row in rows:
        if not head:
            data = (row[0],row[1],row[2])   
            cur.execute("INSERT INTO Spellbeeword_tb VALUES (?, ?,?)", data)
        else:
            head = False
    cur.execute("SELECT * FROM Spellbeeword_tb limit 5")
    print(cur.fetchall())   
    conn.commit()
except sqlite3.Error as e:
    print("Error {}".format(e.args[0]))
finally:
    if conn:
        conn.close()
    inp_file.close()