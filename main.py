from fastapi import FastAPI, Path
from pydantic import BaseModel


app = FastAPI()

events = {
    1: {"customer_id": 123,
        "event_type": "email_click",
        "timestamp": "2023-10-23T14:30:00",
        "email_id": 1234,
        "clicked_link": "https://example.com/some-link"
        },
    2: {"customer_id": 456,
        "event_type": "email_open",
        "timestamp": "2023-10-24T11:30:00",
        "email_id": 998
        },
    3: {"customer_id": 457,
        "event_type": "email_unsubscribe",
        "timestamp": "2023-10-24T11:30:25",
        "email_id": 998
        },
    4: {"customer_id": 124,
        "event_type": "purchase",
        "timestamp": "25-10-2023T15:33:00",
        "email_id": 1234,
        "product_id": 357,
        "amount": 49.99
        },
}


class Event(BaseModel):
    customer_id: int
    event_type: str
    timestamp: str
    email_id: str

@app.get("/")
def get():
    return {"muie": "partidu psd"}


@app.get("/get_event/{event_number}")
def get_event(event_number: int = Path(description="The number of the event you want to see", gt=0, lt=5)):
    return events[event_number]


@app.get("/get_customer_id")
def get_customer_id(customer_id):
    for customer in events:
        if events[customer]["customer_id"] == customer_id:
            return events[customer_id]
    return {"Data": "Not Found"}

@app.post("/create_event/{customer_id}")
def create_event(customer_id: int, event: Event):
    if customer_id in event:
        return {"Error": "Event Already Exists"}
    else:
        events[customer_id] = event
        return events[customer_id]


