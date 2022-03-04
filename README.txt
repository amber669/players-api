----------------------------------------------------------
1. Overview
----------------------------------------------------------
This API for puzzle game players has the following features:
1. Create new players by typing a username. Each user has the following parameters: player_id, username, xp, and gold.
2. Update existing players information includes: username, xp, and gold
3. Generate leaderboard according to user inputs of xp/gold and the number of players to show.

Endpoints specification:
localhost:5000/api/v1/player/                 --> create new player
localhost:5000/api/player/<player_id>/        --> view existing player
localhost:5000/api/player/update/<player_id>/ --> update existing player
localhost:5000/api/leaderboards/              --> customize and see leaderboard

----------------------------------------------------------
2. Instructions to run the API code locally
----------------------------------------------------------
pip install -r requirements.txt
python app.py

If you have not installed python yet, please refer to this website to download python first and then you will be able to run the program.

Download Python:
https://www.python.org/downloads/

----------------------------------------------------------
2. Instructions to run the API code through docker Compose
----------------------------------------------------------
docker compose up
