CREATE DATABASE HTML_Project;
USE HTML_project;
CREATE TABLE user_ratings(
BGGId INT(11) NOT NULL,
Rating VARCHAR(255) NOT NULL,
Username VARCHAR(255) NOT NULL);

CREATE TABLE games(
BGGId INT(11) PRIMARY KEY NOT NULL,
Name_ VARCHAR(255), Description_ VARCHAR(255), YearPublished VARCHAR(255),
GameWeight VARCHAR(255), AvgRating VARCHAR(255), BayesAvgRating VARCHAR(255),
StdDev VARCHAR(255), MinPlayers VARCHAR(255), MaxPlayers VARCHAR(255),
ComAgeRec VARCHAR(255), LanguageEase VARCHAR(255), BestPlayers VARCHAR(255),
GoodPlayers VARCHAR(255), NumOwned VARCHAR(255), NumWant VARCHAR(255),
NumWish VARCHAR(255), NumWeightVotes VARCHAR(255), MfgPlaytime VARCHAR(255),
ComMinPlaytime VARCHAR(255), ComMaxPlaytime VARCHAR(255), MfgAgeRec VARCHAR(255),
NumUserRatings VARCHAR(255), NumAlternates VARCHAR(255), NumExpansions VARCHAR(255),
NumImplementations VARCHAR(255), IsReimplementation VARCHAR(255), Family VARCHAR(255),
Kickstarted VARCHAR(255), ImagePath VARCHAR(255), Rank_boardgame VARCHAR(255), 
Category VARCHAR(255), Rank_Category VARCHAR(255));

CREATE TABLE themes(
BGGId INT(11) PRIMARY KEY NOT NULL,
themes VARCHAR(255));

CREATE TABLE mechanics(
BGGId INT(11) PRIMARY KEY NOT NULL,
mechanics VARCHAR(255));

CREATE TABLE subcategories(
BGGId INT(11) PRIMARY KEY NOT NULL,
subcategories VARCHAR(255));

CREATE TABLE artists_reduced(
BGGId INT(11) PRIMARY KEY NOT NULL,
artists_reduced VARCHAR(255));

CREATE TABLE designers_reduced(
BGGId INT(11) PRIMARY KEY NOT NULL,
designers_reduced VARCHAR(255));

CREATE TABLE publishers_reduced(
BGGId INT(11) PRIMARY KEY NOT NULL,
publishers_reduced VARCHAR(255));







