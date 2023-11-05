# Importing webdriver from selenium
from selenium import webdriver
from PIL import Image
import os  # Import the os module
import time  # Import the time module

# Here Chrome will be used
driver = webdriver.Chrome()

# URL of the website
url = "http://127.0.0.1:8081/"


    # Opening the website
driver.get(url)

    # Check if the old image file exists and delete it
    # if os.path.exists("image.png"):
    #     os.remove("image.png")

    # Save a new screenshot
driver.save_screenshot("image.png")

    # Loading the new image
image = Image.open("image.png")

    # image.show()
