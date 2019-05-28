import mysql.connector

cnx = mysql.connector.connect(user='root', password='aey.1996',
                              host='34.65.17.107',
                              database='lorecdb')

cursor = cnx.cursor()
#query = ('INSERT INTO user (username,email,password,GlassNameDbid) values ("arda", "ardafakili@gmail.com","123123",1);')
#query = ("CREATE TABLE `Python_Employee` ( `id` INT NOT NULL , `name` TEXT NOT NULL , `photo` LONGBLOB NOT NULL , `biodata` LONGBLOB NOT NULL , PRIMARY KEY (`id`))")
query = ("select * from Python_Employee")

cursor.execute(query)

for something in cursor:
    print(something)

cnx.commit()
cnx.close()
