from fastapi import FastAPI, HTTPException
# HTTPException lets us return actual HTTP error responses (like 400 or 404) instead of crashing
from fastapi.responses import HTMLResponse
# HTMLResponse imports a response type that tells FastAPI to send back HTML instead of JSON
from fastapi.staticfiles import StaticFiles
# StaticFiles imports a utility that serves files (like images) directly from a directory
import os
# Python’s operating system utilities, used for working with directories & file paths
import random
# Imports the random module so we can randomly choose an image
from typing import Optional
# Imports the Optional type hint. This allows a function parameter to be either a string or None
app = FastAPI()

# Directory where images are stored
cat_pic_dir = "cat_pictures_api/images"

# Make sure that directory exists (if not, make it)
if not os.path.exists(cat_pic_dir):
  os.makedirs(cat_pic_dir)

# We didn't do this in the basic app. This defines the function to run when GET requests to the root path are made
@app.get("/")
def read_root():
    return {"message": "Welcome to the Cat Pics API. Use /random to get a random picture of our cats."}
  
@app.get("/random")
def get_random_image(cat_name: Optional[str] = None):
  # Our first query parameter. cat_name is OPTIONAL; if not provided, defaults to None
  # Lists all image files in the directory.
  image_files = [f for f in os.listdir(cat_pic_dir) if os.path.isfile(os.path.join(cat_pic_dir, f))]

  display_name = "Our Cats"
  # this is a nicety; sets a default display name that can be modified if cat_name is specified
  
  # Filter by cat name if specified
  if cat_name:
    cat_name = cat_name.lower()
    if cat_name not in ["gal", "oppie"]:
      raise HTTPException(status_code=400, detail="Cat name must be Gal or Oppie")
    # We are setting up a specific error! if the user specifies a cat name that doesn't match one of our two cats, they'll get an Error Code 400. 400 means "Bad request"
    
    image_files = [f for f in image_files if cat_name in f.lower()]
    # filters the image list to only files that contain cat name

    if cat_name == "gal":
       display_name = "Galavant"
    elif cat_name == "oppie":
       display_name = "Opal"
    
  # Check if there are any images that reamined after filtering; if not, give an error
  if not image_files:
    raise HTTPException(status_code=404, detail="No images found")
  # Here we use error code 404, which means "Not found"
  
  # Select a random image
  random_image = random.choice(image_files)
  image_url = f"/images/{random_image}"
  # Build a URL pointing to that image using the /images static route

# Create a multi-line HTML string. The display_name and image_url values are inserted dynamically
  html_content = f"""
    <html>
        <head>
            <title>Random Picture of {display_name}</title>
        </head>
        <body>
            <h1>Random picture of {display_name}</h1>
            <img src="{image_url}" alt="Random Image" style="max-width: 30%; height: auto;">
        </body>
    </html>
    """
    
  return HTMLResponse(content=html_content)
# Return the HTML string as an HTML response instead of JSON. this is so the picture is displayed in the browser

app.mount("/images", StaticFiles(directory=cat_pic_dir), name="images")
# Mounts the image directory so files can be accessed at /images/<filename>. This is what makes the <img src="..."> tag work, otherwise no pictures would actually be displayed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# source this file with python cat_pictures_api/app.py in terminal,
# then go to localhost:8000/ or localhost:8000/random
# documentation is automatically generated at http://localhost:8000/docs
# Now let's let you all try it out