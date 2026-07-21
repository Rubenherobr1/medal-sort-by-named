import sqlite3 as sqlite
from pathlib import Path


def normBin(decimalByte):
    byte = bin(decimalByte).replace("0b", "")
    byte = "0" * (8 - len(byte)) + byte # ensures the representation will have 8 bytes regardless

    return byte


def decodeTitle(metadata, titleIDPos):
    titleID = normBin(metadata[titleIDPos])
    sizeID = int(titleID[:4], 2)
    
    str8, str16 = int("C", 16), int("D", 16) 


    # the length of the title is in the next byte
    if sizeID == str8:
        titleLen = metadata[titleIDPos + 1]
        titlePos = titleIDPos + 2

    # the length of the title is the next 2 bytes, as if the 1st of the 
    # two bytes was read together with the second byte. This is the limit
    # for medal clip names (280 bytes)

    elif sizeID == str16:
        byte1, byte2 = (
            normBin(metadata[titleIDPos + i]) for i in (1, 2)
        )

        titleLen = int(byte1 + byte2, 2)
        titlePos = titleIDPos + 3

    # the length of the title is the 1st nibble of the titleID byte
    else:
        if sizeID == 0:
            return None
        
        titleLen = sizeID
        titlePos = titleIDPos + 1

    return metadata[titlePos : titlePos + titleLen].decode("utf-8")


# find db path
medalPath = Path(Path.home(), "AppData", "Roaming", "Medal")

for path in medalPath.iterdir():
    if path.suffix == ".db":
        nIndex = len("medal-") # yields the index that's right after the hyphen, which includes only numbers if its the target db
        
        if path.stem[nIndex].isnumeric(): # ignores medal-guest.db and CustomGameDatabase.db
            dbPath = medalPath / path.name
            print(f"Path to database: {dbPath}")
            
            break


# connect to sqlite database and get the video id, path and it's metadata
db = sqlite.connect(dbPath) 
resultSet = db.execute("SELECT remote_content_id, video_path, metadata FROM contents")

print("Connected to database and executed query\n")


# create the folder if it dosen't exist yet
clipsDir = Path("Named-clips")
clipsDir.mkdir(exist_ok=True)


MAX_PATH_LEN = 260 # on Windows. Bigger paths can exist on linux
titleList = [] # used to see how many times a title repeat

for id, path, metadata in resultSet: 
    path = Path(path)

    # get the title
    titleIDPos = metadata.index(b"title") + len("title")
    title = decodeTitle(metadata, titleIDPos)

    if title is None: continue

    print(f"Found '{title}', copying...")
    titleList.append(title)


    # alter the clip's title when necessary
    if (nRepeats := titleList.count(title)) > 1: # if the title is repeated
        title += f"-{nRepeats}"

    if len(str(clipsDir)) + len(title) + len(path.suffix) > MAX_PATH_LEN:
        charsLeft = MAX_PATH_LEN - (len(str(clipsDir)) + len(path.suffix))
        title = title[:charsLeft] 

        if not title:
            raise NotImplementedError("Path is too big to copy a file with a name to it")

    
    # copy clip to the target folder
    targetPath = clipsDir / (title + path.suffix)
    path.copy(targetPath) # still runs if the file exists, to prevent possible errors from medal's db data changing


print(f"\nFinished sorting through clips. Copied {len(titleList)} files")


'''
TODO:
- Make a JSON file with a list of the files that i have upon executing the script.
Compare it with the current JSON file to see which files have been removed, and
check for it's existance to make sure the folder was created.
- Add "instalation" and "usage" section to README (?)
- Warn about deleting or altering the JSON file, and explain how the script works
on README (summed up)
- Maybe save the clips to an album on Medal.
'''


