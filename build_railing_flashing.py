#!/usr/bin/env python3
"""
Regenerates the COLORS array in railing_flashing_vote.html from paired photos.

Usage:
  1. Put the front-of-building renderings in photos/front/, and the matching
     roof-deck renderings in photos/deck/, using the SAME filename in both
     folders for a given color (e.g. photos/front/Charcoal.jpg and
     photos/deck/Charcoal.jpg are treated as one color option: "Charcoal").
  2. Run: python3 build_railing_flashing.py
  3. Commit + push railing_flashing_vote.html.

Labels are derived from the filename (underscores -> spaces, title-cased).
"""
import base64, os, re, json, subprocess, tempfile, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = os.path.join(ROOT, "photos", "front")
DECK_DIR = os.path.join(ROOT, "photos", "deck")
HTML_PATH = os.path.join(ROOT, "railing_flashing_vote.html")
MAX_WIDTH = 900
JPEG_QUALITY = 70

def label_for(stem):
    return re.sub(r"[_\-]+", " ", stem).strip().title()

def resize_and_encode(path, tmpdir):
    base = os.path.basename(path)
    out_path = os.path.join(tmpdir, base + ".jpg")
    subprocess.run(
        ["sips", "-Z", str(MAX_WIDTH), "-s", "format", "jpeg",
         "-s", "formatOptions", str(JPEG_QUALITY), path, "--out", out_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    with open(out_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return "data:image/jpeg;base64," + b64

def main():
    if not os.path.isdir(FRONT_DIR) or not os.path.isdir(DECK_DIR):
        sys.exit(f"Missing photos/front or photos/deck under {ROOT}")

    front_files = {os.path.splitext(f)[0]: f for f in os.listdir(FRONT_DIR) if not f.startswith(".")}
    deck_files = {os.path.splitext(f)[0]: f for f in os.listdir(DECK_DIR) if not f.startswith(".")}

    stems = sorted(set(front_files) & set(deck_files))
    missing_deck = sorted(set(front_files) - set(deck_files))
    missing_front = sorted(set(deck_files) - set(front_files))
    if missing_deck:
        print("WARNING: no deck match for:", missing_deck)
    if missing_front:
        print("WARNING: no front match for:", missing_front)
    if not stems:
        sys.exit("No matching front/deck filename pairs found.")

    entries = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for stem in stems:
            front_src = resize_and_encode(os.path.join(FRONT_DIR, front_files[stem]), tmpdir)
            deck_src = resize_and_encode(os.path.join(DECK_DIR, deck_files[stem]), tmpdir)
            label = label_for(stem)
            obj = "  {id:%s,label:%s,srcFront:%s,srcDeck:%s}" % (
                json.dumps(stem), json.dumps(label), json.dumps(front_src), json.dumps(deck_src)
            )
            entries.append(obj)

    colors_js = "const COLORS = [\n" + ",\n".join(entries) + "\n];"

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    start_marker = "const COLORS = ["
    end_marker = "\n];\n"
    start_idx = html.index(start_marker)
    end_idx = html.index(end_marker, start_idx) + len(end_marker)
    html = html[:start_idx] + colors_js + "\n" + html[end_idx:]

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {len(entries)} color options to {HTML_PATH}")
    print("New file size:", os.path.getsize(HTML_PATH))

if __name__ == "__main__":
    main()
