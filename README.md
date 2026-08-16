Voting webpage to pick a railing & flashing paint color for the community.

Each color option is shown as a paired photo-realistic rendering: one view of
the front of the building, one of the roof deck. Voters rank up to 3 color
options; each option counts as a single choice regardless of it having two
photos.

## Adding/updating photos

1. Drop the front-of-building rendering for a color into `photos/front/`,
   and the matching roof-deck rendering into `photos/deck/`, using the
   **same filename** in both folders (e.g. `photos/front/Charcoal.jpg` and
   `photos/deck/Charcoal.jpg`).
2. Run `python3 build_railing_flashing.py` — it resizes/compresses the
   images, base64-embeds them, and rewrites the `COLORS` array in
   `railing_flashing_vote.html`.
3. Commit and push. Netlify will redeploy automatically.
