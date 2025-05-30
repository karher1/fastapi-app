import requests

url = "http://localhost:8002/jobs/16/description/stream"  # Updated URL with /jobs prefix

with requests.get(url, stream=True) as response:
    if response.status_code == 200:
        print("Streaming response:")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(chunk.decode('utf-8'), end="", flush=True)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
