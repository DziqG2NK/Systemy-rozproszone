package sr.ice.client;

import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;

import java.lang.Exception;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ToDoClient {
    private static final String IP = "127.0.0.1";
    private static final int PORT = 50000;

    public static class Task {
        public int id;
        public String description;
        public boolean isDone;

        public Task(int id, String description, boolean isDone) {
            this.id = id;
            this.description = description;
            this.isDone = isDone;
        }

        @Override
        public String toString() {
            return "Task { " +
                    "id=" + id +
                    ", description='" + description + '\'' +
                    ", isDone=" + isDone +
                    " }";
        }
    }

    private static List<Task> getAllListInvocation(ObjectPrx proxy) {
        try {
            OutputStream out = new OutputStream(proxy.ice_getCommunicator());
            out.startEncapsulation();
            out.endEncapsulation();

            byte[] inParams = out.finished();
            Object.Ice_invokeResult resultAns = proxy.ice_invoke("getAllList", OperationMode.Normal, inParams);

            if (!resultAns.returnValue) {
                throw new RuntimeException("Invocation failed!");
            }

            byte[] resultBytes = resultAns.outParams;
            InputStream in = new InputStream(proxy.ice_getCommunicator(), resultBytes);
            in.startEncapsulation();
            int size = in.readSize();
            List<Task> tasks = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                int id = in.readInt();
                String description = in.readString();
                boolean isDone = in.readBool();
                tasks.add(new Task(id, description, isDone));
            }
            in.endEncapsulation();

            return tasks;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static List<Task> getNotDoneTasksInvocation(ObjectPrx proxy) {
        try {
            OutputStream out = new OutputStream(proxy.ice_getCommunicator());
            out.startEncapsulation();
            out.endEncapsulation();

            byte[] inParams = out.finished();
            Object.Ice_invokeResult resultAns = proxy.ice_invoke("getNotDoneTasks", OperationMode.Normal, inParams);

            if (!resultAns.returnValue) {
                throw new RuntimeException("Invocation failed!");
            }

            byte[] resultBytes = resultAns.outParams;
            InputStream in = new InputStream(proxy.ice_getCommunicator(), resultBytes);
            in.startEncapsulation();
            int size = in.readSize();
            List<Task> tasks = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                int id = in.readInt();
                String description = in.readString();
                boolean isDone = in.readBool();
                tasks.add(new Task(id, description, isDone));
            }
            in.endEncapsulation();

            return tasks;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static void addTaskInvocation(ObjectPrx proxy, String description) {
        try {
            OutputStream out = new OutputStream(proxy.ice_getCommunicator());
            out.startEncapsulation();
            out.writeString(description);
            out.endEncapsulation();

            byte[] inParams = out.finished();
            Object.Ice_invokeResult resultAns = proxy.ice_invoke("addTask", OperationMode.Normal, inParams);

            if (!resultAns.returnValue) {
                throw new RuntimeException("Invocation failed!");
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static void changeTaskStateInvocation(ObjectPrx proxy, int id) {
        try {
            OutputStream out = new OutputStream(proxy.ice_getCommunicator());
            out.startEncapsulation();
            out.writeInt(id);
            out.endEncapsulation();

            byte[] inParams = out.finished();
            Object.Ice_invokeResult resultAns = proxy.ice_invoke("changeTaskState", OperationMode.Normal, inParams);

            if (!resultAns.returnValue) {
                throw new RuntimeException("Invocation failed!");
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        try (Communicator communicator = Util.initialize(args)) {

            ObjectPrx base = communicator.stringToProxy("LibraryService:tcp -h %s -p %d".formatted(IP, PORT));

            Scanner scanner = new Scanner(System.in);

            while (true) {
                System.out.println("\n===== TODO APP MENU =====");
                System.out.println("1 - Add new task");
                System.out.println("2 - List all tasks");
                System.out.println("3 - List not done tasks");
                System.out.println("4 - Change task state");
                System.out.println("0 - Exit");
                System.out.print("Choose option: ");

                String option = scanner.nextLine();

                switch (option) {
                    case "1":
                        System.out.print("Enter task description: ");
                        String description = scanner.nextLine();
                        addTaskInvocation(base, description);
                        System.out.println("Task added successfully.");
                        break;
                    case "2":
                        List<Task> allTasks = getAllListInvocation(base);
                        System.out.println("All tasks:");
                        for (Task task : allTasks) {
                            System.out.println(task);
                        }
                        break;
                    case "3":
                        List<Task> notDoneTasks = getNotDoneTasksInvocation(base);
                        System.out.println("Not done tasks:");
                        for (Task task : notDoneTasks) {
                            System.out.println(task);
                        }
                        break;
                    case "4":
                        System.out.print("Enter task ID to mark as done: ");
                        int id = Integer.parseInt(scanner.nextLine());
                        changeTaskStateInvocation(base, id);
                        System.out.println("Task state changed.");
                        break;
                    case "0":
                        System.out.println("Exiting...");
                        return;
                    default:
                        System.out.println("Invalid option. Try again.");
                        break;
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
