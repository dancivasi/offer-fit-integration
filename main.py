from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
import json

app = FastAPI()

with open('events.json', 'r') as file:
    events = file.read()

all_events = json.loads(events)


class EmailEvent(BaseModel):
    customer_id: int
    event_type: str
    timestamp: str


@app.get('/get_email_events/{customer_id}')
def get_email_events_for_customer_id(customer_id: int,
                                     start_time: Optional[str] = Query(None,
                                                                       description="Start timestamp for filtering"),
                                     end_time: Optional[str] = Query(None,
                                                                     description="End timestamp for filtering")
                                     ):
    filtered_events = [
        EmailEvent(**event) for event in all_events
        if event['customer_id'] == customer_id
           and (start_time is None or event['timestamp'] >= start_time)
           and (end_time is None or event['timestamp'] <= end_time)
    ]

    if not filtered_events:
        return {'message': 'No email events found for the provided customer_id'}
    else:
        return filtered_events
