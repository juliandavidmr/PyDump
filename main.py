import MySQLdb

credentials = {
    "host": "localhost",
    "user": "root",
    "passwd": "root",
    "db": "moodledistancia"
}

db = None


def main():
    db = MySQLdb.connect(host=credentials.get("host"),
                         user=credentials.get("user"),
                         passwd=credentials.get("passwd"),
                         db=credentials.get("db"))

    cursor = db.cursor()

    genDDLTables(cursor)
    genDDLProcedures(cursor)
    genStatementsInserts(cursor)

# List tables


def genDDLTables(cursor):
    cursor.execute("SHOW TABLES IN " + credentials.get("db"))

    file = open('ddltables.sql', 'w')

    countTables = cursor.rowcount
    counter = 0
    try:
        for row in cursor.fetchall():
            queryCreateTable = "SHOW CREATE TABLE " + row[0] + "\n"
            file.write("-- " + queryCreateTable)

            cursor.execute(queryCreateTable)
            for ddlt in cursor.fetchall():
                file.write(ddlt[1] + ";\n\n")
                # print ddlt[1]
            counter = counter + 1
    except Exception as identifier:
        print "Error", identifier.__str__()
        # pass

    print "[OK]", counter.__str__(), "of", countTables.__str__(), "tables"
    file.close()

def genDDLProcedures(cursor):
    cursor.execute("SHOW PROCEDURE STATUS")

    file = open('ddlprocedures.sql', 'w')

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
        # pass

    print "[OK]", counter.__str__(), "of", countProc.__str__(), "procedures"
    file.close()

def genStatementsInserts(cursor):
    cursor.execute("SHOW TABLES IN " + credentials.get("db"))

    file = open('inserts.sql', 'w')

    countTables = cursor.rowcount
    counter = 0
    try:
        for tables in cursor.fetchall():            
            queryCreateTable = "SELECT * FROM " + tables[0] + "\n"
            file.write("-- " + queryCreateTable)

            cursor.execute(queryCreateTable)

            print "Generating", cursor.rowcount, "inserts for", tables[0]
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
                
                insert = "INSERT INTO " + tables[0].__str__() + " VALUES(" + values.__str__() + ")"
                file.write(insert + ";\n")
                # print data[1]
            counter = counter + 1
    except Exception as identifier:
        print "Error", identifier.__str__()
        # pass

    print "[OK]", counter.__str__(), "of", countTables.__str__(), "inserts"
    file.close()

main()
