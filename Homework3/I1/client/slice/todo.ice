module Demo
{
    struct Task
    {
        int id;
        string description;
        bool isDone;
    };

    sequence<Task> Tasks;

    interface TodoService
    {
        Tasks getAllList();
        Tasks getNotDoneTasks();
        void addTask(string description);
        void changeTaskState(int id);
    };
};