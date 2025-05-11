package sr.ice.client;

public class Task {
    private int id;
    private String description;
    private boolean isDone;

    public Task(final int id, final String description, final boolean isDone) {
        this.id = id;
        this.description = description;
        this.isDone = isDone;
    }

    @Override
    public String toString() {
        System.out.print(id + ".  " + description + "\t\t\t" + isDone + "\n");
        return "Task { " +
                "id=" + id +
                ", description='" + description + '\'' +
                ", isDone=" + isDone +
                " }";
    }
}
