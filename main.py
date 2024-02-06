from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json


app = FastAPI()

with open('events.json', 'r') as file:
    all_events = json.loads(file.read())


@app.get('/events/{customer_id}')
def events_for_customer_id(customer_id: int):
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
