import os
servers = ["8.8.8.8", "google.com"]
for server in servers:
    os.system(f"ping -n 1 {server}")