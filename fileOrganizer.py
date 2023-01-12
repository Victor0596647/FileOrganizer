import os, shutil, json
from stat import *

# The config file
jsonPath = "filterConfig.json"

def fileChecker(path: str) -> dict[str, list[dict[str, str]]]:
    fileList = {"files":[]}
    try:
        for f in os.listdir(path):
            pathname = os.path.join(path, f)
            fileList["files"].append(checkFileExt(pathname))
        return (fileList)
    except FileNotFoundError:
        print("Please make sure your path leads to an existing directory. Could not find path specified: '"+ path +"'")
        exit()

# Checks the file type and returns a list [filetype, filename, shortpath, extension]
def checkFileExt(filename: str) -> dict[str, str] | None:
    mode = os.lstat(filename).st_mode
    shortPath = filename.rsplit("\\", 1)[1]
    if S_ISDIR(mode):
        fileInfo = {
            "fileType": "dir",
            "shortPath": shortPath,
            "fileExt": ""
        }
        return (fileInfo)
    if S_ISREG(mode):
        # Checks if file has an extension
        try:
            fileExt = shortPath.rsplit(".", 1)[1]
        except IndexError:
            fileExt = ""
        fileInfo = {
            "fileType": "file",
            "fileName": shortPath.rsplit(".", 1)[0],
            "shortPath": shortPath,
            "fileExt": fileExt
        }
        return (fileInfo)

# File filter functions that organizes and returns a dict list with each of them having their destination folder
def fileFilter(fileList: dict[str, list[dict[str,str]]], dirJson: dict) -> dict[str, list[dict]]:
    organizedList = {"fileDestination": []}
    fileExcepts = []
    for file in fileList['files']:
        # Skips if it is a directory
        if file['fileType'] != "file":
            #print(f"directory detected for {file['shortPath']}, skipping...")
            continue
        isException = False
        # File Exclusion Handling
        def addToExc(file: dict[str,str]):
            #print(f'Found an exception for {file["shortPath"]}')
            fileExcepts.append(file["shortPath"])
            isException = True
        
        for fileExc in dirJson["fileExcepts"]:

            if fileExc.rfind(".") != -1:
                splitExt = fileExc.rsplit(".", 1)
                # If statements when an '*' is involved
                if splitExt[0] == "*" or splitExt[1] == "*":
                    if splitExt[0] == "*" and splitExt[1] == "*":
                        addToExc(file)
                        break
                    elif splitExt[0] == '*' and splitExt[1] != '*':
                        if splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2:
                            nameSearch = splitExt[1].strip("`")
                            if file['fileExt'].find(nameSearch) != -1:
                                addToExc(file)
                                break
                        if file['fileExt'] == splitExt[1]:
                            addToExc(file)
                            break

                    elif splitExt[1] == '*' and splitExt[0] != '*':
                        if splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2:
                            nameSearch = splitExt[0].strip("`")
                            if file['fileName'].find(nameSearch) != -1:
                                addToExc(file)
                                break
                        if file['fileExt'] == splitExt[1]:
                            addToExc(file)
                            break

                # If statements when '` `' are involved
                elif (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) or (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                    if (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) and (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                        nameSearch1 = splitExt[0].strip("`")
                        nameSearch2 = splitExt[1].strip("`")
                        if file['fileName'].find(nameSearch1) != -1 and file['fileExt'].find(nameSearch2) != -1:
                            addToExc(file)
                            break
                    elif (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) and not (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                        nameSearch = splitExt[0].strip("`")
                        if file['fileName'].find(nameSearch) != -1 and file['fileExt'] == splitExt[1]:
                            addToExc(file)
                            break
                    elif (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2) and not (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2):
                        nameSearch = splitExt[1].strip("`")
                        if file['fileExt'].find(nameSearch) != -1 and file['fileName'] == splitExt[0]:
                            addToExc(file)
                            break

                elif splitExt[0] == file['fileName'] and splitExt[1] == file['fileExt']:
                    addToExc(file)
                    break

            elif file['fileExt'] == fileExc:
                addToExc(file)
                break

            elif fileExc == "*":
                addToExc(file)
                break

        def addToList(jsonValue):
            # Searches for any matching objects and checks if it can be moved
            movable = True
            for filel in organizedList["fileDestination"]:
                if filel['fileInfo'] == jsonValue['fileInfo']:
                    #print(f"Couldn't organize {filel['fileInfo']} because the same file already has been sorted, skipping...")
                    movable = False
                    break
            if movable is True:
                organizedList["fileDestination"].append(jsonValue)
                #print(jsonValue)

        if isException is False:
            # File Filter handling
            for filter in dirJson["folderFilter"]:
                for ext in filter["exts"]:
                    if ext.rfind(".") != -1:
                        splitExt = ext.rsplit(".", 1)
                        # If statements when an '*' is involved
                        if splitExt[0] == "*" or splitExt[1] == "*":
                            if splitExt[0] == "*" and splitExt[1] == "*":
                                addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                break
                            elif splitExt[0] == '*' and splitExt[1] != '*':
                                if splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2:
                                    nameSearch = splitExt[1].strip("`")
                                    if file['fileExt'].find(nameSearch) != -1:
                                        addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                        break
                                if file['fileExt'] == splitExt[1]:
                                    addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                    break

                            elif splitExt[1] == '*' and splitExt[0] != '*':
                                if splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2:
                                    nameSearch = splitExt[0].strip("`")
                                    if file['fileName'].find(nameSearch) != -1:
                                        addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                        break
                                if file['fileExt'] == splitExt[1]:
                                    addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                    break

                        # If statements when '` `' are involved
                        elif (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) or (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                            if (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) and (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                                nameSearch1 = splitExt[0].strip("`")
                                nameSearch2 = splitExt[1].strip("`")
                                if file['fileName'].find(nameSearch1) != -1 and file['fileExt'].find(nameSearch2) != -1:
                                    addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                    break
                            elif (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2) and not (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2):
                                nameSearch = splitExt[0].strip("`")
                                if file['fileName'].find(nameSearch) != -1 and file['fileExt'] == splitExt[1]:
                                    addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                    break
                            elif (splitExt[1].startswith("`") and splitExt[1].endswith("`") and splitExt[1].count("`") == 2) and not (splitExt[0].startswith("`") and splitExt[0].endswith("`") and splitExt[0].count("`") == 2):
                                nameSearch = splitExt[1].strip("`")
                                if file['fileExt'].find(nameSearch) != -1 and file['fileName'] == splitExt[0]:
                                    addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                                    break
                        elif splitExt[0] == file['fileName'] and splitExt[1] == file['fileExt']:
                            addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                            break
                    elif file['fileExt'] == ext:
                        addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                        break
                    elif ext == "*":
                        addToList({"fileInfo": file, "dest": f'{dirJson["path"]}\\{filter["name"]}'})
                        break
    #print(organizedList)
    print(f"file exclusions {fileExcepts}")
    return (organizedList)

def fileOrganize(dirJson: dict) -> None:
    path = dirJson["path"]
    fileList = fileChecker(path)
    print("Organizing files...")
    organizedList = fileFilter(fileList, dirJson)
    print("starting to move files")
    for fil in organizedList["fileDestination"]:
        try:
            os.mkdir(os.path.join(fil["dest"]), 0o666)
            print(f"Created new directory '{fil['dest']}'")
            shutil.move(path + "\\" + fil["fileInfo"]["shortPath"], fil['dest'], shutil.copy)
            print(path + "\\" + fil["fileInfo"]["shortPath"] + " Moved to " + fil['dest'])
        except FileExistsError:
            try:
                shutil.move(path + "\\" + fil["fileInfo"]["shortPath"], fil['dest'], shutil.copy)
                print(path + "\\" + fil["fileInfo"]["shortPath"] + " Moved to " + fil['dest'])
            except shutil.Error:
                print(f"{fil['fileInfo']['shortPath']} already exists in {fil['dest']}")

# Main Excecution
def main() -> None:
    with open(jsonPath, "r") as f:
        try:
            filecfg = json.load(f)
            for loc in filecfg["locations"]:
                filePath = loc["path"]
                print(f"Now filtering path: '{filePath}'")
                try:
                    fileOrganize(loc)
                except PermissionError as perm:
                    print(f"There was an error when moving files in '{filePath}' maybe try running as admin. Error: {perm}")
                    continue
        except json.JSONDecodeError as e:
            print(f"The {jsonPath} configuration file has some syntax errors, please fix them.\n Error Log: {e}")

if __name__ == "__main__":
    main()