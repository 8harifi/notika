#!/usr/bin/env python3
"""
Simple script to test 404 page functionality
Run this after starting your Django server with DEBUG=False
"""

import requests
import sys

def test_404_page():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing 404 page functionality...")
    print("=" * 50)
    
    # Test 1: Direct 404 preview (should work with DEBUG=True or False)
    print("1. Testing 404 preview page...")
    try:
        response = requests.get(f"{base_url}/404-preview")
        if response.status_code == 200:
            print("✅ 404 preview page works!")
        else:
            print(f"❌ 404 preview failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Django is running!")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Test 404 error (should work with DEBUG=False)
    print("\n2. Testing 404 error page...")
    try:
        response = requests.get(f"{base_url}/test-404")
        if response.status_code == 404:
            print("✅ 404 error page works!")
        else:
            print(f"❌ 404 error failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test non-existent URL (should work with DEBUG=False)
    print("\n3. Testing non-existent URL...")
    try:
        response = requests.get(f"{base_url}/this-page-does-not-exist")
        if response.status_code == 404:
            print("✅ Non-existent URL shows 404!")
        else:
            print(f"❌ Non-existent URL failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("404 testing complete!")

if __name__ == "__main__":
    test_404_page()
