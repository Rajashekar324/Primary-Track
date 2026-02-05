import urllib.request
import threading
import time

files = [
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/comments",
    "https://jsonplaceholder.typicode.com/albums"
]

def download(url, filename):
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, filename)
    print(f"{filename} downloaded")

threads = []
start = time.time()

for i, url in enumerate(files):
    t = threading.Thread(target=download, args=(url, f"file{i}.json"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All downloads completed")
print("Time taken:", time.time() - start)