# Weekly Shabbat times video (NC Graphics)

Setup (once per machine):
  pip install --break-system-packages zmanim pyluach numpy soundfile
  npm install            # fonts + puppeteer-core (needs /usr/bin/google-chrome)

Make this week's video:
  ./make.sh              # or ./make.sh 2026-12-03 for the Shabbat after that date
Output: Shabbat-YYYY-MM-DD.mp4 (1080x1920, 12s, with soft music)

Times: candle lighting 15 min before sunset in UK cities, 18 elsewhere abroad, 40 in Jerusalem;
motzei Shabbat = sun 8.5 degrees below horizon; R"T = 72 min after sunset.

## Weekly video (clip at the top, navy & gold luxury design: template3.html) — current style
  ./make2.sh path/to/clip.mov     # picks the best continuous 40s of the clip (with its sound)
  ./make2.sh -                    # no clip: candles / NC promo at the top + song.m4a
Table: 2 pages of 4 cities (UK+Antwerp, then NY/Lakewood/Montreal/Jerusalem), 12-hour times.
