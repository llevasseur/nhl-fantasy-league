# World Junior Fantasy Draft
Casual Python3 project used by friends to keep track of World Junior hockey players' stats. Statistics of players drafted by participants are totaled to determine Scoreboard ranking and to determine the winner.
## Scoreboard
| User | [G](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals) | [A](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#assists) | [SOG](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#shots-on-goal) | [PIM](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#penalties-in-minutes) | [+/-](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#plus--minus) | [TPM](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#time-played-in-minutes) | [S%](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#save-percentage) | [GAA](https://github.com/llevasseur/world-juniors-2022/blob/master/STANDINGS.md#goals-against-average) | Total |
| :--- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |  -----: |
| [John](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#John) | 5 | 4 | 5 | 2 | 5 | 2 | 2 | 2 | 27 |
| [Alasdair](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Alasdair) | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 25 |
| [Leevon](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Leevon) | 3 | 5 | 4 | 1 | 5 | 5 | 1 | 1 | 25 |
| [Liam](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Liam) | 2 | 2 | 2 | 4 | 2 | 4 | 4 | 4 | 24 |
| [Timo](https://github.com/llevasseur/world-juniors-2022/blob/master/ROSTERS.md#Timo) | 1 | 1 | 1 | 5 | 1 | 1 | 5 | 5 | 20 |
## Installation
Fork this repository to contribute. Commits will be analyzed before being added to the source code.
## Usage
Participants can use this github to view stats, including the Scoreboard, Selected Roosters, and Standings in each category.

To update scores:
1. Run the python script `python ./src/fetch-player-data.py`
2. Write manual player data to `python ./src/write-manual-data.py`. Input ex: Firstname1 Lastname1,SOG,MM,SS, ...
3. Run `python ./src/merge-data.py`
4. Run `python ./src/data-to-md.py`
5. Run `python ./src/parse-standings.py`
6. Add, commit, and push changes to this github repository.
## Design Decisions
Functional Requirements:
1. Request a response from each [eliteprospect.com](https://www.eliteprospects.com/league/wjc-20/stats/2021-2022?page=1) webpage with player statistics (page=[1,4]).
<kbd>>![elite prospects webpage example](/public/images/http_source.jpg)</kbd>
Extract the html from the response and pull out data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) Save as a `json` database.
2. Some information is not provided on eliteprospect.com, including Shots on Goal and Time Played in Minutes. This information can be found on [iihf.com](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can) game statistics summaries.
<kbd>>![iihf stats summary webpage example](/public/images/additional_source.jpg)</kbd>
A web scraper has not been constructed for this website yet so player data is added manually to a separate `json` file. `write-manual-data.py` is a CLI API to do this easily, taking Firstname1 Lastname1,SOG,MM,SS, ... , as input. Save player data to a JSON object by querying data cells in table rows within the inner wrapper.
3. Merge the fetched player database and the manual player database using the player_name as the primary key.
4. Display the data in 3 locations:
a. ROSTERS.md: A visualizer for each participants drafted players' statistics.
b. STANDINGS.md: A visualizer for each participants overall totals versus each other. This determines rank.
c. README.md/Scoreboard: To make the scoreboard readily available for participants when they view this github repo, the Scoreboard is attached to this README. It is a visualizer for participant points based on rank for each category (Goals, Assists, etc). Participant points determine who's winning, or who wins, and is based off the number of players.
## Contributing
Bug reports are welcome on Github at [Issues](https://github.com/llevasseur/world-juniors-2022/issues).
## License
This project is available as open source under the terms of the [MIT License](https://opensource.org/licenses/MIT).
## Future Work
Anticipated additions to this project include:
1. Automating write-manual-data.py to pull from a web scrapped website passed in. Game-specific data, including Shots on Goal (SOG) and Time Played in Minutes (TPM) can be parsed from player data. Example, [here](https://www.iihf.com/en/events/2022/wm20/gamecenter/statistics/37416/5-lat-vs-can).
2. Displaying data using [Matplotlib](https://matplotlib.org/).
3. Increasing scale of project to work for more leagues, like the [NHL](https://www.eliteprospects.com/league/nhl).
4. Handling automated input for names with unfamiliar unicode, like `Topi Niemel�`.