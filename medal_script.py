import sqlite3 as sqlite
from pathlib import Path


unnamedCount = namedCount = 0
medalPath = Path(Path().home(), "AppData", "Roaming", "Medal") 

for path in medalPath.iterdir():
    if path.suffix == ".db":
        nIndex = len("medal-") #yields the index that's right after the hyphen
        
        if path.stem[nIndex].isnumeric(): #ignores medal-guest.db and CustomGameDatabase.db
            dbPath = medalPath / path.name
            print(f"Path to database: {dbPath}")
            
            break


#connect to sqlite database and get the video id, it's path and it's metadata
db = sqlite.connect(dbPath) 
resultSet = db.execute("SELECT local_content_id, video_path, metadata FROM contents")

print("Connected to database and executed query.")


for id, path, metadata in resultSet: 
    #define bounds where the title for the video is in
    lowerBound = metadata.index(b"title") + len("title") #byte that's after the title key

    '''
    The hex code that appears when "clipDuration" is used as a clip name 
    is "\xc7\x0c". it will be repeated twice, if that is the case, since
    there is also a key that's named "clipDuration", but i cannot allow
    it since i use that key for my upper bound.
    '''

    if metadata.count(b"\xc7\x0cclipDuration") > 1: #
        raise NotImplementedError("Do not name your clips 'clipDuration'. Alternatively, open an issue on github and i'll adress it.")

    upperBound = metadata.index(b"\xc7\x0cclipDuration")
    titleSection = metadata[lowerBound : upperBound]

    '''
    The hex code that appears inbetween the title and clipDuration keys
    when a clip does not have a name is "\x07".
    '''

    if titleSection == b"\x07":
        unnamedCount += 1
        continue
    else: 
        namedCount += 1
    
    #print(titleSection)


'''
TODO:
- Maybe save the clips to an album on Medal. If i cant do that, copy them to a folder.
- Look at the MessagePack specification for the part behind the title. Its the same.
'''


