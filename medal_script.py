from pathlib import Path
import sqlite3 as sqlite

#import msgpack #the metadata table is encoded in MessagePack


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
result = db.execute("SELECT local_content_id, video_path, metadata FROM contents")

print("Connected to database and executed query.")

