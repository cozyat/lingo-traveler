import requests
import sys

while True:
    try:
        language = input("Welcome to LingoTraveler! Tell us a language you speak, and we'll find facts over it for you! | Language: ")
        break
    except TypeError as err:
        print("Invalid input! Please try again. Error: ", str(err).title())
        sys.exit()

print("\n")

url = "https://restcountries.com/v3.1"
path = "lang"

response = requests.get(url + "/" + path + "/" + language.lower())

if response.status_code == 200:
    states = response.json()
else:
    print("Error " + str(response.status_code) + ": Please try again.")

countries = []
for state in states:
    try:
        if isinstance(state["name"], dict):
            state_params = state["name"].copy()
            for common_name, state_name in list(state_params.items()):
                if common_name in ["common", "official"]:
                    countries.append(state["name"][common_name].lower())
        else:
            print("Skipping state as 'name' is not a dictionary.")
    except TypeError as err:
        print("Process did not work! Error:", str(err).title())
        sys.exit()

for iterator, country in enumerate(countries, 1):
    print(str(iterator) + ". " + country.title())
print("↑↑↑ Right above are some countries where", language.title(), "is spoken ↑↑↑")
print("\n")

country = input("Now tell us the country you would like to visit to see if you can speak your language there. | Country: ").lower()
print("\n")

selected_state = None
for state in states:
    if country == state["name"]["common"].lower() or country == state["name"]["official"].lower():
        selected_state = state
        break

if selected_state:
    while True:
        print("What would you like to know about " + country.title() + "? " + selected_state["flag"] + " | ** Enter a number only **")
        print("0. EXIT PROGRAM")
        print("1. Population of " + country.title())
        print("2. Capital of " + country.title())
        print("3. " + country.title() + "'s Currency")
        print("4. Flag Information & Attributes")
        print("5. Google Maps Location")
        print("6. OpenStreet Maps Location")
        print("7. FIFA Soccer Status")
        print("8. Timezones")
        print("9. Continents")
        print("")
        try:
            info = int(input("Answer: "))
            if info == 1:
                if "population" in selected_state:
                    print("Population:", selected_state["population"])
                else:
                    print("Population: Data not available")
            elif info == 2:
                if "capital" in selected_state:
                    print("Capital:", selected_state["capital"][0])
                else:
                    print("Capital: Data not available")
            elif info == 3:
                if "currencies" in selected_state:
                    currencies = selected_state["currencies"]
                    for json, details in list(currencies.items()):
                        if "name" in details:
                            currency_name = details["name"]
                        else:
                            currency_name = "Unknown currency"
                        if "symbol" in details:
                            currency_symbol = details["symbol"]
                        else:
                            currency_symbol = ""
                        print("Currency:", currency_name, currency_symbol)
                else:
                    print("Currency information is not available.")
            elif info == 4:
                if "flags" in selected_state:
                    print("Flag Information & Attributes:", selected_state["flags"]["alt"])
                else:
                    print("Flag Information & Attributes: Data not available")
            elif info == 5:
                if "maps" in selected_state:
                    print("Google Maps Location:", selected_state["maps"]["googleMaps"])
                else:
                    print("Google Maps Location: Data not available")
            elif info == 6:
                if "maps" in selected_state:
                    print("OpenStreet Maps Location:", selected_state["maps"]["openStreetMaps"])
                else:
                    print("OpenStreet Maps Location: Data not available")
            elif info == 7:
                if "fifa" in selected_state:
                    print("FIFA Status:", selected_state["fifa"])
                else:
                    print("FIFA Status: Data not available")
            elif info == 8:
                if "timezones" in selected_state:
                    print("Timezones:")
                    for timezone in selected_state["timezones"]:
                        print(timezone)
                else:
                    print("Timezones: Data not available")
            elif info == 9:
                if "continents" in selected_state:
                    print("Continents:")
                    for continent in selected_state["continents"]:
                        print(continent)
                else:
                    print("Continents: Data not available")
            elif info == 0:
                print("Thank you for using LingoTraveler!")
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        print("\n")
else:
    print("We're sorry, but " + language.title() + " is not commonly spoken in " + country.title() + ", or you gave something invalid.")