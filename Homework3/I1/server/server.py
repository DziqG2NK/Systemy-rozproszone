import Ice, sys
from ToDo import ToDo

class Server(Ice.Application):
    def run(self, args):
        adapter = self.communicator().createObjectAdapterWithEndpoints("LibraryAdapter", f"tcp -h 127.0.0.1 -p 50000")
        print("TODO APP \n Server listening on port 50000...")
        servant = ToDo()
        adapter.add(servant, Ice.stringToIdentity("LibraryService"))
        adapter.activate()
        self.communicator().waitForShutdown()
        return 0

if __name__ == "__main__":
    app = Server()
    sys.exit(app.main(sys.argv))