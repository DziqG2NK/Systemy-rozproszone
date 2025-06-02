import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.util.Scanner;

public class Team {
    private String teamName;
    private Channel ordersChannel;
//    private Channel adminChannel;
    private Connection connection;

    public Team(String teamName) {
        this.teamName = teamName;
    }

    public void connect() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            this.connection = connection;

            this.ordersChannel = connection.createChannel();
//            this.adminChannel = connection.createChannel();

            ordersChannel.queueDeclare("orders", false, false, false, null);
//            adminChannel.queueDeclare("admin-info", false, false, false, null);
        }
        catch (Exception e) {
            e.printStackTrace();
            disconnect();
        }
    }

    public void disconnect() {
        try {
            if (ordersChannel != null) {
                this.ordersChannel.close();
            }
//            if (ordersChannel != null) {
//                this.adminChannel.close();
//            }
            if (ordersChannel != null) {
                this.connection.close();
            }

            System.out.println("Succesfully disconnected");
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void orderProduct() {
        try {
            Scanner sc = new Scanner(System.in);
            System.out.println("Order product: ");

            while (true) {
                String product = sc.nextLine();

                if (product.isEmpty()) {
                    continue;
                }

                else if (product == "QUIT") {
                    break;
                }

                else {
                    try {
                        this.ordersChannel.basicPublish("", "orders", null, product.getBytes());
                        System.out.println("Sent: " + product);
                    }
                    catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        finally {
            disconnect();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        try {
            System.out.print("Team name: ");
            String input = sc.nextLine();
            System.out.println();

            Team team = new Team(input);

            team.connect();
            team.orderProduct();
        }
        catch (Exception e) {
            e.printStackTrace();
            sc.close();
        }
    }
}
