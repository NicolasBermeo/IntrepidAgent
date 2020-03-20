import os
from datetime import datetime
import mysql.connector as mysql

# --- LOGGING FUNCTIONS ---
'''
    The following functions are used to log device status to a text file or MySQL database.

	log() obtains the current date and time as well as a pre-defined message passed from the poll function.
	It appends each of these to a pre-existing text file each time a camera is marked as offline.
		It does not return any value.
    
	mysql_log() acts similarly to log(), however it contacts a MySQL database to log the same information.
	Note that connection information, including host, user, and password should be modified according
	to the current configuration of the MySQL server. This function will remain commented until use is
	desired, at which point the commenting may be removed.
		It does not return any value.
'''
# -------------------------
def log(msg):

    now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    msg = str(msg)

    with open('./logs/status.log', 'a') as logfile:
        msg = f'[{now}] {msg}\n'
        logfile.write(msg)
        logfile.close()
        
        return

'''
def mysql_log(msg):
	db1 = mysql.connect(
		host="localhost",
		user="root",
		passwd="password")

	mycursor1 = db1.cursor()	
	mycursor1.execute("CREATE DATABASE IF NOT EXISTS cameraLogs")

	db2 = mysql.connect(
		host="localhost",
		user="root",
		passwd="password",
		database="cameraLogs")
		
	mycursor2 = db2.cursor()	
	mycursor2.execute("CREATE TABLE IF NOT EXISTS logs (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, date_time VARCHAR(255), message VARCHAR(255))")
	
	db3 = mysql.connect(
		host="localhost",
		user="root",
		passwd="password",
		database="cameraLogs")
	
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	mycursor3 = db3.cursor()
	mycursor3.execute("""INSERT INTO logs (date_time, message) VALUES (%s, %s)""",(timestamp,msg))
	db3.commit()
	#print(mycursor3.rowcount, "record inserted.")
	return
'''
