<<<<<<< HEAD
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
=======
import os
import psycopg2

def writedb(conn):
    cur = conn.cursor()
    print("Started opening file to copy into table")

    try:
        with  open("spellbee/docs/Spell_Bee_Word_Unique_db.csv", 'r', encoding="utf-8") as f:
 
            sql_copy ="COPY spellbeeword_tb  FROM STDIN WITH CSV HEADER DELIMITER ',' "
            cur.copy_expert(sql=sql_copy,file=f)
            print('successfully copied files into db')
            # commit changes
            conn.commit()
            print("Committed changes")
    
    except Exception as error:
        print('Error in copying db ',error)
    finally:
        if conn:
            conn.close()
            print("Finally connection closed")
            f.close()

def main():

    DATABASE_URL = os.environ['DATABASE_URL']
    """ DATABASES = {
        'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'spellbee_test_db',
       'USER' : 'spellbee',
       'PASSWORD': 'spellbee@123',
       'HOST': 'localhost',
       'PORT': '',
   }
} """
    

    try:
        conn = psycopg2.connect(DATABASE_URL)
        
        
        writedb(conn)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    

if __name__ == "__main__" :
    main()
        
>>>>>>> master
