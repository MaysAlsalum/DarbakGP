import kagglehub
import os
import shutil

DATASET = "mohammedalsubaie/ksa-regions-cities-and-districts"

path = kagglehub.dataset_download(DATASET)
print("Downloaded to cache:", path)

target = "data/raw/ksa_regions_cities_districts"
os.makedirs(target, exist_ok=True)

shutil.copytree(path, target, dirs_exist_ok=True)
print("Copied to project:", target)