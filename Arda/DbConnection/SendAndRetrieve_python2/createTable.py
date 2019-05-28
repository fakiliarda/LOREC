import mysql.connector

cnx = mysql.connector.connect(user='root', password='aey.1996',
                              host='34.65.17.107',
                              database='lorecdb')

cursor = cnx.cursor()
#query = ('INSERT INTO user (username,email,password,GlassNameDbid) values ("arda", "ardafakili@gmail.com","123123",1);')
#query = ("CREATE TABLE `faces` ( `id` INT NOT NULL , `photo` LONGBLOB NOT NULL , PRIMARY KEY (`id`))")
#query = ("CREATE TABLE `facetags` ( `id` INT NOT NULL , `tag` varchar(15) NOT NULL, PRIMARY KEY (`id`))")
#query = ("select * from facetags")
#query = ("delete from faces where id=1")
#query = ('INSERT INTO facetags (id,tag) values (1, "arda");')
#query = ("delete from facetags where id=1")
#query = """ select * from `facetags` where id= 1 """
query = ("select * from faces")


#id=1
#sql_query = """ select * from `facetags` where id="%s" """
#print(sql_query, id)
#sql_result  = cursor.execute(sql_query, id)



cursor.execute(query)

for something in cursor:
    print(something)

cnx.commit()
cnx.close()
	