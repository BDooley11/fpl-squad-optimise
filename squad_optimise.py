#Explanation of parameters and how to run the model below


# https://python-mip.readthedocs.io/en/latest/examples.html

from mip import Model, xsum, maximize, BINARY
import pandas as pd

# paramaters are explained in markdown below
def squad_optimise(metric=None, start_gw=None, end_gw=None, bench_value=None, bank=0, D=None, M=None, F=None , include_player=[], exclude_player=[], exclude_team_first=[], include_bench=[], exclude_bench=[], exclude_team_bench=[]):
        
    #error check metric 3 need start_gw and end_gw selected too.
    if metric ==3 and (start_gw==None or end_gw==None):
        return "Error, if metric 3 selected start_gw and end_gw range must be selected"
    
    #error check GW range
    if metric ==3 and (start_gw <1 or start_gw >8 or end_gw <1 or end_gw >8 or start_gw > end_gw) :
        return "Error, GW range is 1-8 and end_gw must be >= start_gw"
   
    #error check position paratemeters passed do not fall below minimum
        if (D !=None and D < 3) or (M !=None and M < 2) or (F !=None and F <1):
            return "Error, minimum D=3, M=2 and F-1"
        
    #quality checks for bench_value versus number of defenders    
    if bench_value == None and D==None:
        bench_value = 17.5
    elif bench_value == None:
        if D == 3:
            bench_value = 16.5
        elif D == 4 or D == 5:
            bench_value = 17 
    elif D==None:
        if bench_value < 17:
            D = 3
        elif bench_value == 17:
            D = 4
    elif bench_value < 17 and D > 3:
        return "Error, D value must equal 3 if bench value < 17"
    elif bench_value == 17 and D > 4:
        return "Error, D value must be 3 or 4 if bench value equals 17"
   
    df = pd.read_csv('player_dataset.csv')
    I = range(len(df))
    
    # this section deals with the different possible metrics
    if metric==None:
        return "Error, metric must be value 1,2 or 3"
    elif metric == 1:
        p = df['total_points']
    elif metric == 2:
        p = df['points_per_minute']
    elif metric == 3:
        #this deals expected points GW range
        df['expected_minutes'], df['expected_points'] = [0,0]
        for x in range(start_gw,end_gw+1):
            df['expected_points'] = df['expected_points'] + df[str(x)+'_Pts']
            df['expected_minutes'] = df['expected_minutes'] + df[str(x)+'_xMins']
        p = df['expected_points']
    
    w = df['Value']
    
    m = Model("first_team")

    x = [m.add_var(var_type=BINARY) for i in I]

    m.objective = maximize(xsum(p[i] * x[i] for i in I))

    m += xsum(w[i] * x[i] for i in I) <= (100 - bench_value - bank)
    
    #max number of players selected is 11.
    m += xsum(x[i] for i in I) == 11
    
    #GK constraint
    m += xsum(x[i] for i in I if df['Position'][i] == "GK") == 1
    
    #DEF constraint
    if D != None and D >= 3 and D <= 5:
        m += xsum(x[i] for i in I if df['Position'][i] == "DEF") == D
    elif D != None and (D <= 3 or D >= 5):
        return "Error, number of Defenders must be between 3 and 5"
    else:
        m += xsum(x[i] for i in I if df['Position'][i] == "DEF") >= 3
        m += xsum(x[i] for i in I if df['Position'][i] == "DEF") <= 5
    
    #MID constraint
    if M != None and M >= 2 and M <= 5:
        m += xsum(x[i] for i in I if df['Position'][i] == "MID") == M
    elif M != None and (M <= 2 or M >= 5):
        return "Error, number of Midfielders must be between 2 and 5"
    else:
        m += xsum(x[i] for i in I if df['Position'][i] == "MID") >= 2
        m += xsum(x[i] for i in I if df['Position'][i] == "MID") <= 5
    
    #FWD constraint
    if F != None and F >= 1 and F <= 3:
        m += xsum(x[i] for i in I if df['Position'][i] == "FWD") == F
    elif F != None and (F <= 1 or F >= 3):
        return "Error, number of Forwards must be between 1 and 3"
    else:
        m += xsum(x[i] for i in I if df['Position'][i] == "FWD") >= 1
        m += xsum(x[i] for i in I if df['Position'][i] == "FWD") <= 3
    
    # max number of players per team and also exclude excluded teams.
    excludedTeams = [team.lower() for team in exclude_team_first]
    for team in df['Team Name'].unique():
        if team.lower() in excludedTeams:
            m += xsum(x[i] for i in I if df['Team Name'][i] == team) == 0
        else:
            m += xsum(x[i] for i in I if df['Team Name'][i] == team) <= 3
       
    # if players selcted to be included or excluded dealt with here.
    # option for either ID or name as some players have same name ie Fernandes Man Utd and Spurs.
    for player in include_player:
        if isinstance(player, str):
            m += xsum(x[i] for i in I if df['Player Name'][i] == player) == 1
        elif isinstance(player, int):
            m += xsum(x[i] for i in I if df['ID'][i] == player) == 1

    for player in exclude_player:
        if isinstance(player, str):
            m += xsum(x[i] for i in I if df['Player Name'][i] == player) == 0
        elif isinstance(player, int):
            m += xsum(x[i] for i in I if df['ID'][i] == player) == 0 
            
    for player in include_bench:
        if isinstance(player, str):
            m += xsum(x[i] for i in I if df['Player Name'][i] == player) == 0
        elif isinstance(player, int):
            m += xsum(x[i] for i in I if df['ID'][i] == player) == 0 
           
    m.optimize()
    
    # put results of optimise ie if x ==1 into new df.
    first_team = df.iloc[[i for i in I if x[i].x == 1]].copy()
    if first_team.empty:
        print()
        print("Team calculation not possible due to parameters selected. Please edit and try again")
        print("""
        Possible reasons are:
        1. Included player but exluded team they play for.
        2. Included more players than max allowed. Ie 5 defenders and you include 6.  
        3. Both included and excluded a player.
        4. Combination of selected number of D, M and F cannot equal 10 outfield players.
        """)
    else:   
        # count number of def/mid/fwd in first team to make sure right number of bench players selected.
        defCount = 0
        midCount = 0
        fwdCount = 0

        if D != None:
            defCount = D
        else:
            defCount = (first_team['Position'] == 'DEF').sum()

        if M != None:
            midCount = M
        else:
            midCount = (first_team['Position'] == 'MID').sum()

        if F != None:
            fwdCount = F
        else:
            fwdCount = (first_team['Position'] == 'FWD').sum()

    # bench calculation
        m = Model("bench")

        x = [m.add_var(var_type=BINARY) for i in I]

        m.objective = maximize(xsum(p[i] * x[i] for i in I))

        m += xsum(w[i] * x[i] for i in I) <= bench_value

        #max number of players selected is 4.
        m += xsum(x[i] for i in I) == 4

        #GK constraint
        m += xsum(x[i] for i in I if df['Position'][i] == "GK") == 1

        #DEF constraint
        m += xsum(x[i] for i in I if df['Position'][i] == "DEF") == 5 - defCount

        #MID constraint
        m += xsum(x[i] for i in I if df['Position'][i] == "MID") == 5 - midCount

        #FWD constraint
        m += xsum(x[i] for i in I if df['Position'][i] == "FWD") == 3 - fwdCount

        #Make sure not already in first team constraint
        m += xsum(x[i] for i in I if df['ID'][i] in first_team['ID'].tolist()) == 0

        # max number of players per team and also exclude excluded teams.
        excludedTeams = [team.lower() for team in exclude_team_bench]
        for team in df['Team Name'].unique():
            if team.lower() in excludedTeams:
                m += xsum(x[i] for i in I if df['Team Name'][i] == team) == 0
            elif team in first_team['Team Name'].values:
                m += xsum(x[i] for i in I if df['Team Name'][i] == team) <= 3 - (first_team['Team Name'] == team).sum() 
            else:
                m += xsum(x[i] for i in I if df['Team Name'][i] == team) <= 3

        for player in include_bench:
            if isinstance(player, str):
                m += xsum(x[i] for i in I if df['Player Name'][i] == player) == 1
            elif isinstance(player, int):
                m += xsum(x[i] for i in I if df['ID'][i] == player) == 1
                
        for player in exclude_bench:
            if isinstance(player, str):
                m += xsum(x[i] for i in I if df['Player Name'][i] == player) == 0
            elif isinstance(player, int):
                m += xsum(x[i] for i in I if df['ID'][i] == player) == 0

        m.optimize()

        # put results of optimise ie if x ==1 into new df.
        bench = df.iloc[[i for i in I if x[i].x == 1]].copy()
        
        if bench.empty:
            print()
            print('Bench calculation not possible due to parameters selected. Please edit and try again')
            print("""
    Possible reasons are:
    1. Included player but already maxed position incl defender but already 5 defs in first team.
    2. Bench player included too expensive so cannot complete bench.    
    3. Bench value selected too low, min is 16.5 with D=3 or 17 with D=4.
            """)
        
        else:
            # sort by categories and points, not alphabetical so need to do ["GK", "DEF", "MID", "FWD"]
            first_team['Position'] = pd.Categorical(first_team['Position'], categories=["GK", "DEF", "MID", "FWD"])
            first_team = first_team.sort_values(by=["Position", "total_points"], ascending=[True, False])
            bench['Position'] = pd.Categorical(bench['Position'], categories=["GK", "DEF", "MID", "FWD"])
            bench = bench.sort_values(by=["Position", "total_points"], ascending=[True, False])
            
            # join first team and bench df.
            df_squad = first_team.append(bench)
            df_squad = df_squad.reset_index(drop=True)
            df_squad.index += 1

            #print slightly different display based on metric selected
            if metric ==1 or metric ==2:
                print(df_squad[['ID', 'Player Name', 'Position','Team Name','Value','minutes','total_points']].to_string())
                print()
                print ('Squad value: ',df_squad['Value'].sum(),'(First Team:',first_team['Value'].sum(),', Bench:',bench['Value'].sum(),')')
                # put 100 - First team value - bench value as might be banked money if due to parameters could not get exact squad value
                print ('Bank: ',100 - first_team['Value'].sum() - bench['Value'].sum())
                print ('First Team points: ',first_team['total_points'].sum(),'( Bench:',bench['total_points'].sum(),')')
            else:
                print(df_squad[['ID', 'Player Name', 'Position','Team Name','Value','expected_minutes','expected_points']].to_string())
                print()
                print ('Squad value: ',df_squad['Value'].sum(),'(First Team:',first_team['Value'].sum(),', Bench:',bench['Value'].sum(),')')
                print ('Bank: ',100 - first_team['Value'].sum() - bench['Value'].sum())
                print ('First Team points: ',round(first_team['expected_points'].sum(),3),'( Bench:',round(bench['expected_points'].sum(),3),')')

"""
**Metrics: different metrics to select best team on**
1. Points last season (position changes factored in ie Rashford points converted from F to M).
2. Points last season (value per minute played > 1000mins).
3. Expected points (GW range is 1-8) gotten from site fplreview.com.

**start_gw and end_gw: range of game weeks to calculate expected points**
* only required for metric 3 and range is from 1-8.

**bench_value: value of subs bench, the lowest is 16.5**
* Bench value 16.5; D must = 3.
* Bench value 17; D must = 4.
* If left blank default bench value is 17.5.

**bank: value you want to keep aside and not spend on squad**

**D,M,F: number of defenders, midfielders and forwards you want in your first team**
* note FPL limits - D:min-3,max-5 , M:min-2,max-5 , F:min-1,max-3

**include_player: is a player you want included in your first team**
* Note player name or ID can be used here as some players have the same name ie Henderson Liverpool and Man Utd.
* ID can be gotten from 'player_dataset.csv'.
* String must be entered in quotes ie 'Kane' valid but Kane is not.
* Can have multiple entries separated by , .

**exclude_player: is a player you do not want included in your first team**
* Note player name or ID can be used here as some players have the same name ie Henderson Liverpool and Man Utd.
* ID can be gotten from 'player_dataset.csv'.
* String must be entered in quotes ie 'Kane' valid but Kane is not.
* Can have multiple entries separated by , .

**exclude_team_first: you want no players from this team in your first team**
* String must be entered in quotes ie 'Spurs' valid but Spurs is not.
* Can have multiple entries separated by , .

**include_bench: is a player you want included on your bench**
* Note player name or ID can be used here as some players have the same name ie Henderson Liverpool and Man Utd.
* ID can be gotten from 'player_dataset.csv'.
* String must be entered in quotes ie 'Soucek' valid but Soucek is not.
* Can have multiple entries separated by , .

**exclude_bench: is a player you do not want included on your bench**
* Note player name or ID can be used here as some players have the same name ie Henderson Liverpool and Man Utd.
* ID can be gotten from 'player_dataset.csv'.
* String must be entered in quotes ie 'Soucek' valid but Soucek is not.
* Can have multiple entries separated by , .

**exclude_team_bench: you want no players from this team on your bench**
* String must be entered in quotes ie 'Spurs' valid but Spurs is not.
* Can have multiple entries separated by , .
"""

squad_optimise(
         metric=3,
         start_gw=1,
         end_gw=8,
         bench_value=None,
         bank=0,
         D=None,
         M=None,
         F=None,
         include_player=[],
         exclude_player=[],
         exclude_team_first=[],
         include_bench=[],
         exclude_bench=[],
         exclude_team_bench=[])