import os
import psycopg2

def writedb(conn):
    cur = conn.cursor()
    cur.execute('SELECT version()')
     

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
    cur.execute('SELECT * FROM information_schema.tables;')
    first = cur.fetchall()
    for tb in first:
        
        print('table row:',tb)

    cur.execute('SELECT * FROM "Spellbeeword_tb";')
    first= cur.fetchone()

    print('first row:', first)

    try:
        with  open("spellbee/docs/Spell_Bee_Word_db.csv", 'r') as f:
            cur.copy_from(f,"Spellbeeword_tb",sep=',')
            # commit changes
            conn.commit()
    
    except Exception as error:
        print(error)
    finally:
        if conn:
            conn.close()
            f.close()

def main():

    DATABASE_URL = os.environ['DATABASE_URL']

    print('Printing postgresql db info:',DATABASE_URL)

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # execute an SQL statement to get the HerokuPostgres database version
        print('PostgreSQL database version:')
        
        writedb(conn)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__" :
    main()
        