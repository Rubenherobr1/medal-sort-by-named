# Sort by Named Clips in [Medal](https://medal.tv/)

Do you usually give a memorable name to Medal clips that are amazing, and don't name the other
clips that you have? Have you ever wanted to see only the clips that you gave a name to?

This python script does exactly that: it only gets the clips that are named, and saves it to 
somewhere **(TBD)**, since Medal dosen't give that filter option, and the video files for the 
clips aren't renamed to what name you give them inside Medal. 

**Note**: This is NOT an official script from Medal.

## What versions are supported

This script was developed for the following versions:
- **Latest Stable:** 2629.329.1
- **Recorder version:** 2629.2224.1

To check your version, go to **Settings** and **scroll down**. It should be at the bottom.

The script may or may not work in future or past versions. If you think it does not work in your version,
feel free to open a PR or an issue so i can see what i can do!

## Why i dont use the available [MessagePack](https://msgpack.org/) libraries in my code

I initially tried using the available libraries which still seem to be updated (at the point of
writing this), notably [ormsgpack](https://github.com/ormsgpack/ormsgpack) and 
[msgpack](https://github.com/msgpack/msgpack-python/), but they never worked for one reason or 
another. 

I then asked some LLM's to decode the metadata just to see what they would say, and they 
said that the MessagePack encoding that was used was heavily altered.

Basicly, there's no way i was going to decode it using the normal libraries available. So i 
had to do it myself.


