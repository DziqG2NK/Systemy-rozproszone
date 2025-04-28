import grpc
import communication_pb2
import communication_pb2_grpc


def run():
    channel = grpc.insecure_channel('127.0.0.1:50000')
    stub = communication_pb2_grpc.EventServiceStub(channel)

    # Wysyłamy zapytanie o subskrypcję
    category = communication_pb2.Category.GAMING
    request = communication_pb2.SubscribeMessage(category=category)

    # Strumieniowe odbieranie wiadomości
    for event in stub.Subscribe(request):
        print(f"Received event: {event.event}")


if __name__ == '__main__':
    run()
