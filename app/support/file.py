from utils import ROOT_DIR
import os
import datetime
import shutil

class FileHandler:
    def createTemporaryDirectory(self):
        temporaryDirectoryPath = ROOT_DIR + '/temp'

        if not os.path.isdir(temporaryDirectoryPath):
            os.makedirs(temporaryDirectoryPath)
        return temporaryDirectoryPath

    def createUserDirectory(self):
        temporaryDirectoryPath = self.createTemporaryDirectory()
        userDirectoryName = f'{datetime.datetime.now():%Y%m%d%H%M%S}'
        userDirectoryPath = temporaryDirectoryPath + '/' + userDirectoryName
        os.makedirs(userDirectoryPath)
        return userDirectoryName

    def uploadFile(self, userDirectoryName, intendedFile):
        filename = intendedFile.filename
        userDirectoryPath = ROOT_DIR +'/temp/'+ userDirectoryName
        intendedFile.save(os.path.join(userDirectoryPath, filename))  
        return userDirectoryPath + '/' + filename

    def deleteDirectory(self, parentDiretoryName ,userDirectoryName):
        try:
            userDirectory = ROOT_DIR +'/' + parentDiretoryName +'/'+ userDirectoryName
            if os.path.isdir(userDirectory):
                shutil.rmtree(userDirectory)
            return True
        except:
            return False     

    def zipDirectory(self, userDirectoryName):
        shutil.make_archive(format = 'zip', root_dir = ROOT_DIR + '/spleeter/temp/' + userDirectoryName, base_name = ROOT_DIR +'/temp/'+userDirectoryName +'/'+userDirectoryName)