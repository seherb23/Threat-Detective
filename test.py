import requests
import monitor

while True:
    user_input = input("Enter an input: ")
    response = monitor.handle_request(user_input)
    print("Ran handle_request with input", user_input, "| Response was", response)