import platform

folderout = "backup"


def preparePath(*dirs):
    if str(platform.platform()).lower() == "windows":
        return "\\".join(dirs)
    else:
        return "/".join(dirs)


filename = {
    "tables": preparePath(folderout, "ddltables.sql"),
    "functions": preparePath(folderout, "ddlfunctions.sql"),
    "procedures": preparePath(folderout, "ddlprocedures.sql"),
    "inserts": preparePath(folderout, "inserts.sql"),
    "folderout": folderout
}
