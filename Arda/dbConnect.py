import mysql.connector

cnx = mysql.connector.connect(user='ardafakili', password='lorec',
                              host='34.65.17.107',
                              database='lorecdb')

cursor = cnx.cursor()
#query = ('INSERT INTO user (username,email,password,GlassNameDbid) values ("malcan", "ardafakili@gmail.com","123123",1);')
query = ('SELECT * from user')

cursor.execute(query)

for something in cursor:
    print(something)

cnx.commit()
cnx.close()
