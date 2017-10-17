import sqlite3
from datetime import datetime
import plotly
import plotly.graph_objs as go

location = ['east_gym', 'pool', 'martial_arts_room', 'activities_room', 'dance_studio',
          'racquetball_courts', 'multi_purpose_room', 'wellness_1st_floor', 'wellness_2nd_floor']

# formats all of the data from the sqlite db so it's friendly for plotting
def fetchData(c):
    places = {}
    for loc in location:
        c.execute('SELECT {col1},{col2} FROM {table}'.format(col1='count', col2='date', table=loc))
        rows = c.fetchall()
        # turns [(c0, d0), (c1, d1), ...] into [(c0, c1, ...), (d0, d1, ...)]
        counts, dates = zip(*rows)

        formatted_date = []
        for date in dates:
            f_date = datetime.strptime(date, '%A, %B %d,  at %I:%M: %p')
            formatted_date.append(f_date.replace(year=2017))

        places[loc] = [counts, formatted_date]
    return places

def generateGraphs():
    traces = []
    for loc in location:
        trace = go.Scatter(
            x=data[loc][1],
            y=data[loc][0],
            mode='lines+markers',
            name=loc,
            line=dict(
                shape='spline'
            )
        )
        traces.append(trace)

    # 9 plots, 3x3 grid
    page = plotly.tools.make_subplots(rows=3, cols=3)

    for index, trace in enumerate(traces):
        page.append_trace(trace, int(index / 3) + 1, (index % 3) + 1)

    page['layout'].update(height=1080, width=1920, title='OPERS usage over time')

    plotly.offline.plot(
        page,
        filename='graph.html'
    )

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

data = fetchData(c)

conn.commit()
conn.close()

generateGraphs()