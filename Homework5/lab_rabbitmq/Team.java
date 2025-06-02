import java.util.Scanner;

public class Team {
    private String teamName;

    public Team(String teamName) {
        this.teamName = teamName;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        try {
            System.out.print("Team name: ");
            String input = sc.nextLine();
            System.out.println();

            Team team = new Team(input);

            System.out.print("Order product: ");
            while (true) {
                String product = sc.nextLine();

                if (product.isEmpty()) {
                    continue;
                }

                else if (product.equals("NEXT")) {
                    break;
                }

                else {
                    continue;
//                    TODO
                }
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
        }
    }
}
