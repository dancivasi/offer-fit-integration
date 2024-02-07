from typing import List

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import json


app = FastAPI()


# Option 1, make it a function which is not called at load time
def get_all_events():
    with open('events.json', 'r') as file:
        all_events = json.loads(file.read())
        return all_events


# Option 2, we leave the code as is BUT, you need to know that when main.py is imported
# all_events will be computed and assigned so the main file will actually have main["all_events"] = ...
# Thus in the test we need to reload the import so that the mocking can take place
# with open('events.json', 'r') as file:
#     all_events = json.loads(file.read())

@app.get('/events/{customer_id}')
def events_for_customer_id(customer_id: int, all_events: List[dict] = Depends(get_all_events)):
    customer_events = []
    for event in all_events:
        if event['customer_id'] == customer_id:
            customer_events.append(event)
    if not customer_events:
        return JSONResponse(
            status_code=204,
            content={"message": "No events for the event provided"}
        )
    else:
        return customer_events

