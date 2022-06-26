import pandas as pd
import argparse

teams = ['atalanta', 'bologna', 'cagliari','empoli','fiorentina','genoa','inter','juventus','lazio','milan',
          'napoli','roma','salernitana','sampdoria','sassuolo','spezia','torino','udinese','venezia','verona']

def parse_args():
    parser = argparse.ArgumentParser(description="Winning fantasy football")
    parser.add_argument('-pt', dest="ppath", default= 'C://Users//paletto//Desktop//Ricerca//Fantasy_Soccer_OR//' , type=str, 
                        help='path of the folder where days and players folders are located')
    parser.add_argument('-fd', dest="first_day", default=3, type=int, 
                        help='first day of the league, greater or equal to 3, less than auct_day')
    parser.add_argument('-ld', dest="last_day", default=38, type=int,
                        help='last day of the league, equal or less than 38, greater than auct_day')
    parser.add_argument('-ad', dest="auct_day", default=23, type=int,
                        help='day of the auction, greater than first_day and smaller than last_day')
    parser.add_argument('-f', dest="formation", default="343", type=str,
                        help='formation without goalkeeper as string, ex 343')
    parser.add_argument('-c', dest="coins", default=500, type=int,
                        help='coins for the first auction')
    parser.add_argument('-a', dest="auct", default=5, type=int,
                        help='number of players that can be exchanged during the winter auction')
    parser.add_argument('-g', dest="ngoals", default=6, type=int,
                        help='number of points that make a goal')
    args = parser.parse_args()
    return args

def load_role(role):
    pla = pd.read_excel(args.ppath+"players//"+role+'.xlsx', header=None)
    pla.columns = ['p','player name', 'c', 'team','price']
    pla['player name'] = pla['player name'] + pla['c']
    pla['player name'] = pla['player name'].str.replace(' ','')
    del pla['c']
    pla = pla.set_index('player name')
    del pla['p']
    return pla

if __name__ == "__main__":
    args = parse_args()
    
    first_day = args.first_day
    auct_day = args.auct_day+1 # I add 1 because they are intended as indices
    last_day = args.last_day+1
    
    print("Loading scores")
    # I save, day by day, the scores of all the teams and put them all together in round_1.
    # every element of the list is the grades of all the players of all the teams for a dingle day
    
    round1 = []
    for nday in range(first_day,auct_day):
        teamsc = []
        for el in teams:
            teamsc.append(pd.read_excel(args.ppath+"days//"+str(nday)+' day//'+str(el)+'.xlsx', 
                                        index_col=0, usecols=[1,3],))
        day = pd.concat(teamsc, axis=0)
        day.columns = ['scores '+str(nday)]
        round1.append(day)
        
    round2 = []
    for nday2 in range(auct_day,last_day):
        teamsc2 = []
        for el in teams:
            teamsc2.append(pd.read_excel(args.ppath+"days//"+str(nday2)+' day//'+str(el)+'.xlsx', 
                                         index_col=0, usecols=[1,3],))
        day2 = pd.concat(teamsc2, axis=0)
        day2.columns = ['scores '+str(nday2)]
        round2.append(day2)
    
    # Now I merge the grades so that for every player I have all the grades of each round separated
    # I have to merge them one at the time so that if a player is not present in all days (for example
    # if he joined the team on the sixth day) he will not be removed from the players but hw will be
    # given nans (that after will be filled with zeros).
    unite = round1[0]
    for ind in range(1,len(round1)):
        unite = pd.merge(unite, round1[ind], left_index=True, right_index=True, how='outer') # unisco al totale
    unite.index = unite.index.str.upper()
    unite.index = unite.index.str.replace(' ','')
    unite2 = round2[0]
    for ind in range(1,len(round2)):
        unite2 = pd.merge(unite2, round2[ind], left_index=True, right_index=True, how='outer') # unisco al totale
    unite2.index = unite2.index.str.upper()
    unite2.index = unite2.index.str.replace(' ','')
    
    
    print("Loading players")
    # I load all the files with names and prices of the players, one for round.
    # I join them with their grades so that for every role of each round I have all the grades
   
    keepers = load_role('keepers')
    keep_1 = keepers.join(unite, how='left')
    keep_1.fillna(0, inplace=True)
    
    defenders = load_role('defenders')
    defe_1 = defenders.join(unite, how='left')
    defe_1.fillna(0, inplace=True)
    
    midfielders = load_role('midfielders')
    midf_1 = midfielders.join(unite, how='left')
    midf_1.fillna(0, inplace=True)
    
    strikers = load_role('strikers')
    stri_1 = strikers.join(unite, how='left')
    stri_1.fillna(0, inplace=True)
    
    keepers2 = load_role('keepers2')
    keep_2 = keepers2.join(unite2, how='left')
    keep_2.fillna(0, inplace=True) 
    
    defenders2 = load_role('defenders2')
    defe_2 = defenders2.join(unite2, how='left')
    defe_2.fillna(0, inplace=True)
    
    midfielders2 = load_role('midfielders2')
    midf_2 = midfielders2.join(unite2, how='left')
    midf_2.fillna(0, inplace=True)
     
    strikers2 = load_role('strikers2')
    stri_2 = strikers2.join(unite2, how='left')
    stri_2.fillna(0, inplace=True)
    
    print("Managing players' scores and prices")
    # I extract the prices and the grades as arrays.
    
    keep_1_price = keep_1['price'].values
    keep_1_scores = keep_1[['scores '+str(el) for el in range(first_day,auct_day)]].values
    
    defe_1_price = defe_1['price'].values
    defe_1_scores = defe_1[['scores '+str(el) for el in range(first_day,auct_day)]].values
    
    midf_1_price = midf_1['price'].values
    midf_1_scores = midf_1[['scores '+str(el) for el in range(first_day,auct_day)]].values
    
    stri_1_price = stri_1['price'].values
    stri_1_scores = stri_1[['scores '+str(el) for el in range(first_day,auct_day)]].values
    
    keep_2_price = keep_2['price'].values
    keep_2_scores = keep_2[['scores '+str(el) for el in range(auct_day,last_day)]].values
    
    defe_2_price = defe_2['price'].values
    defe_2_scores = defe_2[['scores '+str(el) for el in range(auct_day,last_day)]].values
    
    midf_2_price = midf_2['price'].values
    midf_2_scores = midf_2[['scores '+str(el) for el in range(auct_day,last_day)]].values
    
    stri_2_price = stri_2['price'].values
    stri_2_scores = stri_2[['scores '+str(el) for el in range(auct_day,last_day)]].values
    
    # formation
    n_keep = 1
    n_defe = int(args.formation[0])
    n_midf = int(args.formation[1])
    n_stri = int(args.formation[2])
    
    # effective numbers of players per role.
    totk = keep_1.shape[0]
    totd = defe_1.shape[0]
    totm = midf_1.shape[0]
    tots = stri_1.shape[0]
    n_play = totk + totd + totm + tots
    
    # all the grades of the two round ordered by role
    conc1 = pd.concat([keep_1,defe_1,midf_1,stri_1],axis=0)
    conc2 = pd.concat([keep_2,defe_2,midf_2,stri_2],axis=0)
    # names of the players ordered by role
    k_d_m_s = conc1.index.to_list()
    # prices ordered by role
    prices_conc1 = conc1['price'].values
    prices_conc2 = conc1['price'].values
    # scores for each round ordered by role
    scores_conc1 = conc1[['scores '+str(el) for el in range(first_day,auct_day)]].values
    scores_conc2 = conc2[['scores '+str(el) for el in range(auct_day,last_day)]].values
    # scores of the day s, one below the other
    list_scores1 = [scores_conc1[i,j] for j in range(auct_day-first_day) for i in range(n_play)]
    list_scores2 = [scores_conc2[i,j] for j in range(last_day-auct_day) for i in range(n_play)]
    
    # starts of the days in the new indexes
    pplay1 = [0+n_play*i for i in range(auct_day-first_day)]
    pplay2 = [0+n_play*i for i in range(last_day-auct_day)] # numero di giornate ritorno
    
    print("Model definition")
    
    import pulp 
    model = pulp.LpProblem('Fanta', pulp.LpMaximize)
    
    # teams of the two rounds
    x1 = pulp.LpVariable.dict('x1_%s', k_d_m_s, lowBound=0, upBound=1, cat=pulp.LpInteger)
    x2 = pulp.LpVariable.dict('x2_%s', k_d_m_s, lowBound=0, upBound=1, cat=pulp.LpInteger)
    # players bought and sold in the winter auction
    bought = pulp.LpVariable.dict('bought_%s', k_d_m_s, lowBound=0, upBound=1, cat=pulp.LpInteger)
    sold = pulp.LpVariable.dict('sold_%s', k_d_m_s, lowBound=0, upBound=1, cat=pulp.LpInteger)
    #indices for y variable
    pairs1 = [(i,str(j)) for j in range(first_day,auct_day) for i in k_d_m_s]
    pairs2 = [(i,str(j)) for j in range(auct_day,last_day) for i in k_d_m_s]
    # lined up players for each day of each round
    y1 = pulp.LpVariable.dict('y1_%s_%s', pairs1, lowBound=0, upBound=1, cat=pulp.LpInteger) # matrice 0,1
    y2 = pulp.LpVariable.dict('y2_%s_%s', pairs2, lowBound=0, upBound=1, cat=pulp.LpInteger) # matrice 0,1
    # scores of the players of each round ordered as the other variables
    scores_players1 = dict(zip(pairs1,list_scores1))
    scores_players2 = dict(zip(pairs2,list_scores2))
    # prices payed at the first and at the second auction
    prices_players1 = dict(zip(k_d_m_s, prices_conc1))
    prices_players2 = dict(zip(k_d_m_s, prices_conc2))
    
    # model's objective function
    model += sum([y1[cop]*scores_players1[cop] for cop in pairs1]) + sum([y2[copp]*scores_players2[copp] for copp in pairs2])
    
    # constraints on the number of players you can buy for every role
    model += sum([x1[i] for i in keep_1.index.to_list()]) == 3
    model += sum([x1[i] for i in defe_1.index.to_list()]) == 8
    model += sum([x1[i] for i in midf_1.index.to_list()]) == 8
    model += sum([x1[i] for i in stri_1.index.to_list()]) == 6
    model += sum([x2[i] for i in keep_1.index.to_list()]) == 3 # keep_1.index == keep_2.index
    model += sum([x2[i] for i in defe_1.index.to_list()]) == 8
    model += sum([x2[i] for i in midf_1.index.to_list()]) == 8
    model += sum([x2[i] for i in stri_1.index.to_list()]) == 6
    
    # constraints about auctions and players' prices
    model += sum([bought[i] for i in k_d_m_s]) <= args.auct
    model += sum([sold[i] for i in k_d_m_s]) <= args.auct
    
    model += sum([prices_players1[i]*x1[i] for i in k_d_m_s]) <= args.coins
    
    for i in k_d_m_s:
        model += x2[i]-x1[i]-bought[i]+sold[i] == 0
        model += bought[i]*prices_players1[i] <= 1
    model += sum([prices_players1[i]*(x1[i]-sold[i]) + bought[i]*prices_players2[i] for i in k_d_m_s]) <= 500
    
    # constraints linking y and x, only bought players can be lined up
    for start in pplay1:
        for step in range(n_play):
            model += y1[pairs1[start+step]] <= x1[k_d_m_s[step]]
        
    for start in pplay2:
        for step in range(n_play):
            model += y2[pairs2[start+step]] <= x2[k_d_m_s[step]]
    
    # minimum number of points you want to score every game
    for start in pplay1:
        model += sum([y1[pairs1[start+step]]*scores_players1[pairs1[start+step]] for step in range(n_play)]) >= 78
    for start in pplay2:
        model += sum([y2[pairs2[start+step]]*scores_players2[pairs2[start+step]] for step in range(n_play)]) >= 78
    
    # constraint on number of lined up players for every role
    for start in pplay1:
        model += sum(y1[pairs1[start+step]] for step in range(totk)) == n_keep
    for start in pplay1:
        model += sum(y1[pairs1[start+totk+step]] for step in range(totd)) == n_defe
    for start in pplay1:
        model += sum(y1[pairs1[start+totk+totd+step]] for step in range(totm)) == n_midf
    for start in pplay1:
        model += sum(y1[pairs1[start+totk+totd+totm+step]] for step in range(tots)) == n_stri  

    for start in pplay2:
        model += sum(y2[pairs2[start+step]] for step in range(totk)) == n_keep
    for start in pplay2:
        model += sum(y2[pairs2[start+totk+step]] for step in range(totd)) == n_defe
    for start in pplay2:
        model += sum(y2[pairs2[start+totk+totd+step]] for step in range(totm)) == n_midf
    for start in pplay2:
        model += sum(y2[pairs2[start+totk+totd+totm+step]] for step in range(tots)) == n_stri  
    
    print("Solving model")
    
    solver = pulp.apis.PULP_CBC_CMD()
    model.solve(solver)
    
    print("saving results")
    # for each round I save the best team, the points and the golas scored every day by the user
    # the players exchanged during the winter auction and the days each player is lined up.
    
    import re
    
    best1 = []
    for v in model.variables()[n_play*2: n_play*3]:
        if v.varValue > 0.5:
            nome = v.name[3:]
            nome = re.sub('_',' ',nome)
            best1.append(nome)
    best2 = []
    for v in model.variables()[n_play*3: n_play*4]:
        if v.varValue > 0.5:
            nome = v.name[3:]
            nome = re.sub('_',' ',nome)
            best2.append(nome)
    
    import numpy as np
    best_k1 = keep_1[keep_1.index.isin(best1)].drop(columns = ['team','price'])
    pkeep1 = np.sort(best_k1, axis=0)[-n_keep:]
    best_d1 = defe_1[defe_1.index.isin(best1)].drop(columns = ['team','price'])
    pdefe1 = np.sort(best_d1, axis=0)[-n_defe:]
    best_m1 = midf_1[midf_1.index.isin(best1)].drop(columns = ['team','price'])
    pmidf1 = np.sort(best_m1, axis=0)[-n_midf:]
    best_s1 = stri_1[stri_1.index.isin(best1)].drop(columns = ['team','price'])
    pstri1 = np.sort(best_s1, axis=0)[-n_stri:]
    
    best_team1 = pd.concat([best_k1, best_d1, best_m1, best_s1],axis=0)
    best_team1.to_excel('results/best_team_1.xlsx')
    
    points1 = np.concatenate((pkeep1,pdefe1,pmidf1,pstri1),axis=0).sum(axis=0)
    goals1 = np.floor((points1-66)/args.ngoals+1)
    dfp1 = pd.DataFrame([points1,goals1],index=['points','goals'],
                        columns = ['scores '+str(el) for el in range(first_day,auct_day)])
    dfp1.to_excel('results/goals_1.xlsx')
    
    best_k2 = keep_2[keep_2.index.isin(best2)].drop(columns = ['team','price'])
    pkeep2 = np.sort(best_k2, axis=0)[-n_keep:]
    best_d2 = defe_2[defe_2.index.isin(best2)].drop(columns = ['team','price'])
    pdefe2 = np.sort(best_d2, axis=0)[-n_defe:]
    best_m2 = midf_2[midf_2.index.isin(best2)].drop(columns = ['team','price'])
    pmidf2 = np.sort(best_m2, axis=0)[-n_midf:]
    best_s2 = stri_2[stri_2.index.isin(best2)].drop(columns = ['team','price'])
    pstri2 = np.sort(best_s2, axis=0)[-n_stri:]
    
    best_team2 = pd.concat([best_k2, best_d2, best_m2, best_s2],axis=0)
    best_team2.to_excel('results/best_team_2.xlsx')
        
    points2 = np.concatenate((pkeep2,pdefe2,pmidf2,pstri2),axis=0).sum(axis=0)
    goals2 = np.floor((points2-66)/args.ngoals+1)
    dfp2 = pd.DataFrame([points2,goals2],index=['points','goals'],
                        columns = ['scores '+str(el) for el in range(auct_day,last_day)])
    dfp2.to_excel('results/goals_2.xlsx')
    
    exch = []
    for v in model.variables()[:n_play*2]:
        if v.varValue > 0.5:
            nome = v.name
            nome = re.sub('_',' ',nome)
            exch.append(nome)
    MyFile=open('results/exchanged.txt','w')
    for element in exch:
         MyFile.write(element)
         MyFile.write('\n')
    MyFile.close()
    
    pres1 = []
    for v in model.variables()[n_play*4: n_play*4+n_play*(auct_day-first_day)]:
        if v.varValue > 0.5:
            nome = v.name
            nome = re.sub('_',' ',nome)
            pres1.append(nome)
    MyFile=open('results/presences1.txt','w')
    for element in pres1:
         MyFile.write(element)
         MyFile.write('\n')
    MyFile.close()
    
    pres2 = []
    for v in model.variables()[n_play*4+n_play*(auct_day-first_day): n_play*4+n_play*last_day]:
        if v.varValue > 0.5:
            nome = v.name
            nome = re.sub('_',' ',nome)
            pres2.append(nome)
    MyFile=open('results/presences2.txt','w')
    for element in pres2:
         MyFile.write(element)
         MyFile.write('\n')
    MyFile.close()
    
    print('Finish')
    
    
    
    