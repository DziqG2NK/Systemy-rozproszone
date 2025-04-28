# from random import randint
# import grpc
# from concurrent import futures
# import time
#
# # imports from proto files
# import communication_pb2
# import communication_pb2_grpc
#
# class BuissnessClass():
#     def __init__(name, value, self):
#         self.name = name
#         self.value = None
#         self.new_value = value
#
#     def update_value(self):
#         diff = randint(-10, 10)
#         self.value = self.new_value
#         self.new_value = self.value + diff
#
#         return self.value, self.new_value
# #
# # class BuissnessServer():
# #     def __init__(self):
#
# buissnesses = {
#     "gaming": [
#         BuissnessClass("CDProject", 1000000),
#         BuissnessClass("Techland", 737888),
#         BuissnessClass("Mojang", 2000004)
#     ],
#     "banks": [
#         BuissnessClass("Pekao S.A.", 500000),
#         BuissnessClass("PKO Bank Polski", 1000000),
#         BuissnessClass("MBank", 800000),
#         BuissnessClass("ING", 600000)
#     ],
#     "industry": [
#         BuissnessClass("KGHM", 2000000),
#         BuissnessClass("PGNiG", 1500000),
#         BuissnessClass("PKP", 1200000),
#         BuissnessClass("LOT", 800000)
#     ]
# }
#
# clients = {}
# subscribers = {}
#
# def create_update_message(name, old_value, new_value):
#     return f"The company {name} now has {new_value}.00 PLN\n" + (f"Wzrost notowań o {(new_value - old_value) / old_value}.00 %" if new_value - old_value > 0
#      else f"Spadek notowań o {(new_value - old_value) / old_value}.00 %")
#
# def inform_about_update():
#     while True:
#
#         for context, categories in list(subscribers.items()):
#             updates = {
#                 "gaming": [],
#                 "banks": [],
#                 "industry": []
#             }
#
#             for category in categories:
#                 for company in category:
#                     old_value, new_value = company.update_value()
#                     updates[category].append(create_update_message(company.name, old_value, new_value))
#
#             if updates:
#                 try:
#                     context.send_message(BuissnessUpdates(updates=updates))
#                 except grpc.RpcError:
#                     print("Błąd wysyłania - czyszczę klienta")
#                     if context in subscribers:
#                         del subscribers[context]
#
#         time.sleep(2)
#
#
# def serve():
#     address = "127.0.0.1:50000"
#     print(f"Server listening on {address}...")
#
#     clients = {}
#
# if __name__ == "__main__":
#     # serve()
#     while True:
#         update_randomly()

from random import randint
import grpc
from concurrent import futures
import time

# imports from proto files
import communication_pb2
import communication_pb2_grpc

class BuissnessClass():
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.new_value = value

    def update_value(self):
        diff = randint(-10, 10)
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

clients = {}
subscribers = {}

def create_update_message(name, old_value, new_value):
    return f"The company {name} now has {new_value}.00 PLN\n" + (f"Wzrost notowań o {(new_value - old_value) / old_value}.00 %" if new_value - old_value > 0
     else f"Spadek notowań o {round((new_value - old_value) / old_value, 4)}.00 %")

def inform_about_update():
    while True:
        for context, categories in list(subscribers.items()):
            updates = {
                "gaming": [],
                "banks": [],
                "industry": []
            }

            for category in categories:

                companies = buissnesses.get(category, [])
                print(companies)
                for company in companies:
                    print(company)
                    old_value, new_value = company.update_value()
                    updates[category].append(create_update_message(company.name, old_value, new_value))

            if updates:
                try:
                    context.send_message(communication_pb2.BuissnessUpdates(updates=updates))
                except grpc.RpcError:
                    print("Błąd wysyłania - czyszczę klienta")
                    if context in subscribers:
                        del subscribers[context]

        time.sleep(2)

# Implementacja serwisu gRPC
class NotificationService(communication_pb2_grpc.NotificationServiceServicer):
    def Subscribe(self, request, context):
        category = request.category.name
        if context not in subscribers:
            subscribers[context] = []
        if category not in subscribers[context]:
            subscribers[context].append(category)

        print(f"Client subscribed to {category} category.")
        return communication_pb2.BuissnessUpdates()

    def Unsubscribe(self, request, context):
        category = request.category.name
        if context in subscribers and category in subscribers[context]:
            subscribers[context].remove(category)
            print(f"Client unsubscribed from {category} category.")
        return communication_pb2.Void()

def serve():
    address = "127.0.0.1:50000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(), server)
    server.add_insecure_port(address)
    server.start()
    print(f"Server listening on {address}...")

    inform_about_update()

if __name__ == "__main__":
    serve()

    # while True:
    #
    #     updates = {
    #         "gaming": [],
    #         "banks": [],
    #         "industry": []
    #     }
    #
    #     # print(buissnesses)
    #     for category in buissnesses:
    #         # print(type(category), category)
    #         companies = buissnesses.get(category)
    #         print(type(companies), companies)
    #         for company in companies:
    #             print(type(company), company)
    #             old_value, new_value = company.update_value()
    #             updates[category].append(create_update_message(company.name, old_value, new_value))
    #             print(create_update_message(company.name, old_value, new_value))
    #
    #     if updates:
    #         # try:
    #         #     context.send_message(communication_pb2.BuissnessUpdates(updates=updates))
    #         # except grpc.RpcError:
    #         #     print("Błąd wysyłania - czyszczę klienta")
    #         #     if context in subscribers:
    #         #         del subscribers[context]
    #         pass
    #
    #     time.sleep(2)
