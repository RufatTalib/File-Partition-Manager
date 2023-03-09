

import os
import queue

class BaseDebug:

    def __init__(self):
        self.Errors = queue.Queue()
        self.Messages = queue.Queue()
    
    def SendError(self, error):
        self.Errors.put(error)
    
    def SendMessage(self, message):
        self.Messages.put(message)

class Environment(BaseDebug):

    def __init__(self):
        super().__init__()
    
    def GetFileNameFromFullPath(self, fullPath):
        return os.path.basename(fullPath)
    
    def GetFileNameAndFormat(self, fullPath):
        return os.path.splitext(self.GetFileNameFromFullPath(fullPath))
    
    def GetDirectoryName(self, fullPath):
        return "Partitions_For_" + self.GetFileNameAndFormat(fullPath)[0]
    
    def GetAllFiles(self, directory):
        return os.listdir(directory)
    
    def GetSeparator(self):
        return os.sep

    def MakeDirectory(self, directoryName):
        try:
            os.mkdir(directoryName)
        except OSError as error:
            self.SendError(error)



class Partition(BaseDebug):
    MAX_PARTITION_POWER = 8

    def __init__(self, targetFileFullPath, partitionSize):
        super().__init__()

        self.targetFileFullPath = targetFileFullPath
        self.partitionSize = partitionSize

        self.environment = Environment()
        self.outputDirectory = self.InitializeOutput(self.environment)

        self.blockCount = -1
        self.pack = 0
    
    def InitializeOutput(self, environment):
        directory = environment.GetDirectoryName(self.targetFileFullPath)

        environment.MakeDirectory(directory)

        return directory

    def GeneratePartitionName(self, directoryName, count):
        filename = directoryName + os.sep + 'Block_' + f"{count}".zfill(self.MAX_PARTITION_POWER)

        self.SendMessage("Working on: " + filename)

        return filename
    
    def GeneratePartition(self):
        self.pack = 0
        self.blockCount += 1
        return open( self.GeneratePartitionName(self.outputDirectory, self.blockCount) , 'wb')
    
    def Generate(self):
        source = open(self.targetFileFullPath, 'rb')

        part = self.GeneratePartition()

        while 1:
            data = source.read(self.partitionSize)

            if not data:
                break

            if self.pack == self.partitionSize:
                part.close()
                part = self.GeneratePartition()
            
            part.write(data)
            self.pack += self.partitionSize
        
        part.close()
        source.close()
    
class Builder(BaseDebug):
    def __init__(self):
        super().__init__()

        self.environment = Environment()
    
    def Build(self, buildFrom, saveAs):
        partNames = self.environment.GetAllFiles(buildFrom)
        
        with open(saveAs, 'wb') as output:

            for partName in partNames:

                filename = buildFrom + self.environment.GetSeparator() + partName

                with open(filename, 'rb') as part:
                    output.write(part.read())
                
                self.SendMessage("Wrote : " + filename)
