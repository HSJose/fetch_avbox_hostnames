import httpx
from rich import print
from os import getenv


def fetch_data(api_url):
    with httpx.Client() as client:
        response = client.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None


def parse_data(api_url):
    data = fetch_data(api_url)
    if data is None:
        return
    
    hostnames_set = set()
    
    for device in data.get("devices", []):  # extracting devices from the data
        avbox_info = device.get("avbox_info", {})

        if avbox_info:
            for av_device in avbox_info.get("devices", []):
                parsed_hostname = av_device.split("@")[-1]
                hostnames_set.add(parsed_hostname)
            hostnames_set.add(device["hostname"])
    
    return hostnames_set


def main():
    api_key = getenv("HS_API_KEY")
    api_url = f"https://{api_key}@api-dev.headspin.io/v0/devices"
    # raw_data = fetch_data(api_url)
    hostnames = parse_data(api_url)
    print("AV_Box Hostnames:")
    print(hostnames)

# Run the function
main()
