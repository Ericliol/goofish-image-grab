import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def grab_images(html_file, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    
    # Step 1: Load rendered HTML from file
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Step 2: Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Step 3: Find the div with class that starts with 'item-main-container--'
    container = soup.find("div", class_=lambda x: x and x.startswith("item-main-container--"))
    if not container:
        print("No item-main-container found.")
        return
    
    # Step 4: Find all <img> tags inside that container
    img_tags = container.find_all("img")
    if not img_tags:
        print("No images found in container.")
        return
    max_imagine_count = 9
    img_tags = img_tags[max_imagine_count:max_imagine_count*2]
    
    print(f"Found {len(img_tags)} images in the container.")
    
    # Step 5: Process each image
    for i, img_tag in enumerate(img_tags):
        if not img_tag.get("src"):
            print(f"Image {i+1} has no src attribute. Skipping.")
            continue
        
        img_url = img_tag["src"]
        
        # Fix image URL if needed
        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif img_url.startswith("/"):
            img_url = "https://www.goofish.com" + img_url
        
        try:
            print(f"Downloading image {i+1} from: {img_url}")
            
            # Download the image
            response = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            
            # Generate a filename for the image
            filename = f"image_{i+1}.png"
            output_path = os.path.join(output_folder, filename)
            
            # Convert to PNG and save
            image = Image.open(BytesIO(response.content))
            image.convert("RGB").save(output_path, "PNG")
            print(f"Image {i+1} saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing image {i+1}: {e}")

if __name__ == "__main__":
    # You can change these parameters
    html_file = "goofish_item_rendered.html"
    output_folder = "goofish_images"  # Change this to your desired folder name
    
    grab_images(html_file, output_folder)
    print("Image extraction completed.")