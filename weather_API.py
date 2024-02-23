import requests

def get_weather():
    """
    Fetches weather data for a selected city using OpenWeatherMap API and checks for rain conditions.

    Returns:
        bool: True if rain conditions are detected, False otherwise.
    """

    # our OpenWeatherMap API key
    api_key = "321c21a0e2a55554d0974bfc221939ad"

    # Specify the city for which to retrieve weather data
    city = "Kelaniya"

    # Build the API request URL with city and API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Send the request and get the response
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response data
        data = response.json()

        # Check if the API response contains valid data
        if "cod" in data and data["cod"] == 200:
            # Extract weather descriptions from the response
            weather_conditions = [condition["description"] for condition in data["weather"]]

            # Check if any of the descriptions indicate rain conditions
            if any(condition in weather_conditions for condition in [
                "light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain",
                "freezing rain", "light intensity shower rain", "shower rain", "heavy intensity shower rain",
                "ragged shower rain", "light intensity drizzle", "drizzle", "heavy intensity drizzle",
                "light intensity drizzle rain", "drizzle rain", "heavy intensity drizzle rain",
                "light shower sleet", "shower sleet", "light rain and snow", "rain and snow",
                "light shower snow", "shower snow", "heavy shower snow", "light rain and drizzle",
                "rain and drizzle", "heavy rain and drizzle"
            ]):
                # Print a message indicating rainy conditions
                print("Rainy Conditions")

                # Print detailed descriptions of the rain conditions
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

                # Return True to indicate rain detection
                return True

            else:
                # Print a message indicating no rain
                print("No rain")

                # Return False to indicate no rain detection
                return False

        else:
            # Print an error message if API response is invalid
            print("Invalid API response. Please check your API key or city name.")

    else:
        # Print an error message if the API request failed
        print(f"API request failed with status code: {response.status_code}")
