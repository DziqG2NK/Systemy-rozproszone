from colorama import Fore, Style
import ray

class NameNode():
    def __init__(self, chunks):
        self.chunks = chunks
        self.artefact = ""

@ray.remote
class StorageNode():
    def __init__(self, storageNumber, chunksNumber, isDamaged):
        self.storageNumber = storageNumber
        self.chunksNumber = chunksNumber
        self.isDamaged = isDamaged
        self.chunks = {}

        for i in range(chunksNumber):
            self.chunks[i] = ""

    def operationInfo(self, operation, hasSucceded):
        if hasSucceded:
            print("STORAGE INFO: Operation " + Fore.BLUE + operation + Fore.WHITE + " has " + Fore.GREEN + "SUCCEEDED")
        if not hasSucceded:
            print("STORAGE INFO: Operation " + Fore.BLUE + operation + Fore.WHITE + " has " + Fore.RED + "FAILED")
        print(Style.RESET_ALL)

    def storageInfo(self):
        if not self.isDamaged:
            print(Fore.BLUE + f"Storage number {self.storageNumber} actual status:")
            for key in self.chunks:
                print(f"Chunk {str(key)}: {self.chunks[key]}")
                print()

        else:
            print(Fore.BLUE + f"Storage number {self.storageNumber} is damaged!")
            print()

    def isChunkFree(self, chunkNumber):
        return self.chunks[chunkNumber] == ""

    def isStorageFull(self):
        for key in self.chunks:
            if self.isChunkFree(key):
                return False

        return True

    def damageChunk(self):
        self.isDamaged = True

    def repairChunk(self):
        self.isDamaged = False

    def storageArtefactPart(self, artefact):
        operation = "of storing artefact"
        for key in self.chunks:
            if self.isChunkFree(key):
                self.chunks[key] = artefact
                self.operationInfo(operation, True)
                break
        else:
            self.operationInfo(operation, False)
            return False

    def destoreArtefact(self, listOfChunks):
        operation = "of desotring artefact"

        try:
            for chunkNumber in listOfChunks:
                self.chunks[chunkNumber] = ""

            self.operationInfo(operation, True)
            return True

        except IndexError:
            self.operationInfo(operation, False)
            return False

    def getChunkValue(self, chunkNumber):
        return self.chunks[chunkNumber]

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
