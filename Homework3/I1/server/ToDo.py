import Demo

class ToDo(Demo.TodoService):
    def __init__(self):
        self.tasks = []

    def getAllList(self):
        print(f"Your all saved tasks:\n")
        for task in self.tasks:
            print(f"{task.id}. \t {task.description} \t\t\t {task.status}")

        return self.tasks

    def getNotDoneTasks(self):
        print(f"Your actual tasks:\n")
        for task in self.tasks:
            if task.status != False:
                print(f"{task.id}. \t {task.description} \t\t\t {task.status}")

        return [task for task in self.tasks if task.status != False]

    def addTask(self, description):
        self.tasks.append(Demo.Task(id=len(self.tasks), description=description, isDone=False))
        print(f"Task added:\n {description}.")

    def changeTaskState(self, id):
        for task in self.tasks:
            if task.id == id:
                task.status = True
                print(f"Task {id} already finished!")

        print(f"Couldn't find task with id {id}.")