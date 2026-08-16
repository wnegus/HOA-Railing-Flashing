Voting webpage to pick a railing & flashing paint color for the community.

Each color option is shown as a paired photo-realistic rendering: one view of
the front of the building, one of the roof deck. Voters rank up to 3 color
options; each option counts as a single choice regardless of it having two
photos.

## Adding/updating photos

Drop photo pairs into `hoa_paint_options/` (not tracked by git — the images
end up embedded as base64 in the HTML instead) named like:

```
optionNN_front_<railing-color-desc>-railing_<flashing-color-desc>-flashing.jpg
optionNN_roof_<railing-color-desc>-railing_<flashing-color-desc>-flashing.jpg
```

e.g. `option01_front_soft-warm-light-gray-railing_light-warm-greige-flashing.jpg`
and the matching `option01_roof_...jpg`. The `front`/`roof` pair sharing the
same `optionNN` and description is treated as one color option; the label
shown to voters is generated from the railing/flashing description text.

Then:

1. Run `python3 build_railing_flashing.py` — it resizes/compresses the
   images, base64-embeds them, and rewrites the `COLORS` array in
   `railing_flashing_vote.html`.
2. Commit and push. Netlify will redeploy automatically.
