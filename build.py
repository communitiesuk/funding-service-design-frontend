import urllib.request
import zipfile
import shutil
import os
print("Downloading static file zip.")
url = 'https://github.com/alphagov/govuk-frontend/releases/download/v4.0.0/release-v4.0.0.zip'
urllib.request.urlretrieve(url, './govuk_frontend.zip')
print("Deleting old app/static")
try:
    shutil.rmtree("./app/static")
except FileNotFoundError:
    print("No old app/static to remove.")
print("Unzipping file to app/static...")
with zipfile.ZipFile("./govuk_frontend.zip", 'r') as zip_ref:
    zip_ref.extractall("./app/static")
print("Moving files from app/static/assets to app/static")
for file_to_move in os.listdir("./app/static/assets"):
    shutil.move("./app/static/assets/" + file_to_move, "./app/static")
print("Deleting app/static/assets")
shutil.rmtree("./app/static/assets")
print("Deleting govuk_frontend.zip")
os.remove("./govuk_frontend.zip")