from fastapi import FastAPI, Response, status
import json


app = FastAPI()

with open('events.json', 'r') as file:
    all_events = json.loads(file.read())


@app.get('/events/{customer_id}', status_code=200)
def events_for_customer_id(customer_id: int, response: Response):
    customer_events = []
    for event in all_events:
        if event['customer_id'] == customer_id:
            customer_events.append(event)
    if customer_events == []:
        print("am ajuns aiciaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        response.status_code = status.HTTP_204_NO_CONTENT
        print("am ajuns aicibbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        return response.status_code
    else:
        return customer_events
