library(nflscrapR)
library(dplyr)

# Use nflscrapR to get NFL game data

games_2017_reg <- scrape_game_ids(2017, type = "reg")
games_2017_post <- scrape_game_ids(2017, type = "post")
games_2018_reg <- scrape_game_ids(2018, type = "reg")
games_2018_post <- scrape_game_ids(2018, type = "post")
games_2019_reg <-scrape_game_ids(2019, type = "reg")
games_2019_post <-scrape_game_ids(2019, type = "post")
games_2017_2019 <- as.data.frame(do.call("rbind", list(games_2017_reg, 
                                                       games_2017_post, 
                                                       games_2018_reg,
                                                       games_2018_post,
                                                       games_2019_reg,
                                                       games_2019_post)))
games_2017_2019$week <- NULL

# Read in next-gen-scrapy data
route_locations <- read.csv("C:\\Users\\Ethan Douglas\\Documents\\Side Projects\\arrowhead_analytics\\next-gen-scrapy-master\\route_locations_2019.csv")
route_locations$game_id <- as.character(route_locations$game_id)

# Combine nflscrapR and next-gen-scrapy data

route_and_game_data <- full_join(route_locations, games_2017_2019)
route_and_game_data <- route_and_game_data[which(route_and_game_data$state_of_game != "PRE"),]
route_and_game_data$state_of_game <- NULL
route_and_game_data$x <- round(route_and_game_data$x, 1)
route_and_game_data$y <- round(route_and_game_data$y, 1)
names(route_and_game_data)[names(route_and_game_data) == "x"] <- "x_coord"
names(route_and_game_data)[names(route_and_game_data) == "y"] <- "y_coord"
route_and_game_data$X <- NULL
route_and_game_data$team <- as.character(route_and_game_data$team)
route_and_game_data$home_team <- as.character(route_and_game_data$home_team)
route_and_game_data$away_team <- as.character(route_and_game_data$away_team)

route_and_game_data$team[route_and_game_data$team == "arizona-cardinals"] <- "ARI"
route_and_game_data$team[route_and_game_data$team == "atlanta-falcons"] <- "ATL"
route_and_game_data$team[route_and_game_data$team == "baltimore-ravens"] <- "BAL"
route_and_game_data$team[route_and_game_data$team == "buffalo-bills"] <- "BUF"
route_and_game_data$team[route_and_game_data$team == "carolina-panthers"] <- "CAR"
route_and_game_data$team[route_and_game_data$team == "chicago-bears"] <- "CHI"
route_and_game_data$team[route_and_game_data$team == "cincinnati-bengals"] <- "CIN"
route_and_game_data$team[route_and_game_data$team == "cleveland-browns"] <- "CLE"
route_and_game_data$team[route_and_game_data$team == "dallas-cowboys"] <- "DAL"
route_and_game_data$team[route_and_game_data$team == "denver-broncos"] <- "DEN"
route_and_game_data$team[route_and_game_data$team == "detroit-lions"] <- "DET"
route_and_game_data$team[route_and_game_data$team == "green-bay-packers"] <- "GB"
route_and_game_data$team[route_and_game_data$team == "houston-texans"] <- "HOU"
route_and_game_data$team[route_and_game_data$team == "indianapolis-colts"] <- "IND"
route_and_game_data$team[route_and_game_data$team == "jacksonville-jaguars"] <- "JAX"
route_and_game_data$team[route_and_game_data$team == "kansas-city-chiefs"] <- "KC"
route_and_game_data$team[route_and_game_data$team == "los-angeles-chargers"] <- "LAC"
route_and_game_data$team[route_and_game_data$team == "los-angeles-rams"] <- "LA"
route_and_game_data$team[route_and_game_data$team == "miami-dolphins"] <- "MIA"
route_and_game_data$team[route_and_game_data$team == "minnesota-vikings"] <- "MIN"
route_and_game_data$team[route_and_game_data$team == "new-england-patriots"] <- "NE"
route_and_game_data$team[route_and_game_data$team == "new-orleans-saints"] <- "NO"
route_and_game_data$team[route_and_game_data$team == "new-york-giants"] <- "NYG"
route_and_game_data$team[route_and_game_data$team == "new-york-jets"] <- "NYJ"
route_and_game_data$team[route_and_game_data$team == "oakland-raiders"] <- "OAK"
route_and_game_data$team[route_and_game_data$team == "philadelphia-eagles"] <- "PHI"
route_and_game_data$team[route_and_game_data$team == "pittsburgh-steelers"] <- "PIT"
route_and_game_data$team[route_and_game_data$team == "san-francisco-49ers"] <- "SF"
route_and_game_data$team[route_and_game_data$team == "seattle-seahawks"] <- "SEA"
route_and_game_data$team[route_and_game_data$team == "tampabay-buccaneers"] <- "TB"
route_and_game_data$team[route_and_game_data$team == "tennessee-titans"] <- "TEN"
route_and_game_data$team[route_and_game_data$team == "washington-redskins" ] <- "WAS"

write.csv(route_and_game_data, "C:\\Users\\Ethan Douglas\\Documents\\Side Projects\\arrowhead_analytics\\next-gen-scrapy-master\\route_and_game_data.csv")
