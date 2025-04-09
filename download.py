import requests

def download_file():
    url = 'https://drive.google.com/uc?export=download&id=1t7c9GCwUNqI5elm6sG3bOIa5YtIDmx6n'
    filename = 'pp-2018.csv'
    
    print(f"Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Successfully downloaded {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

if __name__ == "__main__":
    download_file() 