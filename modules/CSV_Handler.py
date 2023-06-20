import csv
import os
import asyncio

async def create_files_if_not_found():
    if not os.path.isfile("Valid_Adresses.csv"):
        with open("Valid_Adresses.csv", "w"):
            pass  # Creates an empty Valid_Adresses.csv if it doesn't exist

    if not os.path.isfile("IP_Port_Results.csv"):
        with open("IP_Port_Results.csv", "w"):
            pass  # Creates an empty IP_Port_Results.csv if it doesn't exist

    await asyncio.sleep(0)  # Return a coroutine object

async def write_to_valid_addresses(ip):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _write_to_valid_addresses, ip)

def _write_to_valid_addresses(ip):
    with open("Valid_Adresses.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip])

async def write_to_ip_port_results(ip, port, http_code):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _write_to_ip_port_results, ip, port, http_code)

def _write_to_ip_port_results(ip, port, http_code):
    with open("IP_Port_Results.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip, port, http_code])

def filter_http_codes():
    codes = set()
    with open("IP_Port_Results.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            codes.add(row[2])

def display_results():
    with open("IP_Port_Results.csv", "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

    choice = input("Do you want to filter HTTP codes? (Y/N): ")
    if choice.lower() == "y":
        code = input("Enter the HTTP code to filter: ")
        filtered_rows = []
        with open("IP_Port_Results.csv", "r", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == code:
                    filtered_rows.append(row)

        print("Filtered results:")
        for row in filtered_rows:
            print(row)
    else:
        print("No filtering applied.")
