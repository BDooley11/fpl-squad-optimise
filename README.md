This script uses a python implementation of the 'knapsack problem' to pick the best Fanstasy premier league team based on 3 different metrics.

1. Points last season (position changes factored in ie Rashford points converted from F to M).
2. Points last season (value per minute played > 1000mins).
3. Expected points (GW range is 1-8) gotten from site fplreview.com.

player_dataset.csv is generated using scripts in the 'database_scripts' directory. Process is outlined in the README in that directory.

both 'squad_optimiser.ipynb' and 'squad_optimiser.py' do the same thing. A description of the metrics that can be used in the squad optimiser are outlined in both files and a sample output can be seen below based on on the below criteria.

squad_optimise(
         metric=3,
         start_gw=1,
         end_gw=8,
         bench_value=None,
         bank=0.5,
         D=4,
         M=None,
         F=None,
         include_player=['Son','Werner'],
         exclude_player=[395],
         exclude_team_first=['Fulham','Brighton'],
         include_bench=['Ferguson'],
         exclude_bench=[],
         exclude_team_bench=['Brighton'])
         
<img width="560" alt="expected output" src="https://user-images.githubusercontent.com/55091575/91836787-2c64f800-ec43-11ea-9499-798ebc8db955.png">
