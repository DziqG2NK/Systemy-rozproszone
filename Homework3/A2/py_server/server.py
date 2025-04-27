from random import randint
import grpc
from concurrent import futures
import time
import random


class BuissnessClass():
    def __init__(name, value, self):
        self.name = name
        self.value = None
        self.new_value = value

    def update_value(self):
        diff = randint(-10, 10)
        self.value = self.new_value
        self.new_value = self.value + diff

        return self.value, self.new_value

class BuissnessServer():
    def __init__(self):
        

buissnesses = {
    "gaming": [
        BuissnessClass("CDProject", 1000000),
        BuissnessClass("Techland", 737888),
        BuissnessClass("Mojang", 2000004)
    ],
    "banks": [
        BuissnessClass("Pekao S.A.", 500000),
        BuissnessClass("PKO Bank Polski", 1000000),
        BuissnessClass("MBank", 800000),
        BuissnessClass("ING", 600000)
    ],
    "industry": [
        BuissnessClass("KGHM", 2000000),
        BuissnessClass("PGNiG", 1500000),
        BuissnessClass("PKP", 1200000),
        BuissnessClass("LOT", 800000)
    ]
}

def serve():
    address = "127.0.0.1:50000"
    print(f"Server listening on {address}...")

    clients = {}

if __name__ == "__main__":
    serve()