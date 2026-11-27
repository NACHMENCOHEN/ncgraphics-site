# Weekly Shabbat times video (NC Graphics)

Setup (once per machine):
  pip install --break-system-packages zmanim pyluach numpy soundfile
  npm install            # fonts + puppeteer-core (needs /usr/bin/google-chrome)

Make this week's video:
  ./make.sh              # or ./make.sh 2026-12-03 for the Shabbat after that date
Output: Shabbat-YYYY-MM-DD.mp4 (1080x1920, 12s, with soft music)

Times: candle lighting 15 min before sunset in UK cities, 18 elsewhere abroad, 40 in Jerusalem;
motzei Shabbat = sun 8.5 degrees below horizon; R"T = 72 min after sunset.
