# Name: Data base class contorler ( db )
# Main Job: This claass should be called whenever you want to read or write to the database
#
# Author: Ali Albahrani
# Craated Date: 30 March 2021
# Version: 1.3.0
# ClassID# 1000

# Class Usage
#   1. Call ConnectToDB function to establish the connection and save the return value of it.
#   2. Use the the return value, if not err, to send your sql either by calling SendSQL or InsertSQL funcions.
#   3. Cloase the connection if you are done using the CloseConnection function

# Database Paramters
#   Add the database paramters in the func_ConnectToDB funcion.

from .ErrorReporting  import ausError as Err
import mysql.connector as mysql
import os
from GamingGeekProj.settings import DEBUG

# Those constent will be return by the function. You can use them to check the respond of the class's funcions
db_OK_RESPOND:str = "OK"
db_NO_DATA_RESPOND:str = "No Data"

# Establish Connection to the database
def func_ConnectToDB():
    # Return: the db connection that can be used to call the other class function OR ErrorReporting object on error
    # mysql://b89f7ac9ae97e7:12576c53@us-cdbr-east-03.cleardb.com/heroku_2c359834c332ed6?reconnect=true
    try:
        if DEBUG:
            mydb = mysql.connect(
            host="localhost",
            user="root",
            password="alibhp110",
            database="gamegeek"
            )
            return mydb
        else:
            mydb = mysql.connect(
            host="eu-cdbr-east-05.cleardb.com",
            user="b8a0b341a60dcd",
            password="0d9569a0",
            database="heroku_3a6af533857122d"
            )
            return mydb

    except:
        return Err(1001, "Database Conneciton", "Problem in the connection to database parameters, Please, make sure you supply the correct database parameters and the SQL server is running.")
#    try:
#        mydb = mysql.connect(
#        host="localhost",
#        user="root",
#        password="alibhp110",
#        database="gamegeek"
#        )
#        return mydb
#    except:
#        return Err(1001, "Database Conneciton", "Problem in the connection to database parameters, Please, make sure you supply the correct database parameters and the SQL server is running.")

# This function simply cut the connection to the database. please used it when you done.
def func_CloseConnection(connection):
    if (connection.is_connected()):
        connection.close()
    return True

# Main SQL request function that will return the result for your SQL statment
# NOTE: Use this function for all SQL except INSERT
def func_SendSQL(myDBin, SQLStatment:str, parameters={}, returnDate=True, returnColumns=False):

    #   -----------------------------------
    # parameters:
    #   myDBin: The return object from the 'ConnectToDB' funcion of this class. This object is must

    #   SQLStatmetn:str, a simple string that tell what is the SQL statment you want to send. The SQL statment must
    #       fallow this Templete "SELECT [whatever] FROM [Whaterver] WHERE [VAR] = %(varName)s AND ... "
    #       This format is to prevent SQL injection secrity issue

    #   parameters:dic, a dictionary array that will map the vars in SQLStatment paramters to thier value.
    #       E.g. SQLStatmetn = "SELECT * FROM `employee` WHERE `empName` like %(inEmpName)s"
    #       para = {"inEmpName": "Ali"}
    #       This is an OPTIONAL parameter

    #   returnData:bool, Is your SQL request will return any data? Normally this is use for the UDPATE sql
    #       True: [default] Yes, this request has some data the should be return
    #       False: No, This request has nothing to return, normaly for UPDATE sqls.
    #       This is an OPTIONAL parameter

    #   returnColumes: bool, Ask the function to return the names of column.
    #       NOTE: This will change the return type to Dic
    #       True: Yes return a dic that have the name of SQL column
    #       False: [default] No, just return an array (list) of data
    #   -----------------------------------
    # Returning:
    #   The return is a 2D  array of all the data found according to the sent SQL statement.
    #   The first index will indicate the Column and the second one will be the record number.
    #   NOTE: If returnColumns is set to TRUE, the return value will be dic, where the column number will be replaced
    #        but the feild name
    #   -----------------------------------

    try:
        # Create a cursor that point to the record aimed to by sql
        mycursor = myDBin.cursor()

        # Exucte the SQL
        mycursor.execute(SQLStatment, parameters)

        if (returnDate):
            # Funcion was asked to return some data
            if returnColumns:
                # Function was asked to return the columns names

                # Get the columns name from the return data
                columnsNames = mycursor.fetchone()
                # Check if we get any column names
                if columnsNames != None:
                    # connected the column names to the return data and return the result
                    row = dict(zip(mycursor.column_names, columnsNames))
                    return row
                else:
                    # No columns names was found, so there is not data to return
                    return db_NO_DATA_RESPOND

            # Return the resulted data
            return mycursor.fetchall()
        else:
            # The SQL statment should not return any data, so for UPDATE, we need to commit the changes
            myDBin.commit()
            return db_OK_RESPOND
    except (mysql.Error, mysql.Warning) as e:
        # Return the error we got
        err = Err(1002, "Database return an error", "The SQL statment submited is not in the correct format or have some error in it. Please check your SQL.")
        err.err_ExtraInfo = e
        return err

# Use this funcion for INSERT sqls only. This funcion can process a single INSERT statement
def func_InsertSQL(Conn, SQLStatment:str, parameters={}, returnID=True):
    #   -----------------------------------
    # Parameters:
    #   Conn: The db connection that can be obtain from SQLConne function of this class
    #   SQLStatment: Same as SQLStatment in the SendSql function of this class.
    #   parameters: Same as SQLStatment in the SendSql function of this class.
    #   returnID: Ask the funcion to return the ID (Primary Key) of the new inserted record
    #       TRUE: [default], Yes, the function should return inserted record ID
    #       FALSE: NO, no need to return that ID
    #   -----------------------------------
    # Return:
    #      Boolean value telling if the SQL run in the right way or not. In Case of the returnID was set to ture,
    #       return value will be str which is the value of the new inserted record in the database
    #   -----------------------------------

    try:
        mycursor = Conn.cursor()
        mycursor.execute(SQLStatment, parameters)
        Conn.commit()

        if returnID:
            lastEnteredID = mycursor.lastrowid
            return [db_OK_RESPOND, str(lastEnteredID)]
        return db_OK_RESPOND

    except (mysql.Error, mysql.Warning) as e:
        # Return the error we got
        err = Err(1002, "Database Insertion error", "The INSERT statment submited had been rejected by the database. Please check your insert statment.")
        err.err_ExtraInfo = e
        return err

    #except:
    #    return Err(1111, "Database Unknown Error.", "We are sorry but unexpected error had happened. Please try again")

# ---------------------------------------------------------------------------------------------------------------------

# This function can be used to create the database from scratch and can be used as well to recreate
# CAUTION: ALL DATA IN DATABASE WILL BE ERASED IF THIS FUNCTION IS USED
# NOTE: COMMIT; statment must be shown at the end of the file once only
def func_CreateDatabase(sqlFileName="austruck.sql"):

    #   -----------------------------------
    # parameters:
    #   sqlFileName: The SQL file that will be used to create the database.
    #   -----------------------------------
    # Return:
    #   N/A

    print("Trying to connect to the database ... ")
    # Esstablish the connection to database
    cnn = func_ConnectToDB()
    if type(cnn) == Err:
        cnn.func_PrintError()
        return
    print("Connection Established")
    print("*"*10)

    # Check for the SQL file
    if os.path.isfile(sqlFileName):
        # File is there, start reading
        sqlFileHandler = open(sqlFileName, "r", encoding="utf8")

        # Read one line
        oneline = sqlFileHandler.readline()

        # Var to hanld one SQL statment of the file
        theSql = ""

        # Start reading the full file
        while oneline != None:

            # Splite the read file inot words
            onelineWords = oneline.split(" ")

            # Check if the first word in the line is interesting and act accordingly
            if onelineWords[0] == "DROP" or onelineWords[0] == "CREATE" or \
                    onelineWords[0] == "INSERT":

                # Add the line to the final SQL statement as one SQL statement contain a number of lines
                theSql = theSql + oneline

                # Check if the statement is complete
                if oneline.find(";")==-1:
                    # Not completed, next lines in the file should complete it
                    oneline = sqlFileHandler.readline()

                    # Read lines until the ";" sample is found
                    while oneline.find(";")==-1:
                        # Add the new line to the final statement
                        theSql = theSql + oneline
                        # read the next line
                        oneline = sqlFileHandler.readline()

                    # The ";" was found as the while loop stopped, add the line to the statement
                    theSql = theSql + oneline

                ################################
                #   SQL statement is ready
                ################################
                print("---------- START ------------------ ")
                print("Running:", theSql)

                # Try to run the sql statment
                r = func_SendSQL(myDBin=cnn,SQLStatment=theSql, returnDate=False)
                # Check the result
                if type(r) is Err:
                    # Error was found, printint out and exit the function
                    r.func_PrintError()
                    return " ------- FINISH ------- "
                else:
                    # No errors
                    print("  Run Succssfully \n")

                # Prepare for the next iteration
                theSql = ""

            elif onelineWords[0] == "--":
                # Comment line, simply ignore
                pass

            elif "COMMIT;" in onelineWords[0]:
                # Reach the end of file, break the while loop
                print("-"*5, "FILE END", "-"*5)
                return

            # Read the next line in the file ( Normally this will start after running one SQL statement )
            oneline = sqlFileHandler.readline()

    else:
        return Err(1010, "SQL file(" + sqlFileName + ") which should be used to create the database was not found or corrupted. The database cannot be created.","please check the file and try again")

def func_displayDatabase():
    cn = func_ConnectToDB()
    tablesNames = func_SendSQL(cn, "SELECT table_name FROM information_schema.tables WHERE table_schema = 'heroku_2c359834c332ed6'")
    for oneTable in tablesNames:
        temp = str(oneTable)
        temp = temp[2:len(temp)-3]
        print("Table (", temp, ")")
        d = func_SendSQL(myDBin=cn, SQLStatment="SELECT * FROM " + temp)
        if type(d) is Err:
            d.func_PrintError()
        else:
            print(d)
        print("---------------------------------------------")