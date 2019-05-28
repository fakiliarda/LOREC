import mysql.connector

cnx = mysql.connector.connect(user='ardafakili', password='lorec',
                              host='34.65.17.107',
                              database='lorecdb')

cursor = cnx.cursor(buffered=True)
#query = ('INSERT INTO user (username,email,password,GlassNameDbid) values ("arda", "ardafakili@gmail.com","123123",1);')
#query = ('SELECT * from user')
#query = ('show tables')
#query = ('show columns from faces')
#query = ('select * from facetags')
query = ('delete from faces')
#query = ('ALTER TABLE faces ADD COLUMN isRecieved INT AFTER photo')
#query = ('insert into faces (isRecieved) values (0)')
#query = ('update faces set isRecieved=0 where id=1')
#query = ('select id from faces where isRecieved=1')

cursor.execute(query)
result=""
#result=cursor.fetchall()

if not result:
    print("Nothing in cursor")
else:
    for something in result:
        print(something)


#query = ('INSERT INTO user (username,email,password,GlassNameDbid) values ("arda5", "ardafakili@gmail.com","123123",1);')
#cursor.execute(query)
cnx.commit()

query = ('delete from facetags')
cursor.execute(query)
cnx.commit()


#query = ('SELECT * from user')
#cursor.execute(query)
#result=cursor.fetchall()

#if not result:
#    print("Nothing in cursor")
#else:
#    print(result[0][0])
cnx.close()
