import grpc
import time
from concurrent import futures
import communication_pb2
import communication_pb2_grpc

# Implementacja serwera
class EventService(communication_pb2_grpc.EventServiceServicer):
    def Subscribe(self, request, context):
        topics = ["weather", "sports", "music"]  # Przykładowe tematy
        for topic in topics:
            # Wysyłanie powiadomień do klienta
            event_message = f"New event in topic: {topic}"
            yield communication_pb2.EventMessage(event=event_message)
            time.sleep(1)  # symulacja przerwy między wiadomościami

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    communication_pb2_grpc.add_EventServiceServicer_to_server(EventService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Serwer uruchomiony na porcie 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
