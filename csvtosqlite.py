#This file's for transfering data from a csv file created from excel

import csv
import sqlite3

con = sqlite3.connect('dialect.db')
c = con.cursor()

#create table error handling included
try:
    c.execute('''create table dialect ( Tagalog text, 
                                        Cebuano text, 
                                        Ilocano text,
                                        English text)''')
except:
    pass

#open csv file
with open('dialectscsv.csv','r') as f:
    dataset = csv.reader(f)

    #insert csv data to database (no duplicate filter implemented)
    for r in dataset:
        try:
            pass
            #c.execute("INSERT INTO dialect VALUES (?,?,?,?)",(r[0].upper(),r[2].upper(),r[3].upper(),r[4].upper()))
        except:
            print("fails")

con.commit()

#query all for checking

def translate(From, To, Word):
    c.execute(f"SELECT {To} FROM dialect where {From} = '{Word}'")
    con.commit()
    print(c.fetchall())

translate("Tagalog","English","SAAN")

con.close()