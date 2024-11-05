Sun and Moon Simulation in 3D Space
Objective:
This project simulates the positions of the Sun and the Moon relative to Earth in 3D space, based on a specific location and time. The simulation places Earth at the center, with the Sun and Moon moving around it. Cardinal directions (N, S, E, W) are marked, and directional lines are drawn from Earth to the Sun and Moon to visualize their positions. The simulation also displays the azimuth and altitude angles for both the Sun and Moon.

Key Features:
3D Visualization: Earth is fixed at the center of the plot, while the Sun and Moon are shown at their respective positions above Earth.
Sun and Moon Positions: Calculated based on the local time at a specific location (latitude and longitude).
Directional Lines and Angles: Red and blue lines connect Earth to the Sun and Moon, respectively, with the azimuth and altitude angles annotated on the plot.
Cardinal Directions: The plot includes North (N), South (S), East (E), and West (W) directions around Earth for better orientation.
Dependencies:
The following Python libraries are required to run the simulation:

matplotlib (for plotting)
numpy (for mathematical calculations)
geopy (for geolocation and retrieving coordinates based on location)
datetime (for time-related calculations)
You can install the dependencies using pip:

bash
Copy code
pip install matplotlib numpy geopy
Methodology:
1. Geolocation and Local Time Calculation:
Input: The user provides a location, which can be a country name or specific latitude/longitude coordinates.
Process:
Using the geopy library, the latitude and longitude of the location are determined.
The local time is adjusted based on the longitude. The formula used to calculate the UTC offset is:
python
Copy code
UTC Offset = Longitude / 15
The local time is derived from the current UTC time, and the time is converted to decimal hours for easier calculations.
2. Azimuth and Altitude Calculation:
Input: Local time (in decimal hours) and the latitude of the observer.
Process:
The azimuth and altitude of both the Sun and Moon are calculated. These angles define their positions relative to the observer on Earth.
The Sun’s azimuth and altitude are calculated using simple sine and cosine functions, while the Moon's movement is slower and slightly adjusted to account for its orbital dynamics.
3. Spherical to Cartesian Coordinates Transformation:
Input: Azimuth and altitude (in degrees) of the Sun and Moon, along with their distance from Earth.
Process:
The azimuth and altitude are converted into radians.
Using the spherical coordinate system, the positions of the Sun and Moon are calculated in 3D space using the following formulas:
python
Copy code
x = distance * cos(altitude) * sin(azimuth)
y = distance * cos(altitude) * cos(azimuth)
z = distance * sin(altitude)
These calculated positions are used to plot the Sun and Moon in the 3D plot.
4. Visualization:
Earth:
Earth is represented as a sphere at the origin (0, 0, 0) with a green color. Its size is scaled down for visualization purposes.
Sun and Moon:
The Sun is represented by a large yellow sphere, and the Moon is represented by a smaller gray sphere. The positions of the Sun and Moon are scaled according to their distances from Earth.
Cardinal Directions:
Labels for North (N), South (S), East (E), and West (W) are placed around Earth to help orient the plot.
5. Plot Annotations:
Angles:
The azimuth and altitude angles for both the Sun and Moon are annotated on the plot. These angles are placed near the Sun and Moon, showing the observer's perspective.
Directional Lines:
Red lines connect Earth to the Sun, and blue lines connect Earth to the Moon, indicating their relative positions in the sky.
Code Explanation:
1. Geolocation and Time Calculation:
python
Copy code
# Function to convert azimuth and altitude to radians
def degrees_to_radians(degrees):
    return np.radians(degrees)

# Function to calculate Cartesian coordinates from Azimuth and Altitude
def calculate_position(azimuth, altitude, distance):
    azimuth_rad = degrees_to_radians(azimuth)
    altitude_rad = degrees_to_radians(altitude)
    x = distance * np.cos(altitude_rad) * np.sin(azimuth_rad)
    y = distance * np.cos(altitude_rad) * np.cos(azimuth_rad)
    z = distance * np.sin(altitude_rad)
    return x, y, z

# Function to get coordinates based on location input
def get_coordinates(location):
    geolocator = Nominatim(user_agent="sun_moon_simulator")
    location_data = geolocator.geocode(location)
    if location_data:
        return location_data.latitude, location_data.longitude
    return None, None

# Function to adjust time based on longitude
def adjust_time_for_location(longitude):
    utc_offset = longitude / 15
    current_time = datetime.utcnow()
    local_time = current_time + timedelta(hours=utc_offset)
    return local_time
2. Main Plotting Code:
python
Copy code
# Main code for input, calculation, and plotting
location_input = input("Enter location (country or latitude,longitude): ")
local_hour = get_local_time(location_input)
latitude, longitude = get_coordinates(location_input)
sun_azimuth, sun_altitude, moon_azimuth, moon_altitude = get_sun_and_moon_positions(local_hour, latitude)

# Calculate positions of Sun and Moon
earth_radius = 6371  # Earth's radius in kilometers (scaled)
sun_radius = 696340  # Sun's radius in kilometers (scaled)
moon_radius = 1737.1  # Moon's radius in kilometers (scaled)

# Scaled down for visualization
sun_size = sun_radius / 100000  # Scaled size of the Sun for visualization
earth_size = earth_radius / 1000  # Scaled size of the Earth
moon_size = moon_radius / 100  # Scaled size of the Moon

# The distance from Earth to Moon and Earth to Sun (scaled down)
moon_distance = 384400 / 1000  # Scaled distance from Earth to Moon
sun_distance = 149600000 / 100000  # Scaled distance from Earth to Sun

# Calculate positions in 3D (scaled for simulation)
sun_x, sun_y, sun_z = calculate_position(sun_azimuth, sun_altitude, sun_distance)
moon_x, moon_y, moon_z = calculate_position(moon_azimuth, moon_altitude, moon_distance)

# Create a larger 3D plot
fig = plt.figure(figsize=(14, 12))  # Increase the figure size
ax = fig.add_subplot(111, projection='3d')

# Plot Earth as a sphere at the bottom plane (z=0)
ax.plot_surface(x, y, z, color='g', alpha=0.6, label="Earth")
Running the Simulation:
Input Location: When you run the script, you will be prompted to input a location (either a country name or specific latitude/longitude coordinates).
Get Time and Position Data: The script calculates the local time and determines the Sun’s and Moon’s azimuth and altitude for the given location.
Visualization: A 3D plot is generated showing:
Earth at the center
The Sun and Moon at their respective positions relative to Earth
Cardinal directions (N, S, E, W)
Directional lines indicating the position of the Sun and Moon
Conclusion:
This simulation effectively visualizes the positions of the Sun and the Moon based on the user’s location and current time. The 3D plot helps to understand the relative movement of these celestial bodies in the sky. The calculation of azimuth and altitude angles allows for an accurate representation of the Sun and Moon’s positions.

Feel free to adjust the code or contribute improvements to enhance the simulation. You can fork or clone this repository to experiment with different models or add additional features, such as including other celestial bodies or improving the Sun and Moon movement models.

