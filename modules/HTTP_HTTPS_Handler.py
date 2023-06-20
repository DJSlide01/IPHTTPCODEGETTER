import modules.CSV_Handler as csv_handler
import aiohttp

async def get_http_code(ip, port):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"http://{ip}:{port}") as response:
                status_code = response.status
                await csv_handler.write_to_ip_port_results(ip, port, status_code)
        except aiohttp.ClientError:
            pass

async def get_https_code(ip, port):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://{ip}:{port}") as response:
                status_code = response.status
                await csv_handler.write_to_ip_port_results(ip, port, status_code)
        except aiohttp.ClientError:
            pass
