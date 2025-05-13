from colorama import Fore, Style
import ray

@ray.remote
class StorageNode():
    def __init__(self, storageNumber, chunksNumber, isDamaged):
        self.storageNumber = storageNumber
        self.chunksNumber = chunksNumber
        self.isDamaged = isDamaged
        self.chunks = {}

        for i in range(chunksNumber):
            self.chunks[i] = ""

    def __operationInfo(self, operation, hasSucceded):
        if hasSucceded:
            print("STORAGE INFO: Operation " + Fore.BLUE + operation + Fore.WHITE + " has " + Fore.GREEN + "SUCCEEDED")
        if not hasSucceded:
            print("STORAGE INFO: Operation " + Fore.BLUE + operation + Fore.WHITE + " has " + Fore.RED + "FAILED")
        print(Style.RESET_ALL)

    def storageInfo(self):
        info = ""

        if not self.isDamaged:
            info += Fore.BLUE + f"Storage number {self.storageNumber} actual status:\n"
            for key in self.chunks:
                info += Style.RESET_ALL + f"Chunk {str(key)}: {self.chunks[key]}\n"
            info += "\n"
        else:
            info += Fore.BLUE + f"Storage number {self.storageNumber} is damaged!\n"
            info += Style.RESET_ALL

        return info

    def __isChunkFree(self, chunkNumber):
        return self.chunks[chunkNumber] == ""

    def damageStorage(self):
        self.isDamaged = True

    def repairStorage(self):
        self.isDamaged = False

    def storeArtefact(self, artefact):
        operation = "of storing artefact"

        for key in self.chunks:
            # print(key)
            if self.__isChunkFree(key):
                self.chunks[key] = artefact
                self.__operationInfo(operation, True)
                # print("fdbhsfbjds", str(key))
                return key
        else:
            self.__operationInfo(operation, False)


    def destoreArtefact(self, listOfChunks):
        operation = "of destoring artefact"

        try:
            for chunkNumber in listOfChunks:
                self.chunks[chunkNumber] = ""

            self.__operationInfo(operation, True)
            return True

        except IndexError:
            self.__operationInfo(operation, False)
            return False

    def getChunkValue(self, chunkNumber):
        if not self.isDamaged:
            return self.chunks[chunkNumber]
        return None

    def isFull(self):
        if not self.isDamaged:
            for key in self.chunks:
                if self.__isChunkFree(key):
                    return False
            else:
                return True

        return True

    def canBeRead(self):
        return not self.isDamaged