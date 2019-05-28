import mysql.connector
import time
from mysql.connector import Error
from mysql.connector import errorcode
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def insertBLOB(id, photo):
    print("Inserting BLOB into faces table")
    try:
        connection = mysql.connector.connect(user='root', password='aey.1996',
                              host='34.65.17.107',
                              database='lorecdb')
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO `faces`
                          (`id`,`photo`) VALUES (%s,%s)"""
        personPicture = convertToBinaryData(photo)
        #Convert data into tuple format
        print('inserting')
        insert_blob_tuple = (id, personPicture)
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        for something in cursor:
           print(something)
        connection.commit()
        print("waiting")
        time.sleep(5)
        sql_query = """ select * from `facetags` where id=%s """
        print(sql_query, id)
        cursor.execute(sql_query, (id, ))
        for something in cursor:
           print(something)
           print('second')
        connection.commit()
		    
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
	print('sendImage.py')