import sys
import os

sys.path.append(os.path.abspath("./generated"))

import Demo

class ToDo(Demo.TodoService):
    def __init__(self):
        self.tasks = []

    def getAllList(self, current=None):
        print(f"Your all saved tasks:\n")
        for task in self.tasks:
            print(f"{task.id}. \t {task.description} \t\t\t {task.isDone}")

        return self.tasks

    def getNotDoneTasks(self, current=None):
        print(f"Your actual tasks:\n")
        for task in self.tasks:
            if task.isDone != True:
                print(f"{task.id}. \t {task.description} \t\t\t {task.isDone}")

        return [task for task in self.tasks if task.isDone != False]

    def addTask(self, description, current=None):
        self.tasks.append(Demo.Task(id=len(self.tasks), description=description, isDone=False))
        print(f"Task added:\n {description}.")

    def changeTaskState(self, id, current=None):
        for task in self.tasks:
            if task.id == id:
                task.isDone = True
                print(f"Task {id} already finished!")
                return True

        print(f"Couldn't find task with id {id}.")
        return False