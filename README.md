# Intro to `next-gen-scrapy`

## Summary

This is the first version released of `next-gen-scrapy`. This repo of was built to allow users to extract all pass locations -  completions, incompletions, interceptions, and touchdowns - from the regular season and postseason pass charts provided by Next Gen Stats beginning in 2017.

The pass charts are scraped from the NFL's official Next Gen Stats website, https://nextgenstats.nfl.com/charts/list/pass. After obtaining all of the pass chart images from the website, for every pass chart, the field is then undistorted, and all pass locations on the field relative to the line of scrimmage are extracted in (x,y) coordinate format. 

The file `pass_and_game_data.csv` is the final version of all pass location data for the 2017 and 2018 regular seasons and postseasons. After all Python and R scripts are run, for every available pass chart, the data contains Game ID, home team, away team, week, season, player, type of pass, and pass location from the line of scrimmage. This repo will be maintained regularly for bug fixes and new, exciting features and updates - including wide receiver route locations coming soon! Thank you to Sam Ventura, Kostas Pelechrinis, and Ron Yurko for all your help and guidance with this project!

### Example Undistorted Pass Chart (with axes in yards) - Nick Foles in Super Bowl LII

![Nick Foles in Super Bowl LII](https://raw.githubusercontent.com/sarahmallepalle/next-gen-scrapy/master/axes.jpg)

## Output Data

Column | Definition
---|---------
`game_id` | NFL GameID
`team` | Pass chart's team
`week` | Week of game
`name` | Pass chart's player first and last name 
`pass_type` | COMPLETE, INCOMPLETE, INTERCEPTION, or TOUCHDOWN
`x_coord` | x-coordinate of field location in yards; -26.66 <= x <= 26.66, with x = 0 as the vertical axis in the center of the field. 
`y_coord` | y-coordinate of field location in yards; -10 <= y <= 75, with y = 0 as the horizontal axis at the Line of Scrimmage
`type` | Regular ("reg") or postseason ("post") game
`home_team` | Home team of game
`away_team` | Away team of game
`season` | Year of game - 2017 or 2018 (...for now :) )

### Example Subset of Dataset - 10 Pass Locations of Nick Foles in Super Bowl LII

|    |   game_id  | team |    week    |    name    |   pass_type  | x_coord | y_coord | type | home_team | away_team | season |
|:--:|:----------:|:----:|:----------:|:----------:|:------------:|:-------:|:-------:|:----:|:---------:|:---------:|:------:|
| 1  | 2018020400 | PHI  | super-bowl | Nick Foles | COMPLETE     | -3.6    | 16.9    | post | NE        | PHI       | 2017   |
| 2  | 2018020400 | PHI  | super-bowl | Nick Foles | COMPLETE     | 16.2    | -3      | post | NE        | PHI       | 2017   |
| 3  | 2018020400 | PHI  | super-bowl | Nick Foles | COMPLETE     | 11.5    | -6.4    | post | NE        | PHI       | 2017   |
| 4  | 2018020400 | PHI  | super-bowl | Nick Foles | TOUCHDOWN    | -8.5    | 5.7     | post | NE        | PHI       | 2017   |
| 5  | 2018020400 | PHI  | super-bowl | Nick Foles | TOUCHDOWN    | -18.8   | 30.1    | post | NE        | PHI       | 2017   |
| 6  | 2018020400 | PHI  | super-bowl | Nick Foles | TOUCHDOWN    | -19.3   | 41.2    | post | NE        | PHI       | 2017   |
| 7  | 2018020400 | PHI  | super-bowl | Nick Foles | INTERCEPTION | 21.8    | 37.9    | post | NE        | PHI       | 2017   |
| 8  | 2018020400 | PHI  | super-bowl | Nick Foles | INCOMPLETE   | 5.1     | 7.9     | post | NE        | PHI       | 2017   |
| 9  | 2018020400 | PHI  | super-bowl | Nick Foles | INCOMPLETE   | -12.9   | 39.6    | post | NE        | PHI       | 2017   |
| 10 | 2018020400 | PHI  | super-bowl | Nick Foles | INCOMPLETE   | 26.1    | 8       | post | NE        | PHI       | 2017   |

## Installation

Requires Python 2.7 and R

Python 2.7:
```
pip install --upgrade pip
pip install requests bs4 lxml Pillow opencv-python scipy numpy pandas scikit-learn
```

R:
```
install.packages(c("devtools", "dplyr"))
devtools::install_github(repo = "ryurko/nflscrapR")
```

## Usage

From the command line:

```
python scrape.py 	# Scrape images and html data, store in folder Pass_Charts
```
```
python clean.py 	# Clean images and html data, store in folder Cleaned_Pass_Charts
```
```
python main.py 		# Extract pass information from images and data, output to pass_locations.csv
```
```
Rscript game_data_from_nflscrapR.R 	# Use nflscrapR to match pass information to game information, output to pass_and_game_data.csv
```

## Known issues as of this first version
- For a significant amount of pass charts on Next Gen Stats, the number of incomplete passes given in the HTML data, does not match the actual number of incomplete passes depicted in the Pass Charts. Example image here:  https://nextgenstats.nfl.com/charts/list/all/kansas-city-chiefs/2017/wild-card/alex-smith/SMI031126/2017/wild-card/pass (there are supposed to be 33-24=9 incompletes in the pass chart, but there are only 8 shown on the field.) For these rows representing incomplete pass locations not present in a pass chart, `pass_type` is equal to 'INCOMPLETE', and `x_coord` and `y_coord` are both NA.
- NA values for `x_coord` and `y_coord` if pass locations could not be extracted. 
- A row of NA values follwing a Game ID if no pass charts are provided for a game. As of the end of the 2018 regular season, there are 33 games without pass charts for either team.
