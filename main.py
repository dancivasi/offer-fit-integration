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
