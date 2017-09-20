def showTables(dbName):
    return "SHOW TABLES IN " + dbName


def showCreateTable(tableName):
    return "SHOW CREATE TABLE " + tableName + "\n"

def showCreateFunction(funcName):
    return "SHOW CREATE FUNCTION " + funcName + "\n"

def showFunctions():
    return "SHOW FUNCTION STATUS"