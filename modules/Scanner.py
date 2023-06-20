import requests
import asyncio
import csv
import os
import socket
import modules.CSV_Handler as csv_handler
import modules.HTTP_HTTPS_Handler as http_handler
from modules.Ranges import IPRange, PortRange
import ipaddress
from concurrent.futures import ThreadPoolExecutor


MAX_THREADS = 1000  # Maximum number of threads for scanning
MAX_WORKERS_PER_THREAD = 250  # Maximum number of workers per thread


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


async def scan_ips(start_ip, end_ip):
    ip_range = IPRange(start_ip, end_ip)
    valid_ips = []  # To store valid IP addresses

    async def scan_ip(ip):
        if is_valid_ip(ip):
            valid_ips.append(ip)
            await csv_handler.write_to_valid_addresses(ip)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS_PER_THREAD) as executor:
        loop = asyncio.get_running_loop()
        tasks = []
        for ip in ip_range.get_ip_range():
            task = loop.run_in_executor(executor, scan_ip, ip)
            tasks.append(task)

        await asyncio.gather(*tasks)

    return valid_ips


async def check_ports(valid_ips, start_port, end_port):
    port_range = PortRange(int(start_port), int(end_port))  # Convert to integers

    async def check_port(ip, port):
        resolved_ip = await resolve_ip(ip)  # Resolve IP if it is a hostname
        http_task = asyncio.create_task(http_handler.get_http_code(resolved_ip, port))
        https_task = asyncio.create_task(http_handler.get_https_code(resolved_ip, port))

        try:
            await asyncio.gather(http_task, https_task)  # Wait for both tasks to complete
        except:
            http_task.cancel()
            https_task.cancel()
            raise

    tasks = []
    for ip in valid_ips:
        for port in port_range.get_port_range():
            print(f"Checking port {port}")
            task = asyncio.create_task(check_port(ip, port))
            tasks.append(task)

    print("Waiting on requests and writing")
    await asyncio.gather(*tasks)
    print("Port checking complete")  # Display status when all tasks are finished

def is_valid_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


async def resolve_ip(ip):
    try:
        return socket.gethostbyname(ip)  # Resolve hostname to IP address
    except socket.error:
        return ip  # Return the original IP if it's already an IP address


async def scan_ips_and_check_ports(start_ip, end_ip, start_port, end_port):
    valid_ips = await scan_ips(start_ip, end_ip)
    await check_ports(valid_ips, start_port, end_port)


async def scan_and_check_single_ip(ip, start_port, end_port):
    valid_ips = [ip]
    await check_ports(valid_ips, start_port, end_port)


async def run_scanner():
    await csv_handler.create_files_if_not_found()  # Create Valid_Adresses.csv and IP_Port_Results.csv if not found

    while True:
        clear_terminal()
        choice = await menu()

        if choice == 1:
            await csv_handler.delete_valid_addresses()  # Clear Valid_Adresses.csv
            await csv_handler.delete_ip_port_results()  # Clear IP_Port_Results.csv
            start_ip = input("Enter the start IP address: ")
            end_ip = input("Enter the end IP address: ")
            start_port = input("Enter the start port range: ")
            end_port = input("Enter the end port range: ")
            await scan_ips_and_check_ports(start_ip, end_ip, start_port, end_port)
        elif choice == 2:
            await csv_handler.delete_valid_addresses()  # Clear Valid_Adresses.csv
            await csv_handler.delete_ip_port_results()  # Clear IP_Port_Results.csv
            ip = input("Enter the IP address: ")
            start_port = input("Enter the start port range: ")
            end_port = input("Enter the end port range: ")
            await scan_and_check_single_ip(ip, start_port, end_port)
        elif choice == 3:
            csv_handler.display_results()
            break


if __name__ == "__main__":
    asyncio.run(run_scanner())
