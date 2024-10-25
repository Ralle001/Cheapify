import requests
import json


class Search_Everywhere_Result:
    def __init__(self, country_name, country_id, cheapest_price, cheapest_is_direct, has_direct, direct_price):
        self.country_name = country_name
        self.country_id = country_id
        self.cheapest_price = cheapest_price
        self.cheapest_is_direct = cheapest_is_direct
        self.has_direct = has_direct
        self.direct_price = direct_price

    def get_country_id(self):
        return self.country_id
    
    def get_cheapest_price(self):
        return self.cheapest_price
    
class Itinerary:
    def __init__(self, id, price, legs):
        self.id = id
        self.price = price
        self.legs = legs
    
    def get_id(self):
        return self.id

class Leg:
    def __init__(self, id, origin_id, destination_id, duration, departure_time, arrival_time):
        self.id = id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.duration = duration
        self.departure_time = departure_time
        self.arrival_time = arrival_time

# Convert the json to a list
def json_to_list(json):
    results = json['data']['everywhereDestination']['results']
    locations_content = [result['content'] for result in results]

    results = []
    for item in locations_content:
        ref_location = item['location']
        if 'flightQuotes' not in item:
            continue
        ref_flight_quotes = item['flightQuotes']
        ref_flight_routes = item['flightRoutes']

        temp = Search_Everywhere_Result(
            ref_location['name'],
            ref_location['skyCode'],
            ref_flight_quotes['cheapest']['rawPrice'],
            ref_flight_quotes['cheapest']['direct'],
            ref_flight_routes['directFlightsAvailable'],
            ref_flight_quotes.get('direct', {}).get('rawPrice', 'na')
        )
        results.append(temp)

def specific_arrival_airport(json):
    results = json['data']['itineraries']

    result = []

    for item in results:
        temp = Itinerary(
            item['id'],
            item['price']['raw'],
            [Leg
            (
                item['legs'][0]['id'],
                item['legs'][0]['origin']['id'],
                item['legs'][0]['destination']['id'],
                item['legs'][0]['durationInMinutes'],
                item['legs'][0]['departure'],
                item['legs'][0]['arrival']
            ),
            Leg
            (
                item['legs'][1]['id'],
                item['legs'][1]['origin']['id'],
                item['legs'][1]['destination']['id'],
                item['legs'][1]['durationInMinutes'],
                item['legs'][1]['departure'],
                item['legs'][1]['arrival']
            )]
        )

    result.append(temp)
    return result

# Handle the API request
def search_everywhere(query):

    search_everywhere_url = "https://sky-scanner3.p.rapidapi.com/flights/search-everywhere"

    headers = {
	    "x-rapidapi-key": "987653c7efmshaff5337a58ed998p11f5c6jsn5b5d6e02cead",
	    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(search_everywhere_url, headers=headers, params=query)

    return json_to_list(response.json())

def solo_travel():
    departure_airport_code = input("Enter the departure airport code: ")
    arrival_airport_code = input("(Opcional) Enter the arrival airport code: ")
    currency = input("(Opcional) Enter the type of currency you would like to see: ")
    departure_date = input("Departure date (for example: 2024-01-20): ")
    return_date = input("Return date (for example: 2024-01-20): ")

    solo_travel_url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"

    querystring = {
        "fromEntityId":departure_airport_code,
        "toEntityId": arrival_airport_code if arrival_airport_code else 'everywhere',
        "departDate":str(departure_date),
        "returnDate":str(return_date),
        "currency":currency}

    headers = {
	    "x-rapidapi-key": "987653c7efmshaff5337a58ed998p11f5c6jsn5b5d6e02cead",
	    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(solo_travel_url, headers=headers, params=querystring)
    if arrival_airport_code:
        return specific_arrival_airport(response.json())
    else:
        return json_to_list(response.json())

# Main code
final_result = []

print("Select mode: ")
print("1: Find the cheapest travel option from one departure airport to anywhere in the world at the given date")
print("2: Find the cheapest (combined) travel option from two departure airport to anywhere in the world at the given date")

choice = input("Your choice: ")
match choice:
    case "1":
        final_result = solo_travel()
    case 2:
        pass

for item in final_result:
    print(item.get_id())

results_list = []

#querystring = {"fromEntityId":departure_airport_code,"type":flight_type}
querystring = {"fromEntityId":"BUD", "type":"oneway"}

results_list.append(search_everywhere(querystring))



