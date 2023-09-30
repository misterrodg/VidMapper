import os


class FileHandler:
    def __init__(self):
        self.localPath = os.getcwd()

    def checkPath(self, pathFromRoot: str):
        result = False
        path = self.localPath + "/" + pathFromRoot
        if os.path.exists(path):
            result = True
        return result

    def checkFile(self, filePathFromRoot: str):
        result = False
        filePath = self.localPath + "/" + filePathFromRoot
        if os.path.exists(filePath):
            result = True
        return result

    def checkDir(self, subdirPath: str):
        result = False
        dirPath = self.localPath + "/" + subdirPath
        os.makedirs(name=dirPath, exist_ok=True)
        if os.path.exists(dirPath):
            result = True
        return result

    def deleteAllInSubdir(self, fileType: str, subdirPath: str = ""):
        # As it stands, this will only ever delete items in the named subfolder where this script runs.
        # Altering this function could cause it to delete the entire contents of other folders where you wouldn't want it to.
        # Alter this at your own risk.
        if subdirPath != "":
            deletePath = self.localPath + "/" + subdirPath
            if os.path.exists(deletePath):
                for f in os.listdir(deletePath):
                    if f.endswith(fileType):
                        os.remove(os.path.join(deletePath, f))

    def searchForType(self, fileType: str, subdirPath: str = ""):
        result = []
        searchPath = self.localPath
        if subdirPath != "":
            searchPath += "/" + subdirPath
        for dirpath, subdirs, files in os.walk(searchPath):
            result.extend(
                os.path.join(dirpath, f) for f in files if f.endswith(fileType)
            )
        return result

    def splitFolderFile(self, fullPath: str, subdirPath: str = ""):
        result = []
        split = os.path.split(fullPath)
        searchPath = self.localPath
        if subdirPath != "":
            searchPath += "/" + subdirPath
        result.append(split[0].replace(searchPath, ""))
        result.append(split[1])
        return result
