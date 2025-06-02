import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

public class Supplier {
    private String supplierName;
    private ArrayList<String> supplierProducts;

    private Channel orderChannel;
    private Connection connection;

    public Supplier(String supplierName) {
        this.supplierName = supplierName;
        this.supplierProducts = new ArrayList<>();
    }

    public void addProduct(String productName) {
        supplierProducts.add(productName);
    }

    public void getInfoAboutProducts() {
        System.out.println("\nSupplier name: " + this.supplierName + "\n" + "Supplier products: \n");
        for (String supplierProduct : this.supplierProducts) {
            System.out.println("- " + supplierProduct);
        }
    }

    public void listen() throws IOException {

        System.out.println("Waiting for orders...");

        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String product = new String(delivery.getBody(), "UTF-8");

            if (supplierProducts.contains(product)) {
                System.out.println("Received and accepted order for: " + product);
                for (int i = 1; i <= 5; i++) {
                    System.out.println(i + "...");
                }
            }
            else {
                System.out.println("Received but IGNORED order for: " + product);
            }

            orderChannel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
        };

        orderChannel.basicConsume("orders", false, deliverCallback, consumerTag -> {});
    }

    public void connect() {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");

            this.connection = factory.newConnection();
            this.orderChannel = connection.createChannel();

            this.orderChannel.queueDeclare("orders", false, false, false, null);
        }
        catch (Exception e) {
            e.printStackTrace();
            disconnect();
        }
    }

    public void disconnect() {
        try {
            if (this.orderChannel != null) {
                orderChannel.close();
            }
            if (connection != null) {
                connection.close();
            }
            System.out.println("Disconnected from RabbitMQ");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        try {
            System.out.print("Enter supplier name: ");
            String input = sc.nextLine();
            System.out.println();

            Supplier supplier = new Supplier(input);

            System.out.print("Enter products names: ");
            while (true) {
                String product = sc.nextLine();

                if (product.isEmpty()) {
                    continue;
                }

                else if (product.equals("NEXT")) {
                    break;
                }

                else {
                    supplier.addProduct(product);
                }
            }

            supplier.getInfoAboutProducts();
            supplier.connect();
            supplier.listen();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
