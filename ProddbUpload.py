import os, csv
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    cur = conn.cursor()
    inp_file = open("spellbee/docs/Spell_Bee_Merged_db.csv")
    rows = csv.reader(inp_file)
    head =True
    for row in rows:
        if not head:
            data = (row[0],row[1],row[2])   
            cur.execute("INSERT INTO Spellbeeword_tb VALUES(?, ?,?)", data)
        else:
            head = False
    cur.execute("SELECT * FROM Spellbeeword_tb limit 5")
    print(cur.fetchall())   
    conn.commit()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn:
        conn.close()
    inp_file.close()