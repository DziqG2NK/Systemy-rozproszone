import grpc
import communication_pb2
import communication_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = communication_pb2_grpc.EventServiceStub(channel)

    # Wysyłamy zapytanie o subskrypcję
    request = communication_pb2.SubscribeMessage(topic="weather")

    # Strumieniowe odbieranie wiadomości
    for event in stub.Subscribe(request):
        print(f"Received event: {event.event}")


if __name__ == '__main__':
    run()
