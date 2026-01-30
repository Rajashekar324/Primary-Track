import psutil
import time

while True:
    print("CPU:", psutil.cpu_percent(), "% | RAM:", psutil.virtual_memory().percent, "%")
    time.sleep(2)