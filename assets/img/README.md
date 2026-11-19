# Image slots

Every image on the site points at a named slot in this folder. Today each slot is a labeled SVG placeholder.

To swap in a real photo:
1. Save the photo here with the slot name, e.g. `hero.jpg` (landscape, at least 2400 px wide for the hero; 1600 px for others). Compress it (aim for under 300 KB).
2. In `tools/build.py`, change the slot's entry in `IMG` from `hero.svg` to `hero.jpg` (and set a real `alt` text).
3. Run `python3 tools/build.py`, then commit.

| Slot | Used on | Suggested shot |
|---|---|---|
| hero.jpg | Home hero (full-bleed) | Aircraft on the KOLS ramp at golden hour, mountains behind |
| fbo.jpg | Home, Fuel & FBO | FBO building / lobby / ramp |
| fuel.jpg | Home, Fuel & FBO | Fuel truck or fueling an aircraft |
| cargo.jpg | Home, Services | Truck or freight being loaded |
| training.jpg | Flight Training | Trainer aircraft (only once the school is approved) |
| charter.jpg | Charter | Charter aircraft (only once approved) |
| about.jpg | About | Team photo or hangar |
| kols-guide.jpg | Blog: KOLS pilot guide | Runway 4/22 from the air |
| event.jpg | Blog: Wings & Wheels | Event crowd / aircraft display |
| logo.svg | Header, footer | Final CMA logo (SVG preferred; PNG works too) |
| favicon.svg | Browser tab | Square mark from the final logo |
| og-image.png | Social link previews | 1200×630 branded card |
