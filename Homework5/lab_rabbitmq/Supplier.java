import java.util.ArrayList;
import java.util.Scanner;

public class Supplier {
    private String supplierName;
    private ArrayList<String> supplierProducts;

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
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
