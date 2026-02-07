from os import path, mkdir
import json

def download(url:str, filename:str, download_data:dict):
   if not path.isdir("./Downloads/"): mkdir("./Downloads/")
   filename_noext = filename.split(".")[0]
   target_path = str("./Downloads/" + filename_noext)
   metadata = dict()
   if not path.isdir(target_path):
      metadata = {
         "filename": filename,
         "filesize": download_data["filesize"],
         "finished": False
      }
      mkdir(target_path)
      with open(target_path+"/metadata.json", "w") as metadata_file:
         json.dump(metadata, metadata_file, indent=3)