import grpc
import communication_pb2
import communication_pb2_grpc

def run():
    # Tworzenie kanału połączenia z serwerem
    channel = grpc.insecure_channel('127.0.0.1:50000')

    # Tworzenie stub'a do komunikacji z serwisem NotificationService
    stub = communication_pb2_grpc.NotificationServiceStub(channel)

    # Tworzymy wiadomość subskrypcji (kategoria: GAMING)
    subscribe_message = communication_pb2.SubscribeMessage(category=communication_pb2.GAMING)

    # Subskrybujemy (wysyłamy SubscribeMessage i odbieramy strumień odpowiedzi)
    try:
        print("Subskrybujemy aktualizacje dla kategorii GAMING...")
        for response in stub.Subscribe(subscribe_message):
            print("Otrzymano aktualizację:")
            print(response)
    except grpc.RpcError as e:
        print(f"Błąd RPC: {e}")

if __name__ == '__main__':
    run()
