from fastapi import FastAPI

app=FastAPI( )

@app.get("/")
async def root() :
    return {"message" : "Welcome to Pole System!"}

class Poll:
    def __init__(self, pollId: int, question: str):
        self.pollId = pollId
        self.question = question
        self.votes = {}

    def add_option(self, option: str):
        if option not in self.votes:
            self.votes[option] = 0

    def add_vote(self, option: str):
        if option in self.votes:
            self.votes[option] += 1
            return True
        else:
            return False

    def delete_vote(self, option: str):
        if option in self.votes:
            if self.votes[option] > 0:
                self.votes[option] -= 1
                return True
        else:
            return False
