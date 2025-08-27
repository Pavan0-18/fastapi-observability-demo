#!/usr/bin/env python3
"""
Traffic simulator to generate load on the demo service
"""
import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000"

def make_request():
    """Make a single request to a random endpoint"""
    endpoints = ["/", "/health", "/simulate-work"]
    endpoint = random.choice(endpoints)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        print(f"✓ {endpoint} -> {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"✗ {endpoint} -> Error: {e}")
        return None

def generate_traffic(duration_seconds=300, requests_per_second=2):
    """Generate continuous traffic for specified duration"""
    print(f"Starting traffic generation for {duration_seconds} seconds")
    print(f"Target: {requests_per_second} requests per second")
    
    end_time = time.time() + duration_seconds
    request_interval = 1.0 / requests_per_second
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while time.time() < end_time:
            # Submit request
            executor.submit(make_request)
            
            # Add some randomness to avoid perfect timing
            sleep_time = request_interval + random.uniform(-0.1, 0.1)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    print("Traffic generation completed!")

def burst_traffic():
    """Generate burst traffic patterns"""
    print("Generating burst traffic...")
    
    # Generate 20 concurrent requests
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(make_request) for _ in range(20)]
        
        # Wait for all to complete
        for future in futures:
            future.result()
    
    print("Burst traffic completed!")

if __name__ == "__main__":
    print("Demo Service Traffic Simulator")
    print("=" * 40)
    
    while True:
        print("\nSelect traffic pattern:")
        print("1. Continuous traffic (5 minutes)")
        print("2. Burst traffic")
        print("3. Custom continuous traffic")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            generate_traffic(300, 2)  # 5 minutes, 2 req/sec
        elif choice == "2":
            burst_traffic()
        elif choice == "3":
            try:
                duration = int(input("Duration (seconds): "))
                rps = float(input("Requests per second: "))
                generate_traffic(duration, rps)
            except ValueError:
                print("Invalid input. Please enter numbers.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select 1-4.")
    
    print("Goodbye!")