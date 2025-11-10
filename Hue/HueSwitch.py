import requests


class HueSwitch:
    """
    A simple controller for a Philips Hue light via the Hue Bridge REST API.
    """

    def __init__(self, bridge_ip, username, light_id):
        """
        Initialize the HueSwitch controller.

        Args:
            bridge_ip (str): IP address of your Hue Bridge (e.g. "192.168.1.10")
            username (str): Authorized API username (generated via Hue API)
            light_id (int): ID of the light you want to control
        """
        self.bridge_ip = bridge_ip
        self.username = username
        self.light_id = light_id
        self.base_url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"

    def turn_on(self):
        """Turn the light on."""
        payload = {"on": True}
        return self._send_request(payload)

    def turn_off(self):
        """Turn the light off."""
        payload = {"on": False}
        return self._send_request(payload)

    def _send_request(self, payload):
        """Internal helper to send a PUT request to the Hue Bridge."""
        try:
            response = requests.put(self.base_url, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_state(self):
        """Get current state of the light."""
        try:
            url = f"http://{self.bridge_ip}/api/{self.username}/lights/{self.light_id}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("state", {})
        except requests.RequestException as e:
            return {"error": str(e)}


    @classmethod
    def find_light_by_name(cls, bridge_ip, username, name):
        """
        Search all lights for one with the given name. Returns the light ID or None.
        """
        url = f"http://{bridge_ip}/api/{username}/lights"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            lights = response.json()
            for light_id, info in lights.items():
                if info.get("name") == name:
                    return int(light_id)
            return None
        except requests.RequestException as e:
            print(f"Error fetching lights: {e}")
            return None
