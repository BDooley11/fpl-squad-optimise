1. 'FPL_Database.csv' is gotten using scrips in FPL-Season-Review Repo. (Note this script will not work now as FPL API's reset every season so no way of accessing historic information if not saved before then)
2. Run 'FPL_player_info.py' which generates a csv 'players.csv' of all the players in the current years gamed.
3. To get expected points for each player download a csv from 'fplreview.com'. 
	-Select Team Planner -> Massive Data -> GW projection selcted max and put in your team id and submit.
	-Scroll down and there will be option to download csv 'fplreview.csv'. 
	- Save this csv in same folder as 'player_dataset_generator.ipynb' notebook.
Alternatively run 'fplreview_selenium.py' which will download the spreadsheet from fplreview.com.
4. Open 'player_dataset_generator.ipynb' and follow instruction in this notebook. The final result of which will be a csv called 'player_dataset.csv' which can be cut into the main folder and will be the csv which the model will use to make its selections.