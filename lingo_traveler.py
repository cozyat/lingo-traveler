import requests
import sys

def get_language():
    while True:
        try:
            language = input("Welcome to LingoTraveler! Tell us a language you speak, and we'll find facts over it for you! | Language: ")
            return language
        except TypeError as err:
            print("Invalid input! Please try again. Error: ", str(err).title())
            sys.exit()

def fetch_countries(language):
    url = "https://restcountries.com/v3.1"
    path = "lang"
    response = requests.get(url + "/" + path + "/" + language.lower())
    if response.status_code == 200:
        return response.json()
    else:
        print("Error " + str(response.status_code) + ": Please try again.")
        sys.exit()

def extract_country_names(states):
    countries = []
    for state in states:
        try:
            if isinstance(state["name"], dict):
                state_params = state["name"].copy()
                for common_name in state_params:
                    if common_name in ["common", "official"]:
                        countries.append(state["name"][common_name].lower())
            else:
                print("Skipping state as 'name' is not a dictionary.")
        except TypeError as err:
            print("Process did not work! Error:", str(err).title())
            sys.exit()
    return countries

def display_countries(countries, language):
    for iterator, country in enumerate(countries, 1):
        print(str(iterator) + ". " + country.title())
    print("↑↑↑ Right above are some countries where", language.title(), "is spoken ↑↑↑\n")

def get_user_country():
    return input("Now tell us the country you would like to visit to see if you can speak your language there. Input the name only! | Country: ").lower()

def find_selected_state(states, country):
    for state in states:
        if country == state["name"]["common"].lower() or country == state["name"]["official"].lower():
            return state
    return None

def display_country_options(selected_state, country):
    while True:
        print("What would you like to know about " + country.title() + "? " + selected_state["flag"] + " | Enter a number only")
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
                print("Population:", f"{selected_state.get('population', 'Data not available'):,}")
            elif info == 2:
                print("Capital:", selected_state.get("capital", ["Data not available"])[0])
            elif info == 3:
                if "currencies" in selected_state:
                    for json, details in selected_state["currencies"].items():
                        currency_name = details.get("name", "Unknown currency")
                        currency_symbol = details.get("symbol", "")
                        print("Currency:", currency_name, currency_symbol)
                else:
                    print("Currency information is not available.")
            elif info == 4:
                print("Flag Information & Attributes:", selected_state["flags"].get("alt", "Data not available"))
            elif info == 5:
                print("Google Maps Location:", selected_state["maps"].get("googleMaps", "Data not available"))
            elif info == 6:
                print("OpenStreet Maps Location:", selected_state["maps"].get("openStreetMaps", "Data not available"))
            elif info == 7:
                print("FIFA Status:", selected_state.get("fifa", "Data not available"))
            elif info == 8:
                print("Timezones:")
                for timezone in selected_state.get("timezones", ["Data not available"]):
                    print(timezone)
            elif info == 9:
                print("Continents:")
                for continent in selected_state.get("continents", ["Data not available"]):
                    print(continent)
            elif info == 0:
                print("Thank you for using LingoTraveler!")
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
        print("\n")

def main():
    language = get_language()
    print("\n")
    states = fetch_countries(language)
    countries = extract_country_names(states)
    display_countries(countries, language)
    country = get_user_country()
    print("\n")
    selected_state = find_selected_state(states, country)
    if selected_state:
        display_country_options(selected_state, country)
    else:
        print("We're sorry, but " + language.title() + " is not commonly spoken in " + country.title() + ", or you gave something invalid.")

main()
