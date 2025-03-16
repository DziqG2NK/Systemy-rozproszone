from fastapi import FastAPI

app=FastAPI( )

class Vote:
    def __init__(self, id: int, name: str):
        self.id = id

class Poll:
    def __init__(self, id: int):
        self.id = id
        self.votes = {}

    def add_vote(self, vote: Vote):
        if vote.id not in self.votes.keys():
            self.votes[vote.id] = 1
        else:
            self.votes[vote.id] += 1

biggest_id = 1
polls_array = []

@app.get("/")
async def root() :
    return {"message" : "Take your poll!"}

@app.get("/poll")
async def get_all_polls():
    return polls_array

@app.put("/poll")
async def create_new_poll():
    global biggest_id
    polls_array.append(Poll(biggest_id))
    biggest_id += 1
    return {"message" : f"New poll id is {biggest_id - 1}"}

@app.delete("/poll/{poll_id}/votes/{vote_id}")
async def remove_one_vote(poll_id: int, vote_id: int):
    for i, i_poll in enumerate(polls_array):
        if i_poll.id == poll_id and vote_id in i_poll.votes.keys() and i_poll.votes[vote_id] > 0:
            polls_array[i].votes[vote_id] -= 1
            return {"message" : f"Removed vote for option {vote_id} in poll {poll_id}"}

    return {"message": f"Removing not completed"}

@app.post("/poll/{poll_id}/votes/{vote_id}")
async def add_vote_to_poll(poll_id: int, vote_id: int):
    for i, i_poll in enumerate(polls_array):
        if i_poll.id == poll_id:
            if vote_id not in i_poll.votes.keys():
                polls_array[i].votes[vote_id] = 1
                return {"message": f"Created option {vote_id} in poll {poll_id}"}

            polls_array[i].votes[vote_id] += 1
            return {"message" : f"Added vote for option {vote_id} in poll {poll_id}"}

    return {"message": f"Voting not succeeded"}
