import os
import psycopg2

def writedb(conn):
    cur = conn.cursor()
    print("Started opening file to copy into table")

    try:
        with  open("spellbee/docs/Spell_Bee_Word_db.csv", 'r', encoding="utf-8") as f:
            sql_copy= "COPY spellbeeword_tb  FROM stdin (FORMAT CSV)"
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
            f.close()

def main():

    DATABASE_URL = os.environ['DATABASE_URL']

    

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        
        
        writedb(conn)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__" :
    main()
        