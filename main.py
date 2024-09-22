from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import re
import database # this is another file with name database.py
# import backend_page
# import backend_page.db_helper as helper #this is another module with some function
import db_helper as helper
app = FastAPI()

@app.get("/")
def read_root():
    
    return {"Hello": "World"}

# make a dictionary for a session
inprogress_order= dict()

def TrackOrder(parameters: dict, session_id: str):
    order_id = int(parameters['number'])
    order_status = database.get_order_status(order_id)

    if order_status:
        fullfillment_text = f'The order status for order id {order_id} = {order_status}'
    else:
        fullfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content= {
        'fulfillmentText': fullfillment_text
    })


def addOrder(parameters: dict, session_id: str):
    food_item = parameters['food-item']
    quantity = parameters['number']

    if(len(food_item) != len(quantity)):
        fullfillment_text = f"Sorry! i didn't understand. Can you please specify the food-item and quantity clearly"
    else:
        new_food_dict = dict(zip(food_item, quantity))
        if session_id in inprogress_order:
            curr_food_dict = inprogress_order[session_id]
            curr_food_dict.update(new_food_dict)
            inprogress_order[session_id] = curr_food_dict
        else:
            inprogress_order[session_id] = new_food_dict
        
        order_str = helper.get_str_from_food_dict(inprogress_order[session_id])
        fullfillment_text = f'so far you have  {order_str}. Do you need something else ? '

    return JSONResponse(content= {
        'fulfillmentText': fullfillment_text
    })

def completeOrder(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        fullfillment_text = f"sorry we didn't find your order. can you place it again?"
    else:
        order = inprogress_order[session_id]
        order_id = save_to_database(order)

        if order_id == -1:
            fullfillment_text = f"sorry! i couldn't process your order. pls place a new order"
        else: 
            order_total = database.get_total_order_price(order_id)
            fullfillment_text = f"awesome! we have placed your order"\
                                f"Here is your order id {order_id}. " \
                                f"your order total is {order_total} which you can pay at the time of delivery"

        del inprogress_order[session_id]  #remove the session after completing the order
    return JSONResponse(content= {
        'fulfillmentText': fullfillment_text
    })

def save_to_database(order: dict):
    # order = {'pizza': 1, 'lassi': 4}
    for food_item, quantity in order.items():
        next_order_id = database.get_next_order_id()
        rcode = database.insert_order_in_db(
            food_item, 
            quantity, 
            next_order_id
        )

        if rcode == -1:
            return -1
        
    database.insert_order_tracking(next_order_id, 'in progress')
    return next_order_id

#step to remove the order
#step1: locate the session id record
#step2: get the value from the dict : {'vada pav': 2, 'samosa' :1}
#step3: remove the food item. request: ['vada pav', 'samosa']

def removeOrder(parameters: dict, session_id: str):
    if session_id not in inprogress_order:
        return JSONResponse(content= {
        'fulfillmentText': f"I am having trouble to find your order. can you place a new order"
    })

    current_order = inprogress_order[session_id]
    food_items = parameters['food-item']

    removed_items = []
    no_such_item = []
    for item in food_items:
        if item not in current_order:  #the item is not present in the database
            no_such_item.append(item)
            
        else:
            #delete item from current order
            removed_items.append(item)
            del current_order[item]
        
    if len(removed_items) > 0:
        fullfillment_text = f"Removed {','. join(removed_items)} from your order!"
    
    if len(no_such_item) > 0:
        fullfillment_text = f"your current order doesn't have {','.join(no_such_item)}"

    if len(current_order.keys()) == 0:
        fullfillment_text += "your order is empty!"
    else:
        order_remain = helper.get_str_from_food_dict(current_order)
        fullfillment_text += f"Here is what is left in your order: {order_remain}"


    return JSONResponse(content= {
        'fulfillmentText': fullfillment_text
    })






@app.post('/')
async def handle_request(request: Request):
    #retrieve the json data from the request
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = helper.session_id_extracter(output_contexts[0]['name'])
    
    #making a dictionary for handling the intent
    intent_handler = {
        'order.add' : addOrder,
        'order.complete': completeOrder,
        'order.remove': removeOrder,
        'track_order_ongoing_tracking': TrackOrder
    }
    # if intent == 'track_order_ongoing_tracking':
    #     return TrackOrder(parameters)

    return intent_handler[intent](parameters, session_id)
