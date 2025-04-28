from random import randint
import grpc
import time
from concurrent import futures

# import protofile results
import communication_pb2
import communication_pb2_grpc

class BuissnessClass():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.new_value = value

    def update_value(self):
        diff = randint(-10, 10) * 10000
        self.value = self.new_value
        self.new_value = self.value + diff

        return self.value, self.new_value


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

def create_update_message(name, old_value, new_value):
    print(new_value, old_value)
    return f"The company {name} now has {new_value}.00 PLN\n" + (f"Wzrost notowań o {round((new_value - old_value) / old_value, 2)} %" if (new_value - old_value) > 0
     else f"Spadek notowań o {round((new_value - old_value) / old_value, 2)} %")


class EventService(communication_pb2_grpc.EventServiceServicer):
    def Subscribe(self, request, context):
        if request.category == communication_pb2.Category.GAMING:
            yield communication_pb2.EventMessage(event="Gaming event")
        elif request.category == communication_pb2.Category.BANKS:
            yield communication_pb2.EventMessage(event="Banks event")
        elif request.category == communication_pb2.Category.INDUSTRY:
            yield communication_pb2.EventMessage(event="Industry event")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_EventServiceServicer_to_server(EventService(), server)
    server.add_insecure_port('127.0.0.1:50000')
    server.start()
    print("Server waiting and listening on port 50000...")
    server.wait_for_termination()

def send_updates():
    while True:
        updates = []
        for category in buissnesses:
            for buissness in buissnesses[category]:
                buissness.update_value()
                updates.append(create_update_message(buissness.name, buissness.value, buissness.new_value))

        for message in updates:
            print(message)

        max_range = 6
        for i in range(max_range):
            print(f"{i+ 1} / {max_range} sekund...")
            time.sleep(1)

clients = {}
subscribers = {}

if __name__ == '__main__':
    serve()

    # while True:
    #     updates = []
    #     for category in buissnesses:
    #         for buissness in buissnesses[category]:
    #             buissness.update_value()
    #             updates.append(create_update_message(buissness.name, buissness.value, buissness.new_value))
    #
    #     for message in updates:
    #         print(message)
    #     time.sleep(5)
