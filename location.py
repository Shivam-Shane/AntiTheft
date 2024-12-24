from geopy.geocoders import Nominatim
import subprocess
from logger import logging

# Initialize geolocator
geolocator = Nominatim(user_agent="location_finder")

def get_system_location(lat, lon,accuracy):
    """
    Get the system Location
    Args: Latitude: Latitude(degrees)
          Longitude: Longitude(degrees)
    Returns: String containing the system location and coordinates, location accuracy in meters
    """
    try:
        logging.info(f"Fetching location using latitude/longitude: {lat}, {lon}")
        # Reverse geocoding to get address from latitude/longitude
        location = geolocator.reverse((lat, lon), language="en", exactly_one=True)
        
        if location:
            address = location.address
            return f"""Estimated address::
            {address}

            Latitude: {lat}
            Longitude: {lon}
            Accuracy: {accuracy} Meters
            """
        else:
            return "Could not find a valid address."

    except Exception as e:
        return f"Error fetching location: {e}"

def get_location_corrdinates_powershell():
    """
    Get the system location corrdinates
    Args:   None
    Returns: latitude, longitude, and location accuracy in meters
    """
    try:
        logging.info("Fetching location coordinates using PowerShell")
        
        # PowerShell command to fetch location
        cmd = [
            "powershell",
            "-Command",
            (
                "Add-Type -AssemblyName System.Device; "
                "$geoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher; "
                "$geoWatcher.Start(); "
                "while (($geoWatcher.Status -ne 'Ready') -and ($geoWatcher.Permission -ne 'Denied')) "
                "{ Start-Sleep -Milliseconds 100 }; "
                "$coord = $geoWatcher.Position.Location; "
                "Write-Output ('{0},{1},{2}' -f $coord.Latitude, $coord.Longitude, $coord.HorizontalAccuracy)"
            )
        ]
        
        # Execute PowerShell command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        result.check_returncode()  # Raise exception if return code is non-zero
        
        # Parse and return coordinates
        lat, lon, accuracy = map(float, result.stdout.strip().split(","))
        return lat, lon, accuracy

    except subprocess.TimeoutExpired:
        logging.error("Timeout while fetching location.")
    except Exception as e:
        logging.error(f"Error fetching location: {e}")

def location_details():
    """
    Get the system location details, calls the helper function to get the location
    Args: None
    Return: Location Details
    """
    logging.info("Getting location details")
    coordinates = get_location_corrdinates_powershell()
    if coordinates:
        logging.info("Coordinates found, getting locations...")
        lan, lon, accuracy = coordinates
        return get_system_location(lan, lon, accuracy)
    else:
        return "Unable to fetch location"
