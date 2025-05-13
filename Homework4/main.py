from colorama import Fore, Style
import ray
from storagenode import StorageNode

@ray.remote
class NameNode():
    def __init__(self, storagesNumber, chunksNumber, chunkSize, copiesNumber):
        self.copiesNumber = copiesNumber
        self.storages = {}
        self.artefacts = {}
        self.artefactsLengths = {}
        self.chunkSize = chunkSize

        for i in range(storagesNumber):
            self.storages[i] = StorageNode.remote(i, chunksNumber, False)

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
                ray.get(self.storages[i].destoreArtefact.remote(list[i]))

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

                if ray.get([storage.isFull.remote() for storage in self.storages.values()]).count(False) == 0:
                    print("No space left, removing artefact")
                    self.removeArtefact(fileName)
                    return

                chunkInStorage = ray.get(self.storages[i % n].storeArtefact.remote(artefactPart))

                if chunkInStorage is not None:
                    self.artefacts[fileName].append([i % n, chunkInStorage])

                i += 1

    def modifyArtefact(self, fileName, newArtefact):
        self.removeArtefact(fileName)
        self.storeArtefact(fileName, newArtefact)

    def printAll(self):
        storagesState = ""

        for storage in self.storages.values():
            storagesState += ray.get(storage.storageInfo.remote())

        for artefacts in self.artefacts:
            print(artefacts)
            print(self.artefacts[artefacts])

        print(storagesState)

    def readArtefact(self, fileName):
        if fileName in self.artefacts:
            n = self.artefactsLengths[fileName]
            result = [None for _ in range(n)]

            for i in range(self.copiesNumber):
                for j, [storage, chunk] in enumerate(self.artefacts[fileName]):
                    if ray.get(self.storages[storage].canBeRead.remote()):
                        if result[j % n] == None:
                            result[j % n] =  ray.get(self.storages[storage].getChunkValue.remote(chunk))

            artefact = ""
            try:
                for res in result:
                    artefact = artefact + res

                return artefact

            except TypeError as e:
                print(e)
                print("Error reading artefact")

        else:
            print(f"No record like {fileName} in base")

    def damageStorage(self, storage):
        self.storages[storage].damageStorage.remote()

    def repairStorage(self, storage):
        self.storages[storage].repairStorage.remote()

def main():
    ray.init()

    storagesNumber = int(input("Podaj ilość NodeStorage'y: "))
    chunksNumber = int(input("Ilość chunków na Storage: "))
    chunkSize = int(input("Długość stringa w chunku "))
    nn = NameNode.remote(storagesNumber,chunksNumber,chunkSize, 3)

    while True:
        print("\nDostępne operacje:")
        print("1 - Dodaj artefakt")
        print("2 - Podejrzyj storage")
        print("3 - Odczytaj artefakt (niezaimplementowane)")
        print("4 - Usuń artefakt")
        print("5 - Zmień artefakt")
        print("6 - Uszkodź storage")
        print("7 - Napraw storage")
        print("8 - Wyjdź")

        choice = input("Wybierz opcję (1-8): ")

        if choice == "1":
            fileName = input("Podaj nazwę artefaktu: ")
            data = input("Podaj zawartość artefaktu: ")
            ray.get(nn.storeArtefact.remote(fileName, data))

        elif choice == "2":
            ray.get(nn.printAll.remote())

        elif choice == "3":
            fileName = input("Podaj nazwę artefaktu: ")
            read_artefact = ray.get(nn.readArtefact.remote(fileName))
            if read_artefact != None:
                print(read_artefact)
            pass


        elif choice == "4":
            fileName = input("Podaj nazwę artefaktu do usunięcia: ")
            ray.get(nn.removeArtefact.remote(fileName))

        elif choice == "5":
            fileName = input("Podaj nazwę artefaktu do zmiany: ")
            newData = input("Podaj nową zawartość: ")
            ray.get(nn.modifyArtefact.remote(fileName, newData))

        elif choice == "6":
            try:
                storage = int(input("Podaj numer storage'u do uszkodzenia: "))
                ray.get(nn.damageStorage.remote(storage))
                print(f"Uszkodzono storage {storage}")
            except Exception as e:
                print(e)
                print("Coś poszło nie tak")

        elif choice == "7":
            try:
                storage = int(input("Podaj numer storage'u do naprawy: "))
                ray.get(nn.repairStorage.remote(storage))
                print(f"Naprawiono storage {storage}")
            except Exception as e:
                print(e)
                print("Coś poszło nie tak")

        elif choice == "8":
            print("Zamykanie programu.")
            break

        else:
            print("Nieznana opcja, spróbuj ponownie.")

    ray.shutdown()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # # print_hi('PyCharm')

    # node = NameNode(5,5, 5, 3)
    # # print(node.divideArtefact("To jest jakiś przykładowy string !ddd"))
    # node.printAll()
    # node.storeArtefact("Przykład","To jest jakiś przykładowy string !ddd")
    # node.printAll()
    # node.damageStorage(1)
    # node.printAll()
    #
    # print(node.readArtefact("Przykład"))
    # node.modifyArtefact("Przykład", "NIC W SUMIE CIEKAWEGO")
    # node.printAll()
    # node.damageStorage(3)
    # print(node.readArtefact("Przykład"))

    # print("NFHDSKFB" + None)

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
