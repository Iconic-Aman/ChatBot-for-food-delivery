import re
import mysql.connector
from backend_page.database import cnx

text = "projects/aman-chatbot-ghka/agent/sessions/contexts/ongoing-order"
def session_id_extracter(text):

# Define the regular expression pattern using (.*?)
    
    pattern = r"/sessions/(.*?)/contexts/"
    match = re.search(pattern, text)
    if match:
        session_number = match.group(1)
        # print("Session Number:", session_number)
        return session_number
    # else:
    #     print("No match found.")

# session_id_extracter(text)

def get_str_from_food_dict(food_dict: dict):
    formatted_items = []
    for item, quantity in food_dict.items():
        quantity = int(quantity)
        formatted_items.append(f"{quantity} {item}" + ("s" if quantity > 1 else ""))
    result_string = ', '.join(formatted_items[:-1]) + (" and " if len(formatted_items) > 1 else "") + formatted_items[-1]
    return result_string


# def handle_unknown_intent(parameters: dict, session_id: str):
#     fullfillment_text = f"Unknown intent. Please handle this case."
#     return JSONResponse(content={
#         'fulfillmentText': fullfillment_text
#     })




menu_items = {'lassi': 1, 'samosa': 2, 'bananas': 10.0}
    
a = get_str_from_food_dict(menu_items)
print(a)
    
# menu_items = {'samosa': 2, 'lassi': 1}


# Create a list to store formatted strings for each item

# Iterate over items and append the formatted string to the list


# Join the list using commas and add "and" before the last item

# print(result_string)
