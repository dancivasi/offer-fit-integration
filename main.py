from typing import List
from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
import json
from typing import Optional
from pydantic import BaseModel
import datetime
app = FastAPI()


class EmailEvent(BaseModel):
    customer_id: int
    event_type: str
    timestamp: str


# Option 1, make it a function which is not called at load time

def get_all_events():
    with open('events.json', 'r') as file:
        all_events = json.loads(file.read())
        return all_events


# Option 2, we leave the code as is BUT, you need to know that when main.py is imported
# all_events will be computed and assigned so the main file will actually have main["all_events"] = ...
# This in the test we need to reload the import so that the mocking can take place
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


@app.get('/get_events/{customer_id}')
def get_events_for_customer_id(customer_id: int,
                               start_time: Optional[str] = Query(None,
                                                                 description="Start timestamp for filtering"),
                               end_time: Optional[str] = Query(None,
                                                               description="End timestamp for filtering"),
                               all_events: List[dict] = Depends(get_all_events)
                               ):
    if start_time:
        start_time = datetime.datetime.fromisoformat(start_time)
    if end_time:
        end_time = datetime.datetime.fromisoformat(end_time)
    filtered_events = []
    for event in all_events:
        timestamp = datetime.datetime.fromisoformat(event['timestamp'])
        if event['customer_id'] == customer_id and (start_time is None or timestamp >= start_time) and (end_time is None or timestamp <= end_time):
            filtered_events.append(event)
    if not filtered_events:
        return {'message': 'No email events found for the provided customer_id'}

    return filtered_events


if __name__ == "__main__":
    print(get_all_events())
