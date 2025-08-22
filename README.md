# Match_mate_API
This API is for football match predictions

# APPS
I created two apps:

1. accounts for user registeration
2. match to set up fixtures and games
3. Predictions to allow for match predictions

# Models
Made models for each app. 
For accounts, I made a serializer with inbuilt django User. 
Also included a leaderboard model for 

Match models include: League, Team, and Fixtures where the games will be listed out 

Prediction models include: Predictions.

# Changed the prediction models plan. 
Added a prediction app and moved the prediction models into it. 

# Changed the structure of account model
I removed leaderboard model and created a leaderboard serializer to display the leaderboard according to the UserStats

# Auto update Userstats and leaderboard
from my predictions model in predictions up I created a method to auto update the UserStats for everytime there is a result. 
Aided this functionality with signal.py a nd _init_.py in the predictions app. 
