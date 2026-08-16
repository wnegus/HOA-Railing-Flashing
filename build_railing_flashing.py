#!/usr/bin/env python3
"""
Regenerates the COLORS array in railing_flashing_vote.html from paired photos
in hoa_paint_options/, named like:

  option01_front_soft-warm-light-gray-railing_light-warm-greige-flashing.jpg
  option01_roof_soft-warm-light-gray-railing_light-warm-greige-flashing.jpg

i.e. optionNN_<front|roof>_<railing-color-desc>-railing_<flashing-color-desc>-flashing.jpg

Usage:
  1. Drop matching front/roof photo pairs into hoa_paint_options/ using that
     naming pattern (front and roof filenames must share the same option
     number and description).
  2. Run: python3 build_railing_flashing.py
  3. Commit + push railing_flashing_vote.html.
"""
import base64, os, re, json, subprocess, tempfile, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "hoa_paint_options")
HTML_PATH = os.path.join(ROOT, "railing_flashing_vote.html")
MAX_WIDTH = 900
JPEG_QUALITY = 70

FNAME_RE = re.compile(
    r"^(option\d+)_(front|roof)_(.+)-railing_(.+)-flashing\.jpe?g$", re.IGNORECASE
)

def titleize(desc):
    return re.sub(r"[_\-]+", " ", desc).strip().title()

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
    if not os.path.isdir(SRC_DIR):
        sys.exit(f"Missing {SRC_DIR}")

    options = {}  # option_id -> {"front": path, "roof": path, "railing": ..., "flashing": ...}
    for fname in sorted(os.listdir(SRC_DIR)):
        m = FNAME_RE.match(fname)
        if not m:
            if not fname.startswith("."):
                print("SKIP (doesn't match naming pattern):", fname)
            continue
        opt_id, view, railing_desc, flashing_desc = m.groups()
        entry = options.setdefault(opt_id, {})
        entry[view.lower()] = os.path.join(SRC_DIR, fname)
        entry["railing"] = titleize(railing_desc)
        entry["flashing"] = titleize(flashing_desc)

    entries = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for opt_id in sorted(options, key=lambda k: int(re.sub(r"\D", "", k))):
            data = options[opt_id]
            if "front" not in data or "roof" not in data:
                print(f"WARNING: {opt_id} missing front or roof photo, skipping")
                continue
            src_front = resize_and_encode(data["front"], tmpdir)
            src_deck = resize_and_encode(data["roof"], tmpdir)
            label = f"{data['railing']} Railing / {data['flashing']} Flashing"
            obj = "  {id:%s,label:%s,srcFront:%s,srcDeck:%s}" % (
                json.dumps(opt_id), json.dumps(label), json.dumps(src_front), json.dumps(src_deck)
            )
            entries.append(obj)

    if not entries:
        sys.exit("No complete front/roof pairs found.")

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
