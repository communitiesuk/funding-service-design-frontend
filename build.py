import os
import shutil
import urllib.request
import zipfile


# Download zips using "url"
print("Downloading static file zip.")

url = (
    "https://github.com/alphagov/govuk-frontend/"
    "releases/download/v4.0.0/release-v4.0.0.zip"
)

# There is a known problem on Mac where one must manually
# run the script "Install Certificates.command" found
# in the python application folder for this to work.
urllib.request.urlretrieve(url, "./govuk_frontend.zip")

print("Deleting old app/static")

# Attempts to delete the old files, states if
# one doesnt exist.
try:
    shutil.rmtree("app/static")
except FileNotFoundError:
    print("No old app/static to remove.")

print("Unzipping file to app/static...")

# Extracts the previously downloaded zip to /app/static
with zipfile.ZipFile("./govuk_frontend.zip", "r") as zip_ref:
    zip_ref.extractall("./app/static")

print("Moving files from app/static/assets to app/static")

for file_to_move in os.listdir("./app/static/assets"):
    shutil.move("./app/static/assets/" + file_to_move, "app/static")

print("Deleting app/static/assets")

# Deletes temp. files.
shutil.rmtree("./app/static/assets")
os.remove("./govuk_frontend.zip")
