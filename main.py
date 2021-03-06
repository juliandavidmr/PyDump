import datetime
import MySQLdb
from credentials import credentials
from queries import showTables, showCreateTable, showFunctions, showCreateFunction
from configs import filename
import utils


def main():
    db = MySQLdb.connect(host=credentials.get("host"),
                         user=credentials.get("user"),
                         passwd=credentials.get("passwd"),
                         db=credentials.get("db"))

    cursor = db.cursor()

    # Create directory
    utils.createFolder(filename.get("folderout"))

    initialDate = datetime.datetime.now()
    genDDLTables(cursor)
    genDDLProcedures(cursor)
    genDDLFunctions(cursor)
    genStatementsInserts(cursor)
    print "[FINISH]", (datetime.datetime.now() - initialDate), "total time."


def genDDLTables(cursor):  # List tables
    cursor.execute(showTables(credentials.get("db")))

    file = open(filename.get("tables"), 'w')

    countTables = cursor.rowcount
    counter = 0
    try:
        for row in cursor.fetchall():
            queryCreateTable = showCreateTable(row[0])
            file.write("-- " + queryCreateTable)

            cursor.execute(queryCreateTable)
            for ddlt in cursor.fetchall():
                file.write(ddlt[1] + ";\n\n")
                # print ddlt[1]
            counter = counter + 1
    except Exception as identifier:
        print "Error", identifier.__str__()

    print "[OK]", counter.__str__(), "of", countTables.__str__(), "tables"
    file.close()


def genDDLFunctions(cursor):  # List tables
    cursor.execute(showFunctions())

    file = open(filename.get("functions"), 'w')

    countFuncs = cursor.rowcount
    counter = 0

    for row in cursor.fetchall():
        try:
            if row[0] == credentials.get("db"):
                queryCreateFunc = showCreateFunction(row[1])
                file.write("-- " + queryCreateFunc)

                cursor.execute(queryCreateFunc)
                for ddlt in cursor.fetchall():
                    file.write(ddlt[2] + ";\n\n")
                counter += 1
            else:
                countFuncs -= 1
        except Exception as identifier:
            print "Error", identifier.__str__()

    print "[OK]", counter.__str__(), "of", countFuncs.__str__(), "functions"
    file.close()


def genDDLProcedures(cursor):
    cursor.execute("SHOW PROCEDURE STATUS")

    file = open(filename.get("procedures"), 'w')

    countProc = cursor.rowcount
    counter = 0
    try:
        for row in cursor.fetchall():
            if row[0] == credentials.get("db"):
                queryCreateProcedure = "SHOW CREATE PROCEDURE  " + \
                    row[1] + "\n"
                file.write("-- " + queryCreateProcedure)

                cursor.execute(queryCreateProcedure)
                for ddlt in cursor.fetchall():
                    file.write(ddlt[2] + ";\n\n")
                    # print ddlt[1]
                counter = counter + 1
            else:
                countProc = countProc - 1
    except Exception as identifier:
        print "Error", identifier.__str__()

    print "[OK]", counter.__str__(), "of", countProc.__str__(), "procedures"
    file.close()


def genStatementsInserts(cursor):
    cursor.execute(showTables(credentials.get("db")))

    file = open(filename.get("inserts"), 'w')

    countTables = cursor.rowcount
    counter = 0
    try:
        for tables in cursor.fetchall():
            queryCreateTable = "SELECT * FROM " + tables[0] + "\n"
            file.write("-- " + queryCreateTable)

            cursor.execute(queryCreateTable)

            utils.ptime("Generating", cursor.rowcount,
                        "inserts for", tables[0])
            for data in cursor.fetchall():
                values = ""
                lengthCountTemp = 0
                lengthTotal = cursor.rowcount
                for val in data:
                    val = val.__str__()
                    lengthCountTemp += 1
                    if val.find('\'') != -1:
                        # print "Encontrado ' en", val
                        val = val.replace('\'', '\\\'')
                    if lengthCountTemp != lengthTotal:
                        values = values + "'" + val.__str__() + "',"
                if values.endswith(','):
                    values = values[:len(values) - 1]

                insert = "INSERT INTO " + \
                    tables[0].__str__() + " VALUES(" + values.__str__() + ")"
                file.write(insert + ";\n")
                # print data[1]
            counter = counter + 1
    except Exception as identifier:
        print "Error", identifier.__str__()

    print "[OK]", counter.__str__(), "of", countTables.__str__(), "inserts"
    file.close()


main()
