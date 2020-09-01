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
         
     ID       Player Name Position       Team Name  Value  expected_minutes  expected_points
1   383            Lloris       GK           Spurs    5.5             697.0           32.001
2   259  Alexander-Arnold      DEF       Liverpool    7.5             649.0           36.219
3   255         Robertson      DEF       Liverpool    7.0             629.0           33.801
4   123             James      DEF         Chelsea    5.0             549.0           28.790
5   471           Vinagre      DEF          Wolves    4.5             501.0           24.301
6   254             Salah      MID       Liverpool   12.0             580.0           45.328
7   390               Son      MID           Spurs    9.0             539.0           33.512
8   365           Redmond      MID     Southampton    6.5             626.0           27.821
9   388              Kane      FWD           Spurs   10.5             634.0           39.237
10  117            Werner      FWD         Chelsea    9.5             562.0           37.913
11  202           Bamford      FWD           Leeds    5.5             595.0           27.120
12   35            Nyland       GK     Aston Villa    4.0             170.0            6.680
13  145          Ferguson      DEF  Crystal Palace    4.0               0.0            0.000
14  131          McCarthy      MID  Crystal Palace    4.5             518.0           16.296
15  191          Anguissa      MID          Fulham    4.5             385.0           12.698

Squad value:  99.5 (First Team: 82.5 , Bench: 17.0 )
Bank:  0.5
First Team points:  366.043 ( Bench: 35.674 )
