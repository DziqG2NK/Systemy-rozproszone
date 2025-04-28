/*
slice2java --output-dir generated slice/todo.ice
*/

package sr.ice.client;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;

import java.lang.Exception;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ClientBooksDynamic {
	private static final String IP = "127.0.0.1";
	private static final int PORT = 10001;

	private static int countBooksByAuthorsInvocationInClient(ObjectPrx proxy, String author) {
		OutputStream out = new OutputStream(proxy.ice_getCommunicator());
		out.startEncapsulation();
		out.writeString(author);
		out.endEncapsulation();

		byte[] inParams = out.finished();
		Object.Ice_invokeResult resultAns = proxy.ice_invoke("countBooksByAuthor", OperationMode.Normal, inParams);

		if (!resultAns.returnValue) {
			throw new RuntimeException("Invocation failed!");
		}

		byte[] resultBytes = resultAns.outParams;

		InputStream in = new InputStream(proxy.ice_getCommunicator(), resultBytes);
		in.startEncapsulation();
		int bookCount = in.readInt();
		in.endEncapsulation();

		return bookCount;
	}
	private static Book getBookInvocationInClient(ObjectPrx proxy, String title) {
		OutputStream out = new OutputStream(proxy.ice_getCommunicator());
		out.startEncapsulation();
		out.writeString(title);
		out.endEncapsulation();

		byte[] inParams = out.finished();
		Object.Ice_invokeResult resultAns = proxy.ice_invoke("getBook", OperationMode.Normal, inParams);

		if (!resultAns.returnValue) {
			throw new RuntimeException("Invocation failed!");
		}
		byte[] resultBytes = resultAns.outParams;

		InputStream in = new InputStream(proxy.ice_getCommunicator(), resultBytes);
		in.startEncapsulation();
		String returnedTitle = in.readString();
		String returnedAuthor = in.readString();
		int returnedYear = in.readInt();
		in.endEncapsulation();

		return new Book(returnedTitle, returnedAuthor, returnedYear);
	}
	private static List<Book> listBooksInvocationInClient(ObjectPrx proxy) {
		OutputStream out = new OutputStream(proxy.ice_getCommunicator());
		out.startEncapsulation();
		out.endEncapsulation();

		byte[] inParams = out.finished();
		Object.Ice_invokeResult resultAns = proxy.ice_invoke("listBooks", OperationMode.Normal, inParams);

		if (!resultAns.returnValue) {
			throw new RuntimeException("Invocation failed!");
		}

		byte[] resultBytes = resultAns.outParams;

		InputStream in = new InputStream(proxy.ice_getCommunicator(), resultBytes);
		in.startEncapsulation();
		int size = in.readSize();
		List<Book> books = new ArrayList<>();
		for (int i = 0; i < size; i++) {
			String title = in.readString();
			String author = in.readString();
			int year = in.readInt();
			books.add(new Book(title, author, year));
		}
		in.endEncapsulation();

		return books;
	}

	public static void main(String[] args) {
		try (Communicator communicator = Util.initialize(args)) {

			ObjectPrx base = communicator.stringToProxy("LibraryService:tcp -h %s -p %d".formatted(IP, PORT));

			Scanner scanner = new Scanner(System.in);
			System.out.println("Select method for testing");
			System.out.println("b -- getBook | l -- listBooks | c -- countBooksByAuthor");
			System.out.print("Your choice (e.g. b):");
			char choice = scanner.nextLine().charAt(0);

			switch (choice) {
				case 'b':
					System.out.print("Book title (e.g. Animal Farm):");
					String bookTitle = scanner.nextLine();

					// Dynamic Invocation #1 -- Book getBook(string title);
					Book bookResult = getBookInvocationInClient(base, bookTitle);
					System.out.println("getBook(\"" + bookTitle + "\") --> " + bookResult);
					break;
				case 'l':
					// Dynamic Invocation #2 -- BookSeq listBooks();
					List<Book> books = listBooksInvocationInClient(base);
					System.out.println("listBooks() --> ");
					for (Book book : books) {
						System.out.println("\t" + book);
					}
					break;
				case 'c':
					System.out.print("Author (e.g. George Orwell):");
					String authorName = scanner.nextLine();

					// Dynamic Invocation #3 -- int countBooksByAuthor(string author);
					int bookCountByAuthor = countBooksByAuthorsInvocationInClient(base, authorName);
					System.out.println("countBooksByAuthor(\"" + authorName + "\") --> " + bookCountByAuthor);
					break;
				default:
					System.out.println("Invalid command.");
					break;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}



}