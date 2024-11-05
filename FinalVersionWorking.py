import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

# Convert azimuth and altitude to radians
def degrees_to_radians(degrees):
    return np.radians(degrees)

# Function to calculate the Cartesian coordinates based on Azimuth and Altitude
def calculate_position(azimuth, altitude, distance):
    # Convert azimuth and altitude to radians
    azimuth_rad = degrees_to_radians(azimuth)
    altitude_rad = degrees_to_radians(altitude)
    
    # Calculate Cartesian coordinates with distance (scaled for simulation)
    x = distance * np.cos(altitude_rad) * np.sin(azimuth_rad)  # East-West (x-axis)
    y = distance * np.cos(altitude_rad) * np.cos(azimuth_rad)  # North-South (y-axis)
    z = distance * np.sin(altitude_rad)  # Altitude (z-axis)
    
    return x, y, z

# Function to get latitude and longitude based on country or coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="sun_moon_simulator")
    try:
        location_data = geolocator.geocode(location)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            raise ValueError("Location not found.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Function to adjust the time based on longitude (Longitude affects the time zone)
def adjust_time_for_location(longitude):
    utc_offset = longitude / 15  # Time zone offset based on longitude
    current_time = datetime.utcnow()  # Get current UTC time
    local_time = current_time + timedelta(hours=utc_offset)  # Adjust current time to local time
    return local_time

# Get the current time and extract the hour of the day
def get_local_time(location):
    latitude, longitude = get_coordinates(location)
    if latitude is None or longitude is None:
        return None
    local_time = adjust_time_for_location(longitude)
    return local_time.hour + local_time.minute / 60  # Convert time to decimal hours

# Given Azimuth and Altitude for Sun and Moon
def get_sun_and_moon_positions(hour, latitude):
    sun_t = (hour / 24) * 2 * np.pi  # Normalize hour to radians for smooth movement
    sun_azimuth = (sun_t + np.pi) % (2 * np.pi)  # Azimuth calculation (relative to local time)
    sun_altitude = 90 - latitude  # Altitude based on latitude (simplified)
    
    moon_t = (hour / 24) * np.pi  # Moon moves more slowly than the Sun
    moon_azimuth = (moon_t + np.pi) % (2 * np.pi)  # Azimuth calculation
    moon_altitude = 90 - latitude + 10 * np.sin(moon_t)  # Some variation in altitude
    
    return np.degrees(sun_azimuth), 90 - np.degrees(sun_altitude), np.degrees(moon_azimuth), 90 - np.degrees(moon_altitude)

# Input location (can be country or specific coordinates)
location_input = input("Enter location (country or latitude,longitude): ")

# Get the local time (in decimal hours)
local_hour = get_local_time(location_input)

# If location not found, exit
if local_hour is None:
    print("Invalid location, unable to get local time.")
    exit()

# Get the latitude from the location input
latitude, longitude = get_coordinates(location_input)

# Get Sun and Moon azimuth and altitude at the current local time
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

# Plot Earth, Sun, and Moon with their respective sizes using spheres
# Earth (small green sphere)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = earth_size * np.outer(np.cos(u), np.sin(v))
y = earth_size * np.outer(np.sin(u), np.sin(v))
z = earth_size * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='g', rstride=5, cstride=5, alpha=0.6, label="Earth")

# Sun (large yellow sphere)
x_sun = sun_size * np.outer(np.cos(u), np.sin(v))
y_sun = sun_size * np.outer(np.sin(u), np.sin(v))
z_sun = sun_size * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_sun + sun_x, y_sun + sun_y, z_sun + sun_z, color='yellow', rstride=5, cstride=5, alpha=0.9, label="Sun")

# Moon (smaller gray sphere)
x_moon = moon_size * np.outer(np.cos(u), np.sin(v))
y_moon = moon_size * np.outer(np.sin(u), np.sin(v))
z_moon = moon_size * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_moon + moon_x, y_moon + moon_y, z_moon + moon_z, color='gray', rstride=5, cstride=5, alpha=0.7, label="Moon")

# Plot lines connecting Earth to Sun and Moon
ax.plot([0, sun_x], [0, sun_y], [0, sun_z], 'r-', label="Earth-Sun line")
ax.plot([0, moon_x], [0, moon_y], [0, moon_z], 'b-', label="Earth-Moon line")

# Cardinal directions for Earth (N, E, S, W)
ax.text(earth_size * 1.5, 0, 0, 'E', color='black', fontsize=14, fontweight='bold')
ax.text(-earth_size * 1.5, 0, 0, 'W', color='black', fontsize=14, fontweight='bold')
ax.text(0, earth_size * 1.5, 0, 'N', color='black', fontsize=14, fontweight='bold')
ax.text(0, -earth_size * 1.5, 0, 'S', color='black', fontsize=14, fontweight='bold')

# Annotate Azimuth and Altitude Angles with lines from Earth
ax.text(sun_x / 2, sun_y / 2, sun_z / 2, f'Sun Azimuth: {sun_azimuth:.2f}°', color='red', fontsize=12)
ax.text(sun_x / 2, sun_y / 2, sun_z / 1.5, f'Sun Altitude: {sun_altitude:.2f}°', color='red', fontsize=12)

ax.text(moon_x / 2, moon_y / 2, moon_z / 2, f'Moon Azimuth: {moon_azimuth:.2f}°', color='blue', fontsize=12)
ax.text(moon_x / 2, moon_y / 2, moon_z / 1.5, f'Moon Altitude: {moon_altitude:.2f}°', color='blue', fontsize=12)

# Add some random stars for background
num_stars = 100
star_x = np.random.uniform(-1.5, 1.5, num_stars)
star_y = np.random.uniform(-1.5, 1.5, num_stars)
star_z = np.random.uniform(-1.5, 1.5, num_stars)
ax.scatter(star_x, star_y, star_z, color='white', s=1, alpha=0.7, label="Stars")

# Labels and title
ax.set_xlabel("X (East-West)")
ax.set_ylabel("Y (North-South)")
ax.set_zlabel("Z (Altitude)")
ax.set_title(f"Sun & Moon Positions - {location_input} at {local_hour:.2f} hours")

# Show legend
ax.legend()

# Display the plot
plt.show()
