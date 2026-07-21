import sqlite3 as sqlite
import pyshortcuts as pyshort # https://github.com/newville/pyshortcuts - pip install pyshortcuts

from pathlib import Path


def decodeTitle(metadata, titleIDPos):
    titleID = bin(metadata[titleIDPos]).replace("0b", "")
    sizeID = int(titleID[:4], 2)

    str8, str16 = int("C", 16), int("D", 16) 


    # the length of the title is in the next byte
    if sizeID == str8:
        titleLen = metadata[titleIDPos + 1]
        titlePos = titleIDPos + 2

    # the length of the title is the next 2 bytes, as if the 1st of the 
    # two bytes was read together with the second byte. This is the limit
    # for medal names (280 charecters)

    elif sizeID == str16:
        byte1, byte2 = (
            bin(metadata[titleIDPos + i]).replace("0b", "") for i in (1, 2)
        )

        titleLen = int(byte1 + byte2, 2)
        titlePos = titleIDPos + 3

    # the length of the title is the 1st nibble of the titleID byte
    else:
        if sizeID == 0:
            return None
        
        titleLen = sizeID
        titlePos = titleIDPos + 1

    return metadata[titlePos : titlePos + titleLen]


# find db path
medalPath = Path(Path().home(), "AppData", "Roaming", "Medal") 

for path in medalPath.iterdir():
    if path.suffix == ".db":
        nIndex = len("medal-") # yields the index that's right after the hyphen, which includes only numbers
        
        if path.stem[nIndex].isnumeric(): # ignores medal-guest.db and CustomGameDatabase.db
            dbPath = medalPath / path.name
            print(f"Path to database: {dbPath}")
            
            break


# connect to sqlite database and get the video path and it's metadata
db = sqlite.connect(dbPath) 
resultSet = db.execute("SELECT video_path, metadata FROM contents")

print("Connected to database and executed query.")


unnamedCount = namedCount = 0

for path, metadata in resultSet: 
    # get the title, if it exists
    titleIDPos = metadata.index(b"title") + len("title") # byte that's after the title key
    title = decodeTitle(metadata, titleIDPos)

    if title is None:
        unnamedCount+=1
        continue
    else:
        namedCount+=1



'''
TODO:
- Save the clips as shortcuts in a folder to occupy almost no space
- Maybe save the clips to an album on Medal.
'''


