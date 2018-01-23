import os
import eyed3

eyed3.log.setLevel("ERROR")

def mapGenre(genre):
    if genre:
        if any(x in genre.name.lower() for x in ["rock", "grunge", "indie", "new wave", "punk", "metal", "alternative", "leftfield", "garage", "new romantic"]):
            return "rock"
        if any(x in genre.name.lower() for x in ["rap", "hip-hop", "trip hop", "trip-hop", "hip hop"]):
            return "hip-hop"
        if any(x in genre.name.lower() for x in ["pop"]):
            return "pop"
        if any(x in genre.name.lower() for x in ["soul", "r b", "funk"]):
            return "soul"
        if any(x in genre.name.lower() for x in ["blues"]):
            return "blues"
        if any(x in genre.name.lower() for x in ["country"]):
            return "country"
        if any(x in genre.name.lower() for x in ["dance", "drum and bass", "electronic", "rave", "disco", "house"]):
            return "dance"
        if any(x in genre.name.lower() for x in ["vocal"]):
            return "vocal"
        if any(x in genre.name.lower() for x in ["folk"]):
            return "folk"
        if any(x in genre.name.lower() for x in ["reggae", "ska"]):
            return "reggae"
        if any(x in genre.name.lower() for x in ["jazz", "swing"]):
            return "jazz"
    return None

def main(force = False):
    unlabelled = {}
    for root, dirs, files in os.walk("./data/raw"):
        if '_' in root:
            continue
        for f in files:
            audiofile = eyed3.load(os.path.join(root, f))
            if not audiofile:
                continue
            if force or not audiofile.tag.comments.get("label"):
                genre = mapGenre(audiofile.tag.genre)
                if genre:
                    audiofile.tag.comments.set(genre, "label")
                    audiofile.tag.save()
                else:
                    if not audiofile.tag.genre:
                        genre = None
                    else:
                        genre = audiofile.tag.genre.name

                    print(genre)
                    if genre not in unlabelled:
                        unlabelled[genre] = 0
                    unlabelled[genre] += 1

    print("Unlabelled " + repr(unlabelled))

if __name__ == "__main__":
    main()
