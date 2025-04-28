from random import randint
import grpc
import time
import keyboard
import threading
import sys
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

clients = {}
subscribers = {}

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
    # print(new_value, old_value)
    return f"Firma {name} ma wartość {new_value}.00 PLN\n" + (f"Wzrost notowań o {round((new_value - old_value) / old_value, 2)} %" if (new_value - old_value) > 0
     else f"Spadek notowań o {round((new_value - old_value) / old_value, 2)} %")


class EventService(communication_pb2_grpc.EventServiceServicer):
    def Subscribe(self, request, context):
        client_id = str(context.peer())
        if client_id not in subscribers:
            subscribers[client_id] = []

        category = ""
        match request.category:
            case communication_pb2.Category.GAMING:
                category = "gaming"
            case communication_pb2.Category.BANKS:
                category = "banks"
            case communication_pb2.Category.INDUSTRY:
                category = "industry"
            case _:
                print(f"Klient nie wybrał żadnej obecnej kategorii")
                yield communication_pb2.EventMessage(event="Nie zasubskrybowano! \n Nie wybrano odpowiedniej kategorii. \n Wybierz [GAMING|BANKS|INDUSTRY]")

        if category != "":
            subscribers[client_id].append(request.category)
            print(f"Klient {client_id} subskrybuje kategorię {category}")
            yield communication_pb2.EventMessage(event=f"Zasubskrybowano kategorię {category}")

        try:
            while True:
                time.sleep(1)
        except grpc.RpcError:
            print(f"Klient {client_id} zakończył subskrypcję.")
            subscribers[client_id].remove(request.category)
            if not subscribers[client_id]:
                del subscribers[client_id]

    def SendInfo(self, request, context):
        while True:
            if len(subscribers) > 0:
                print("Wysyłanie informacji...")

                for subscriber_categories in subscribers.values():
                    updates = []

                    for category in subscriber_categories:
                        print(category)

                    # Iterujemy po każdej firmie w kategorii
                    for category, buissness_list in buissnesses.items():
                        for buissness in buissness_list:
                            old_value, new_value = buissness.update_value()
                            update = communication_pb2.BuissinessUpdate(
                                name=buissness.name,
                                old_value=old_value,
                                new_value=new_value
                            )
                            updates.append(update)

                    # Wysyłamy BuissinessUpdates do subskrybentów
                    yield communication_pb2.BuissinessUpdates(updates=updates)


            max_range = 6
            for i in range(max_range):
                print(f"{i + 1} / {max_range} sekund...")
                time.sleep(1)


def end_server():
    print("NACIŚNIJ [q] PRZYCISK ABY WYJŚĆ")
    while True:
        if keyboard.is_pressed("q"):
            print("Serwer kończy działanie...")
            # exit()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_EventServiceServicer_to_server(EventService(), server)
    server.add_insecure_port('127.0.0.1:50000')
    server.start()
    print("Serwer nasłuchuje na porcie 50000...")
    server.wait_for_termination()

def update_buissnesses():
    while True:
        updates = []
        for category in buissnesses:
            for buissness in buissnesses[category]:
                buissness.update_value()
                updates.append(create_update_message(buissness.name, buissness.value, buissness.new_value))

        # for message in updates:
        #     print(message)

        max_range = 6
        for i in range(max_range):
            # print(f"{i+ 1} / {max_range} sekund...")
            time.sleep(1)

def send_info_to_subscribers():
    print("NHFDJFBS")
    while True:
        if len(subscribers) > 0:
            print("Wysyłanie informacji...")
            for subscriber_categories in subscribers.values():
                print(subscriber_categories)
                # yield communication_pb2.BuissinessUpdates()

        max_range = 6
        for i in range(max_range):
            print(f"{i + 1} / {max_range} sekund...")
            time.sleep(1)


def start_threads():
    turning_off_thread = threading.Thread(target=end_server)
    turning_off_thread.daemon = True
    turning_off_thread.start()

    # Uruchomienie serwera
    server_thread = threading.Thread(target=serve)
    server_thread.daemon = True
    server_thread.start()

    # Uruchomienie funkcji do wysyłania informacji
    notifying_thread = threading.Thread(target=send_info_to_subscribers)
    notifying_thread.daemon = True
    notifying_thread.start()

    while True:
        time.sleep(1)  # Utrzymujemy główny wątek żywy

if __name__ == '__main__':
    start_threads()
    serve()




    # updating_thread = threading.Thread(target=update_buissnesses)
    # updating_thread.daemon = True
    # updating_thread.start()
    #
    #
    # print("NHFKDSBHFJ")
    # notifying_thread = threading.Thread(target=send_info_to_subscribers)
    # notifying_thread.daemon = True
    # notifying_thread.start()
    #
    # serve()

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
