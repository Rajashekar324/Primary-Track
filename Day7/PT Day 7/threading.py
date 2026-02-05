# import threading
# import time
# def say_hello():
#     print("hello world")

# t=threading.Thread(target=say_hello)
# t.start()

# print("MAin Thread")

# def task():
#     print("task started")
#     time.sleep(2)
#     print("task completed")
# task()
# print("Program finished")

# # why we need a threading
# # one task is waiting(like downloading,sleeping,input/output) and for program to stay responsive
# # ex: downloading a file,showing progress,accepting user input

# #passing arguments to thread
# import threading
# def greet(name):
#     print("Hello,{name}")
# t=threading.Thread(target=greet,args=("Alice"))
# t.start()

# def greet(name):
#     time.sleep(2)   
#     print(f"Hello, {name}!")
# greet("Alice")

# Multi threading
# def worker(num):
#     print(f"Worker {num} is starting")
#     time.sleep(2)
#     print(f"Worker {num} is done")

# for i in range(5):
#     t=threading.Thread(target=worker,args=(i,))
#     t.start()


#downlading files using multithreading
# import urllib.request
# import time
# import json
# import ssl

# def download_json():
#     try:
#         print("Connecting to API...")
#         time.sleep(2)

#         url = 'https://fakestoreapi.com/products'
#         headers = {
#             "User-Agent": "Mozilla/5.0"
#         }

#         req = urllib.request.Request(url, headers=headers)
#         context = ssl._create_unverified_context()

#         with urllib.request.urlopen(req, context=context) as response:
#             data = response.read()

#         print("Data downloaded")

#         posts = json.loads(data)

#         with open('posts.json', 'w') as f:
#             json.dump(posts, f, indent=4)

#         print("Download complete")

#     except Exception as e:
#         print("Error:", e)
# download_json()

# print("Program finished")

# from multiprocessing import Process

# def worker_function():
#     print("Worker is running")

# if __name__ == "__main__":
#     p = Process(target=worker_function)
#     p.start()
#     p.join()

#     print("Main process is done")

# import time
# from multiprocessing import Pool
# def square(n):
#     return n * n
# if __name__ == "__main__":
#     numbers = [10**7,10**2,10**3,10**4,10**5]
#     start=time.time()
#     with Pool() as p:
#         result=p.map(square,numbers)
#     end=time.time()
#     print("Squares:",result)
#     print("Time taken with multiprocessing:",end-start)

# from multiprocessing import Pool
# import time
# def simulate_region(region):
#     print(f"Calculating weather for {region}...")
#     time.sleep(1)
#     result = f"region {region} complete"
#     return result

# if __name__ == "__main__":
#     regions = ['North', 'South', 'East', 'West']

#     with Pool(processes=4) as p:
#         result=p.map(simulate_region, regions)

#     print("Results:", result )

from multiprocessing import Pool
import time
def analyze_log(chunk):
    print(f"Analyzing log chunk {chunk}...")
    time.sleep(1)
    result = f"log chunk {chunk} analyzed"
    return result
if __name__ == "__main__":
    log_chunks = [1, 2, 3, 4]
    with Pool(4) as p:
        result = p.map(analyze_log, log_chunks)
    print("Analysis Results:", result)