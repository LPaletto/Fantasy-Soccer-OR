# Best Fantasy Soccer team by Operative Research

This repository contains the data and the model to compute the best fantasy soccer team
for 2021/2022 Serie A league.

## Data

Data is divided in
1. players' grades for each day
2. players' prices 

All the data is stored in excel files.

All the players' grades have been taken from [Fantamagic site](https://www.fantamagic.it/fantacalcio/voti.php) .
Players' prices come from the fantasy soccer tournament I played last year. The auction has been made
starting with 500 credits. 
I'm open to hints on how to make the prices more 'statistical' and not linked to my tournament only.

## Model

The model is aimed to find the best team for the Serie A fantasy football. 

Brief description of the game. A certain number of users forms a league. Each user starts with a certain
number of coins, with whom he has to buy his team (3 keepers, 8 defenders, 8 midfielders and 6 strikers).
Players are bought through an auction, the user who wins the auction for a player gets the player in
his team. There is a second auction in winter where each user can sell a certain number of his players
and buy the same number of players from the ones that are not owned by other users. Each Serie A day
all the users line up a formation which they use against another random user of their league. Lined up
players' scores are summed and determine the points scored by the user. The number of goals scored by the
user is computed from the points scored. The goals are used to decide who wins as in a normal soccer match
(the match can end tie) and 0,1 or 3 fantapoints are gained by the users according to the result of their
match. At the end of the Serie A the user with the highest number of fantapoints wins the league.

You can find the model definition in the **model_definition.pdf** file. The model was implemented
with **pulp** library.

## Running the model

Run 

```
python main.py --help
```

to check what parameters you can modify, then run

```
python main.py
```

plus eventual parameters different from the default ones to run the model. 

## Accessing results

Results are overwritten and saved in the results folder. They include:
1. the best team for each round
2. each player best line up days for both rounds
3. the best combination of sold and bought players in the winter auction 
4. the points and goals scored by the user each day by lining up the best team in each day for both rounds
Bt default, the results folder contains the results for the default model configuration.





