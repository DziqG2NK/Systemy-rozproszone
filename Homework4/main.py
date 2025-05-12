from colorama import Fore, Style
import ray

class NameNode():
    def __init__(self, chunks):
        self.chunks = chunks
        self.artefact = ""

# @ray.remote
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
        if not self.isDamaged:
            print(Fore.BLUE + f"Storage number {self.storageNumber} actual status:")
            for key in self.chunks:
                print(Style.RESET_ALL)
                print(f"Chunk {str(key)}: {self.chunks[key]}")
            print()

        else:
            print(Fore.BLUE + f"Storage number {self.storageNumber} is damaged!")
            print(Style.RESET_ALL)

    def __isChunkFree(self, chunkNumber):
        return self.chunks[chunkNumber] == ""

    def damageChunk(self):
        self.isDamaged = True

    def repairChunk(self):
        self.isDamaged = False

    def storeArtefact(self, artefact):
        operation = "of storing artefact"
        for key in self.chunks:
            if self.__isChunkFree(key):
                self.chunks[key] = artefact
                self.__operationInfo(operation, True)
                break
        else:
            self.__operationInfo(operation, False)
            return False

    def destoreArtefact(self, listOfChunks):
        operation = "of desotring artefact"

        try:
            for chunkNumber in listOfChunks:
                self.chunks[chunkNumber] = ""

            self.__operationInfo(operation, True)
            return True

        except IndexError:
            self.__operationInfo(operation, False)
            return False

    def getChunkValue(self, chunkNumber):
        return self.chunks[chunkNumber]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    storage = StorageNode(1, 5, False)
    storage.storageInfo()
    storage.storeArtefact("fhbdjs1")
    storage.storeArtefact("fhbdjs2")
    storage.storeArtefact("fhbdjs3")
    storage.storeArtefact("fhbdjs4")
    storage.storeArtefact("fhbdjs5")
    storage.storeArtefact("fhbdjs6")
    storage.storeArtefact("fhbdjs7")
    storage.storageInfo()
    storage.damageChunk()
    storage.storageInfo()
    storage.storeArtefact("fhbdjs8")
    storage.storageInfo()
    storage.repairChunk()
    storage.storageInfo()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
