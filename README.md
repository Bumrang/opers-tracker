# opers-tracker
Tracks how many people are using the UCSC OPERS facilities.

# Usage

Run tracker.py to fetch updates to the user count. Best to leave it on a cron job or something similar.

Run plotter.py to get a visualization of the data collected.

# Dependencies

For tracker.py:
- BeautifulSoup4
- SQLite3

For plotter.py:
- Plotly
- SQLite3
