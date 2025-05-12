from colorama import Fore, Style
import ray
from storagenode import StorageNode

# @ray.remote
class NameNode():
    def __init__(self, storagesNumber, chunksNumber, chunkSize):
        self.storages = {}
        self.artefacts = {}
        self.chunkSize = chunkSize

        for i in range(storagesNumber):
            self.storages[i + 1] = StorageNode(i, chunksNumber, False)

    def divideArtefact(self, artefact):
        return [artefact[i : i + self.chunkSize] for i in range(0, len(artefact), self.chunkSize)]

    def isStored(self, fileName):
        return fileName in self.artefacts

    def removeArtefact(self, fileName):
        locations = self.artefacts[fileName]

        for key in locations:
            storageChunks = locations[key]
            self.storages[key].destoreArtefact(storageChunks)

    def storeArtefact(self, fileName, artefact):
        self.artefacts[fileName] = {}

        dividedArtefact = self.divideArtefact(artefact)
        i = 1
        n = len(self.storages)

        for artefactPart in dividedArtefact:
            print(artefactPart)
            if [storage.isFull() for storage in self.storages.values()].count(False) == 0:
                # print jakis
                print("jakis")
                self.removeArtefact(fileName)
                break

            chunkInStorage = self.storages[(i % n) + 1].storeArtefact(artefactPart)
            if chunkInStorage is not None:
                if chunkInStorage in self.artefacts[fileName]:  # ZMIANA LINII
                    self.artefacts[fileName][chunkInStorage].append(chunkInStorage)  # ZMIANA LINII
                else:
                    self.artefacts[fileName][chunkInStorage] = []  # ZMIANA LINII
                    self.artefacts[fileName][chunkInStorage].append(chunkInStorage)  # ZMIANA LINII

            i += 1

    def printAll(self):
        for storage in self.storages.values():
            storage.storageInfo()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    node = NameNode(5,5, 5)
    # print(node.divideArtefact("To jest jakiś przykładowy string !ddd"))
    node.printAll()
    node.storeArtefact("Przykład","To jest jakiś przykładowy string !ddd")
    node.printAll()

    # Testing StorageNode
    # storage = StorageNode(1, 5, False)
    # storage.storageInfo()
    # storage.storeArtefact("fhbdjs1")
    # storage.storeArtefact("fhbdjs2")
    # storage.storeArtefact("fhbdjs3")
    # storage.storeArtefact("fhbdjs4")
    # storage.storeArtefact("fhbdjs5")
    # storage.storeArtefact("fhbdjs6")
    # storage.storeArtefact("fhbdjs7")
    # storage.storageInfo()
    # storage.damageChunk()
    # storage.storageInfo()
    # storage.storeArtefact("fhbdjs8")
    # storage.storageInfo()
    # storage.repairChunk()
    # storage.storageInfo()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
