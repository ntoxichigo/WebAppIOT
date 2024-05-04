import json
import random
import time
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=AntonioIOT.azure-devices.net;DeviceId=Raspberrydevice;SharedAccessKey=m2BKMIPo9kzNGIxOzs6WrWhqpWEcIKPd6AIoTMa/b+o="

# Global variable to keep track of the light state
LIGHT_STATE = False


def simulate_light_sensor_data():
    # Simulate light sensor data
    return random.randint(0, 100)


def control_virtual_light(state):
    global LIGHT_STATE
    LIGHT_STATE = state
    print(f"Virtual light is now {'ON' if state else 'OFF'}")

    # Send a message to the simulator to control the LED
    message = Message(json.dumps({"command": "setLED", "state": state}))
    device_client.send_message(message)
    print("LED control message sent to Azure IoT Hub")


def send_telemetry(light_level):
    # Create a JSON message with the light sensor data and light state
    message_json = {"lightLevel": light_level, "lightState": LIGHT_STATE}
    message = Message(json.dumps(message_json))

    # Send the message to Azure IoT Hub
    device_client.send_message(message)
    print("Telemetry message sent to Azure IoT Hub")


def main():
    global device_client

    # Create an IoT Hub device client
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Connect the device client
    device_client.connect()

    while True:
        # Simulate light sensor data
        light_level = simulate_light_sensor_data()
        print(f"Light level: {light_level}")

        # Send telemetry to Azure IoT Hub
        send_telemetry(light_level)

        # Control the virtual light based on the light level
        if light_level < 50:
            control_virtual_light(True)
        else:
            control_virtual_light(False)

        # Wait for a specific interval before sending the next message
        time.sleep(5)


if __name__ == "__main__":
    main()