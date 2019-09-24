library(nflscrapR)
library(dplyr)

# Use nflscrapR to get NFL game data

games_2017_reg <- scrape_game_ids(2017, type = "reg")
games_2017_post <- scrape_game_ids(2017, type = "post")
games_2018_reg <- scrape_game_ids(2018, type = "reg")
games_2018_post <- scrape_game_ids(2018, type = "post")
games_2019_reg <-scrape_game_ids(2019, type = "reg")
games_2017_2019 <- as.data.frame(do.call("rbind", list(games_2017_reg, 
                                                       games_2017_post, 
                                                       games_2018_reg,
                                                       games_2018_post,
                                                       games_2019_reg)))
games_2017_2019$week <- NULL

# Read in next-gen-scrapy data
pass_locations <- read.csv("pass_locations.csv")
pass_locations$game_id <- as.character(pass_locations$game_id)

# Combine nflscrapR and next-gen-scrapy data

pass_and_game_data <- full_join(pass_locations, games_2017_2019)
pass_and_game_data <- pass_and_game_data[which(pass_and_game_data$state_of_game != "PRE"),]
pass_and_game_data$state_of_game <- NULL
pass_and_game_data$x <- round(pass_and_game_data$x, 1)
pass_and_game_data$y <- round(pass_and_game_data$y, 1)
names(pass_and_game_data)[names(pass_and_game_data) == "x"] <- "x_coord"
names(pass_and_game_data)[names(pass_and_game_data) == "y"] <- "y_coord"
pass_and_game_data$X <- NULL
pass_and_game_data$team <- as.character(pass_and_game_data$team)
pass_and_game_data$home_team <- as.character(pass_and_game_data$home_team)
pass_and_game_data$away_team <- as.character(pass_and_game_data$away_team)

pass_and_game_data$team[pass_and_game_data$team == "arizona-cardinals"] <- "ARI"
pass_and_game_data$team[pass_and_game_data$team == "atlanta-falcons"] <- "ATL"
pass_and_game_data$team[pass_and_game_data$team == "baltimore-ravens"] <- "BAL"
pass_and_game_data$team[pass_and_game_data$team == "buffalo-bills"] <- "BUF"
pass_and_game_data$team[pass_and_game_data$team == "carolina-panthers"] <- "CAR"
pass_and_game_data$team[pass_and_game_data$team == "chicago-bears"] <- "CHI"
pass_and_game_data$team[pass_and_game_data$team == "cincinnati-bengals"] <- "CIN"
pass_and_game_data$team[pass_and_game_data$team == "cleveland-browns"] <- "CLE"
pass_and_game_data$team[pass_and_game_data$team == "dallas-cowboys"] <- "DAL"
pass_and_game_data$team[pass_and_game_data$team == "denver-broncos"] <- "DEN"
pass_and_game_data$team[pass_and_game_data$team == "detroit-lions"] <- "DET"
pass_and_game_data$team[pass_and_game_data$team == "green-bay-packers"] <- "GB"
pass_and_game_data$team[pass_and_game_data$team == "houston-texans"] <- "HOU"
pass_and_game_data$team[pass_and_game_data$team == "indianapolis-colts"] <- "IND"
pass_and_game_data$team[pass_and_game_data$team == "jacksonville-jaguars"] <- "JAX"
pass_and_game_data$team[pass_and_game_data$team == "kansas-city-chiefs"] <- "KC"
pass_and_game_data$team[pass_and_game_data$team == "los-angeles-chargers"] <- "LAC"
pass_and_game_data$team[pass_and_game_data$team == "los-angeles-rams"] <- "LA"
pass_and_game_data$team[pass_and_game_data$team == "miami-dolphins"] <- "MIA"
pass_and_game_data$team[pass_and_game_data$team == "minnesota-vikings"] <- "MIN"
pass_and_game_data$team[pass_and_game_data$team == "new-england-patriots"] <- "NE"
pass_and_game_data$team[pass_and_game_data$team == "new-orleans-saints"] <- "NO"
pass_and_game_data$team[pass_and_game_data$team == "new-york-giants"] <- "NYG"
pass_and_game_data$team[pass_and_game_data$team == "new-york-jets"] <- "NYJ"
pass_and_game_data$team[pass_and_game_data$team == "oakland-raiders"] <- "OAK"
pass_and_game_data$team[pass_and_game_data$team == "philadelphia-eagles"] <- "PHI"
pass_and_game_data$team[pass_and_game_data$team == "pittsburgh-steelers"] <- "PIT"
pass_and_game_data$team[pass_and_game_data$team == "san-francisco-49ers"] <- "SF"
pass_and_game_data$team[pass_and_game_data$team == "seattle-seahawks"] <- "SEA"
pass_and_game_data$team[pass_and_game_data$team == "tampabay-buccaneers"] <- "TB"
pass_and_game_data$team[pass_and_game_data$team == "tennessee-titans"] <- "TEN"
pass_and_game_data$team[pass_and_game_data$team == "washington-redskins" ] <- "WAS"
                                            
write.csv(pass_and_game_data, "./pass_and_game_data.csv")
