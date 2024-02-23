import requests

def get_weather():
    api_key = "321c21a0e2a55554d0974bfc221939ad"  
    city = "Exeter"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        weather_conditions = [condition["description"] for condition in data["weather"]]
        if any(condition in weather_conditions for condition in [
            "light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain",
            "freezing rain", "light intensity shower rain", "shower rain", "heavy intensity shower rain",
            "ragged shower rain", "light intensity drizzle", "drizzle", "heavy intensity drizzle",
            "light intensity drizzle rain", "drizzle rain", "heavy intensity drizzle rain",
            "light shower sleet", "shower sleet", "light rain and snow", "rain and snow",
            "light shower snow", "shower snow", "heavy shower snow", "light rain and drizzle",
            "rain and drizzle", "heavy rain and drizzle"
        ]):
            print("Rainy Conditions")
            for condition in weather_conditions:
                if condition in [
                    "light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain",
                    "freezing rain", "light intensity shower rain", "shower rain", "heavy intensity shower rain",
                    "ragged shower rain", "light intensity drizzle", "drizzle", "heavy intensity drizzle",
                    "light intensity drizzle rain", "drizzle rain", "heavy intensity drizzle rain",
                    "light shower sleet", "shower sleet", "light rain and snow", "rain and snow",
                    "light shower snow", "shower snow", "heavy shower snow", "light rain and drizzle",
                    "rain and drizzle", "heavy rain and drizzle"
                ]:
                    print(f"- {condition}")
            return(True)
        else:
            print("No rain")
            return(False)
    else:
        print("City not found. Please try again.")

