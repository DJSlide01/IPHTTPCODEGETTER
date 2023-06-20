import asyncio
import modules.Scanner as scanner


async def menu():
    print("Scanner Menu:")
    print("1. Scan IP range")
    print("2. Scan single IP")
    print("3. Display results")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    return choice


async def run_scanner():
    while True:
        choice = await menu()

        if choice == 1:
            # Scan IP range
            start_ip = input("Enter the start IP address: ")
            end_ip = input("Enter the end IP address: ")
            start_port = input("Enter the start port range: ")
            end_port = input("Enter the end port range: ")
            await scanner.scan_ips_and_check_ports(start_ip, end_ip, start_port, end_port)
        elif choice == 2:
            # Scan single IP
            ip = input("Enter the IP address: ")
            start_port = input("Enter the start port range: ")
            end_port = input("Enter the end port range: ")
            await scanner.scan_and_check_single_ip(ip, start_port, end_port)
        elif choice == 3:
            # Display results
            scanner.csv_handler.display_results()

        elif choice == 4:
            # Exit the program
            break


if __name__ == "__main__":
    asyncio.run(run_scanner())
