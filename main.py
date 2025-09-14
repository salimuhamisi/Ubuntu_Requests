import requests
import os
import hashlib
from urllib.parse import urlparse

def is_valid_image(response):
    """Check if the response is an image by inspecting headers."""
    content_type = response.headers.get("Content-Type", "")
    return content_type.startswith("image/")

def get_unique_filename(filename, content):
    """Generate a unique filename if a duplicate exists (using hash)."""
    # Hash the content to avoid saving the same image twice
    file_hash = hashlib.md5(content).hexdigest()[:8]
    name, ext = os.path.splitext(filename)
    return f"{name}_{file_hash}{ext}"

def fetch_image(url):
    try:
        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        
        # Validate if it's an image
        if not is_valid_image(response):
            print(f"✗ Skipped (not an image): {url}")
            return
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"
        
        # Ensure file has valid extension
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            filename += ".jpg"
        
        filepath = os.path.join("Fetched_Images", filename)
        
        # Avoid duplicates: if file exists, generate unique filename
        if os.path.exists(filepath):
            filename = get_unique_filename(filename, response.content)
            filepath = os.path.join("Fetched_Images", filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)
    
    # Get multiple URLs (comma separated)
    urls = input("Please enter image URLs (separated by commas): ").split(",")
    urls = [u.strip() for u in urls if u.strip()]
    
    for url in urls:
        fetch_image(url)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
