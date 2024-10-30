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
states = response.json()

countries = []
for state in states:
    try:
        if isinstance(state["name"], dict):
            state_params = state["name"].copy()
            for common_name, state_name in list(state_params.items()):
                if common_name in ["common", "official"]:
                    countries.append(state["name"].get(common_name).lower())
        else:
            print("Skipping state as 'name' is not a dictionary.")
    except TypeError as err:
        print("Process did not work! Error:", str(err).title())
        sys.exit()

country = input("Now tell us the country you would like to visit to see if you can speak your language there. | Country: ").lower()
print("\n")

selected_state = None
for state in states:
    if country == state["name"].get("common", "").lower() or country == state["name"].get("official", "").lower():
        selected_state = state
        break

if selected_state:
    while True:
        print("What would you like to know about " + country.title() + "? " + selected_state.get("flag", " ") + " | ** Enter a number only **")
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
                print("Population:", selected_state.get("population", "Data not available"))
            elif info == 2:
                print("Capital:", selected_state.get("capital", ["Data not available"])[0])
            elif info == 3:
                currencies = selected_state.get("currencies", {})
                if currencies:
                    for json, details in list(currencies.items()):
                        currency_name = details.get("name", "Unknown currency")
                        currency_symbol = details.get("symbol", "")
                        print("Currency:", currency_name, currency_symbol)
                else:
                    print("Currency information is not available.")
            elif info == 4:
                print("Flag Information & Attributes:", selected_state.get("flags", "Data not available"))
            elif info == 5:
                print("Google Maps Location:", selected_state.get("maps", {}).get("googleMaps", "Data not available"))
            elif info == 6:
                print("OpenStreet Maps Location:", selected_state.get("maps", {}).get("openStreetMaps", "Data not available"))
            elif info == 7:
                print("FIFA Status:", selected_state.get("fifa", "Data not available"))
            elif info == 8:
                print("Timezones:", selected_state.get("timezones", "Data not available"))
            elif info == 9:
                print("Continents:", selected_state.get("continents", "Data not available"))
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