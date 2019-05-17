import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
def readBLOB(emp_id, photo, bioData):
    print("Reading BLOB data from Python_Employee table")
    try:
        connection = mysql.connector.connect(user='root', password='aey.1996',
                              host='34.65.17.107',
                              database='lorecdb')
        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from Python_Employee where id = %s"""
        cursor.execute(sql_fetch_blob_query, (emp_id, ))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            image =  row[2]
            file = row[3]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, photo)
            write_file(file, bioData)
    except mysql.connector.Error as error :
        connection.rollback()
        print("Failed to read BLOB data from MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
readBLOB(1, "C:/Users/Arda/Desktop/HDD/SendAndRetrieve/retrieved2.jpg", "C:/Users/Arda/Desktop/HDD/SendAndRetrieve/retrieved2.txt")
#readBLOB(2, "D:\Python\Articles\my_SQL\query_output\scott_photo.png", "D:\Python\Articles\my_SQL\query_output\scott_bioData.txt")
