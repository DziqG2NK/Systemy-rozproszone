from fastapi import FastAPI
from fastapi import Body, FastAPI, status
from fastapi.responses import JSONResponse

app=FastAPI( )

@app.get("/")
async def root() :
    return {"message" : "WELCOME TO MY POLL"}

class Vote:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Poll:
    def __init__(self, id: int):
        self.id = id
        self.votes = {}

    def add_vote(self, vote: Vote):
        if vote.id not in self.votes.keys():
            self.votes[vote.id] = 1
        else:
            self.votes[vote.id] += 1


next_id = 0
all_polls = []


@app.get("/poll")
async def get_poll():
    return all_polls


@app.put("/poll")
async def create_poll():
    global next_id
    all_polls.append(Poll(next_id))
    next_id += 1


@app.delete("/poll/{id}")
async def delete_poll(poll_id: int):
    for i in range(len(all_polls)):
        if all_polls[i].id == poll_id:
            all_polls[i].votes = {}
            all_polls.pop()


@app.put("/poll/{id_p}/votes/{id_v}")
async def add_vote_to_poll(poll_id: int, vote_id: int):
    for i in range(len(all_polls)):
        if all_polls[i].id == poll_id:
            if vote_id not in all_polls[i].votes.keys():
                all_polls[i].votes[vote_id] = 1
            else:
                all_polls[i].votes[vote_id] += 1


@app.get("/poll/{id_p}/votes/{id_v}")
async def get_vote_count(poll_id: int, vote_id: int):
    return all_polls[poll_id].votes[vote_id]


@app.delete("/poll/{id_p}/votes/{id_v}")
async def remove_one_vote(poll_id: int, vote_id: int):
    for i in range(len(all_polls)):
        if all_polls[i].id == poll_id and vote_id in all_polls[i].votes.keys() and all_polls[i].votes[vote_id] > 0:
            all_polls[i].votes[vote_id] -= 1
