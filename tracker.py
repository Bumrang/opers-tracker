import requests
from bs4 import BeautifulSoup
import sqlite3

location = ['east_gym', 'pool', 'martial_arts_room', 'activities_room', 'dance_studio',
          'racquetball_courts', 'multi_purpose_room', 'wellness_1st_floor', 'wellness_2nd_floor']

def createArray (bslist):
    array = []
    for place in bslist:
        array.append([place.contents[0], place.next_sibling.contents[0], place.next_sibling.next_sibling.contents[0]])
    return array

def createTables(c):
    for loc in location:
        c.execute('CREATE TABLE IF NOT EXISTS {table} (id INT PRIMARY KEY, count INT NOT NULL, date TEXT NOT NULL, UNIQUE(date))'.format(table=loc))

def insertSql (c, places):
    for index, loc in enumerate(location):
        c.execute("INSERT INTO {table} (count, date) VALUES ({ct}, '{dt}')".format(table=loc, ct=places[index][1], dt=places[index][2]))

http_res = requests.get('https://docs.google.com/spreadsheets/u/1/d/1o1lQ6FFqr6RALPZ6I48cuWDd1clrPOlks8f3sWKx-9s/pubhtml?gid=217361177&single=true')

# parse for "s6" id which is the beginning of each data entry
bs = BeautifulSoup(http_res.content, 'html.parser')
places_raw = bs.find_all("td", {"class":"s6"})
places = createArray(places_raw)

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

createTables(c)
insertSql(c, places)

conn.commit()
conn.close()