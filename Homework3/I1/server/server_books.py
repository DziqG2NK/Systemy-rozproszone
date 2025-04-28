"""
slice2py --output-dir generated slice/todo.ice
python server_books.py
"""

import sys
import Ice
import os
import logging

sys.path.append(os.path.abspath("./generated"))
import Demo

address = "127.0.0.1:50000"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BooksI(Demo.LibraryService):
    def __init__(self):
        # It's like a little "database" or something :P
        self.books = [
            Demo.Book(title="1984", author="George Orwell", year=1949),
            Demo.Book(title="Brave New World", author="Aldous Huxley", year=1932),
            Demo.Book(title="Fahrenheit 451", author="Ray Bradbury", year=1953),
            Demo.Book(title="Animal Farm", author="George Orwell", year=1945)
        ]
        logger.info("BooksI object created and sample books initialized.")

    def getBook(self, title, current=None):
        logger.info(f"Received request for book with title: {title}")
        for book in self.books:
            if book.title == title:
                logger.info(f"Book found: {book.title} by {book.author}")
                return book
        logger.warning(f"Book with title '{title}' not found.")
        return Demo.Book(title="Unknown", author="Unknown", year=0)

    def listBooks(self, current=None):
        logger.info("Received request to list all books.")
        for book in self.books:
            logger.info(f"Book: {book.title} by {book.author} ({book.year})")
        return self.books

    def countBooksByAuthor(self, author, current=None):
        logger.info(f"Received request to count books by author: {author}")
        count = sum(1 for book in self.books if book.author == author)
        logger.info(f"Found {count} books by {author}.")
        return count


class Server(Ice.Application):
    def run(self, args):
        adapter = self.communicator().createObjectAdapterWithEndpoints("LibraryAdapter", f"tcp -h 127.0.0.1 -p 50000")
        servant = BooksI()
        adapter.add(servant, Ice.stringToIdentity("LibraryService"))
        adapter.activate()
        logger.info("ICE Server for LibraryService has just started!")
        self.communicator().waitForShutdown()
        return 0


if __name__ == "__main__":
    app = Server()
    sys.exit(app.main(sys.argv))
