from colorama import Fore, Style
import ray
from storagenode import StorageNode

# @ray.remote
class NameNode():
    def __init__(self, storagesNumber, chunksNumber, chunkSize, copiesNumber):
        self.copiesNumber = copiesNumber
        self.storages = {}
        self.artefacts = {}
        self.artefactsLengths = {}
        self.chunkSize = chunkSize

        for i in range(storagesNumber):
            self.storages[i] = StorageNode(i, chunksNumber, False)

    def divideArtefact(self, artefact):
        return [artefact[i : i + self.chunkSize] for i in range(0, len(artefact), self.chunkSize)]

    def isStored(self, fileName):
        return fileName in self.artefacts

    def removeArtefact(self, fileName):
        list = [[] for _ in range(len(self.storages))]
        for [storage, chunk] in self.artefacts[fileName]:
            list[storage].append(chunk)

        print(list)
        for i in range(len(list)):
            if list[i]:
                self.storages[i].destoreArtefact(list[i])

        del self.artefacts[fileName]
        del self.artefactsLengths[fileName]

    # klucz: [pierwszy wyraz [storage, []]]

    def storeArtefact(self, fileName, artefact):
        self.artefacts[fileName] = []

        dividedArtefact = self.divideArtefact(artefact)
        self.artefactsLengths[fileName] = len(dividedArtefact)
        i = 0
        n = len(self.storages)

        for _ in range(self.copiesNumber):

            for artefactPart in dividedArtefact:

                if [storage.isFull() for storage in self.storages.values()].count(False) == 0:
                    print("No space left, removing artefact")
                    self.removeArtefact(fileName)
                    break

                chunkInStorage = self.storages[i % n].storeArtefact(artefactPart)

                if chunkInStorage is not None:
                    self.artefacts[fileName].append([i % n, chunkInStorage])

                i += 1

    def modifyArtefact(self, fileName, newArtefact):
        self.removeArtefact(fileName)
        self.storeArtefact(fileName, newArtefact)

    def printAll(self):
        for storage in self.storages.values():
            storage.storageInfo()

        for artefacts in self.artefacts:
            print(artefacts)
            print(self.artefacts[artefacts])

    def readArtefact(self, fileName):
        n = self.artefactsLengths[fileName]
        result = [None for _ in range(n)]

        for i in range(self.copiesNumber):
            for j, [storage, chunk] in enumerate(self.artefacts[fileName]):
                if self.storages[storage].isFull:
                    if result[j % n] == None:
                        result[j % n] = self.storages[storage].getChunkValue(chunk)

        artefact = ""
        for res in result:
            artefact = artefact + res

        return artefact


def main():
    nn = NameNode(5,5,5)

    while True:
        print("\nDostępne operacje:")
        print("1 - Dodaj artefakt")
        print("2 - Podejrzyj storage")
        print("3 - Odczytaj artefakt (niezaimplementowane)")
        print("4 - Usuń artefakt")
        print("5 - Zmień artefakt")
        print("6 - Wyjdź")

        choice = input("Wybierz opcję (1-6): ")

        if choice == "1":
            fileName = input("Podaj nazwę artefaktu: ")
            data = input("Podaj zawartość artefaktu: ")
            nn.storeArtefact(fileName, data)
        elif choice == "2":
            nn.printStorages()
        elif choice == "3":
            print("Odczyt artefaktu: (niezaimplementowane)")
            pass
        elif choice == "4":
            fileName = input("Podaj nazwę artefaktu do usunięcia: ")
            nn.deleteArtefact(fileName)
        elif choice == "5":
            fileName = input("Podaj nazwę artefaktu do zmiany: ")
            newData = input("Podaj nową zawartość: ")
            nn.updateArtefact(fileName, newData)
        elif choice == "6":
            print("Zamykanie programu.")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    # # print_hi('PyCharm')
    node = NameNode(5,5, 5, 2)
    # print(node.divideArtefact("To jest jakiś przykładowy string !ddd"))
    node.printAll()
    node.storeArtefact("Przykład","To jest jakiś przykładowy string !ddd")
    node.printAll()
    node.modifyArtefact("Przykład", "NIC W SUMIE CIEKAWEGO")
    node.printAll()
    print(node.readArtefact("Przykład"))


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
