from fastapi import FastAPI
import json

app = FastAPI()

with open('events.json', 'r') as file:
    events = file.read()

all_events = json.loads(events)


@app.get('/get_event/{customer_id}')
def get_event(customer_id: int):
    customer_events = []
    for event in all_events:
        if event['customer_id'] == customer_id:
            customer_events.append(event)
    if customer_events == []:
        return {'message': 'No events for the event provided'}
    else:
        return customer_events
