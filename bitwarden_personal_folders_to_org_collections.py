import json
import time

# Folder to Collection mapping
# Determined by exporting folders from personal vault and
# creating dummy collections in Org and exporting both.
# This version is sanitised.
folderCollectionMapping = [
    {
      "origName":"Shared folder 1",
      "organizationId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "My Collection",
      "externalId": null
      "catchAll": False
    },
    {      
      "origName":"Shared folder 2",
      "organizationId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "My Collection",
      "externalId": null
      "catchAll": False
    },
    {       
      "origName":"Shared folder 3",
      "organizationId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "My Collection",
      "externalId": null
      "catchAll": True
    },
]

# Writes the collections information at the top of the file.
def createStaticCollections(folderCollectionMap: dict):
    collections = []
    for mapping in folderCollectionMap:
       tmp_map = mapping.copy()
       tmp_map.pop("origName")
       tmp_map.pop("catchAll")
       collections.append(tmp_map)
    return collections
    
# Finds items in the orginal export based on the shared folder name.
# Updates the organizationId, collectionIds and sets folderId to null.
# returns list of items
def findItems(data, folderName: str, collectionId: str, catchAll: bool):
    shared_items = []
    folders = []
    for folder in data["folders"]:
        name = folder["name"]
        if folderName in name:
            folders.append(folder["id"])

    itemcnt = 0
    for item in data["items"]:
        if catchAll or item["folderId"] in folders:
            itemcnt = itemcnt + 1
            shared_items.append(item)
    data["items"][:] = [x for x in data["items"] if not (x["folderId"] in folders)]  

    for item in shared_items:
        item["organizationId"] = "REPLACE_WITH_YOUR_ORG_ID"
        item["collectionIds"] = [collectionId,]
        item["folderId"] = None

    return shared_items

with open("BITWARDEN_EXPORT_PERSONAL_FOLDERS", "r") as read_file:
    data = json.load(read_file)
    jsonout = {}
    collections = createStaticCollections(folderCollectionMapping)
    jsonout["encrypted"] = False
    jsonout["collections"] = collections
    jsonout["items"] = []
     
    for mapping in folderCollectionMapping:
        items = findItems(data, mapping["origName"], mapping["id"], mapping["catchAll"])
        if len(items) > 0:
            jsonout["items"] = jsonout["items"] + items
   
    # Write json to file.
    timestr = time.strftime("%Y%m%d-%H%M%S")
    jsonFilename = "bitwarden_" + timestr + ".json"
    with open(jsonFilename, "w") as data_file:
        json.dump(jsonout, data_file, indent=2)

        
