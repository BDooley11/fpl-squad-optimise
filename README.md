This script uses a python implementation of the 'knapsack problem' to pick the best Fanstasy Premier League team based on 3 different metrics.

1. Points last season (position changes factored in ie Rashford points converted from FWD to MID).
2. Points last season (value per minute played > 1000mins).
3. Expected points (GW range is 1-8) gotten from site fplreview.com.

player_dataset.csv is generated using scripts in the 'database_scripts' directory. Process is outlined in the README in that directory.

Both 'squad_optimiser.ipynb' and 'squad_optimiser.py' do the same thing. 
A description of the parameters that can be used in the squad optimiser are outlined in both files and a sample output can be seen below.

<img width="334" alt="squad optimise" src="https://user-images.githubusercontent.com/55091575/91836947-6635fe80-ec43-11ea-832d-04c367dd2451.png">
         
<img width="560" alt="expected output" src="https://user-images.githubusercontent.com/55091575/91836787-2c64f800-ec43-11ea-9499-798ebc8db955.png">
