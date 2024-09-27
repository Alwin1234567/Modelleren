import requests

class Distances:
    def __init__(self):
        self.base_url = "http://localhost:8989/route"

    def get_distance_and_time(self, coordinates):
        """
        Get the driving distance and time between a list of coordinates.

        Parameters:
        coordinates (list of tuples): List of (latitude, longitude) coordinates.

        Returns:
        dict: A dictionary with distances and durations.
        """
        if len(coordinates) < 2:
            raise ValueError("At least two coordinates are required")

        # Format coordinates for the GraphHopper API
        coord_str = '&'.join([f"point={lat},{lng}" for lat, lng in coordinates])
        
        # Define the parameters
        params = {
            'profile': 'car',
            'locale': 'en',
            'calc_points': 'false'
        }
        
        # Construct the full URL with parameters
        url = f"{self.base_url}?{coord_str}&profile={params['profile']}&locale={params['locale']}&calc_points={params['calc_points']}"
        print(url)
        
        # Print the URL for debugging
        print(f"Request URL: {url}")
        
        # Make the request to the GraphHopper API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'paths' in data and len(data['paths']) > 0:
                path = data['paths'][0]
                distance = path['distance']  # Distance in meters
                time = path['time']  # Time in milliseconds
                return {'distance': distance, 'time': time}
            else:
                raise ValueError("No route found")
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()

# Example usage
distances = Distances()
coordinates = [(52.07280854487388, 5.051941085326194),(52.30287630144949, 4.945374454652066)]
result = distances.get_distance_and_time(coordinates)
print(f"{result['distance']/1000} km")
print(f"{result['time']/1000/60} minutes")
