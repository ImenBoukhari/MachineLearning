#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[1]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def clear_data(string1):
    if re.search(r'\[[a-z]* [0-9]+\]', string1) is None:
        return string1
    else:
        return string1.replace(re.search(r'\[[a-z]* [0-9]+\]', string1).group(), '')


def get_area(team,nhl_cities):
    for each in list(nhl_cities.index.values):
        if team in each:
            return nhl_cities.at[each, 'Metropolitan area']


def get_nhl_data():
    return out_df

def nhl_correlation(): 
    population_by_region = []  # pass in metropolitan area population from cities
    win_loss_by_region = []  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    nhl_df = pd.read_csv("assets/nhl.csv")
    cities = pd.read_html("assets/wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
    nhl_df = nhl_df[nhl_df['year'] == 2018].drop([0, 9, 18, 26], axis=0) # get only 2018 stats
    population = cities[['Metropolitan area', 'Population (2016 est.)[8]']]
    population = population.set_index('Metropolitan area')
    cities['NHL'] = cities['NHL'].apply(lambda x: clear_data(x))
    nhl_cities = cities[['Metropolitan area', 'NHL']].set_index('NHL')
    nhl_cities = nhl_cities.drop(['—', ''], axis=0)
    nhl_df['team'] = nhl_df['team'].apply(lambda x: x[:-1].strip() if x.endswith("*") else x.strip())
    nhl_df['area'] = nhl_df['team'].apply(lambda x: x.split(" ")[-1])
    nhl_df['area'] = nhl_df['area'].apply(lambda x: get_area(x,nhl_cities))
    out = []
    for group, frame in nhl_df.groupby('area'):
        total_wins = np.sum(pd.to_numeric(frame['W']))
        total_losses = np.sum(pd.to_numeric(frame['L']))
        total_matches = total_wins + total_losses
        ratio = (total_wins / total_matches)
        out_dict = {
            'Area': group,
            'Ratio': ratio
        }
        out.append(out_dict)
    new_df = pd.DataFrame(out)
    new_df = new_df.set_index('Area')
    out_df = pd.merge(new_df, population, how="inner", left_index=True, right_index=True)
    out_df['Population (2016 est.)[8]'] = pd.to_numeric(out_df['Population (2016 est.)[8]'])
    population_by_region = out_df['Population (2016 est.)[8]']
    win_loss_by_region = out_df['Ratio']
    return( stats.pearsonr(population_by_region, win_loss_by_region)[0])
    

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)
nhl_correlation()


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[4]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4 = 'NBA'


def nba_correlation():
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W/L%']]
    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    population_by_region = merge['Population']
    win_loss_by_region = merge['W/L%']

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nba_correlation()


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[5]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4 = 'MLB'


def mlb_correlation():
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('\ Sox', 'Sox')
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W-L%']]
    _df.rename(columns={"W-L%": "W/L%"}, inplace=True)
    _df['team'] = _df['team'].str.replace('\ Sox', 'Sox')
    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    population_by_region = merge['Population']
    win_loss_by_region = merge['W/L%']

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
mlb_correlation()


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[6]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4 = 'NFL'


def nfl_correlation():
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W-L%']]
    _df.rename(columns={"W-L%": "W/L%"}, inplace=True)
    dropList = []
    for i in range(_df.shape[0]):
        row = _df.iloc[i]
        if row['team'] == row['W/L%']:
            dropList.append(i)
    _df = _df.drop(dropList)

    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df['team'] = _df['team'].str.replace('+', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    population_by_region = merge['Population']
    win_loss_by_region = merge['W/L%']

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nfl_correlation()


# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

# In[8]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")


def nhl_df():
    Big4 = 'NHL'
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'\*', "")
    _df = _df[['team', 'W', 'L']]

    dropList = []
    for i in range(_df.shape[0]):
        row = _df.iloc[i]
        if row['team'] == row['W'] and row['L'] == row['W']:
            dropList.append(i)
    _df = _df.drop(dropList)

    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df = _df.astype({'team': str, 'W': int, 'L': int})
    _df['W/L%'] = _df['W'] / (_df['W'] + _df['L'])

    merge = pd.merge(team, _df, 'inner', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    return merge[['W/L%']]


def nba_df():
    Big4 = 'NBA'
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W/L%']]
    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})
    return merge[['W/L%']]


def mlb_df():
    Big4 = 'MLB'
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('\ Sox', 'Sox')
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W-L%']]
    _df.rename(columns={"W-L%": "W/L%"}, inplace=True)
    _df['team'] = _df['team'].str.replace('\ Sox', 'Sox')
    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    return merge[['W/L%']]


def nfl_df():
    Big4 = 'NFL'
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area'] = cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("", np.nan).replace("—",np.nan).dropna().reset_index().rename(columns={"value": "team"})
    team = pd.merge(team, cities, how='left', on='Metropolitan area').iloc[:, 1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team'] = team['team'].str.replace('[\w.]*\ ', '')

    _df = pd.read_csv("assets/" + str.lower(Big4) + ".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]', "")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)', "")
    _df['team'] = _df['team'].str.replace(r'[\xa0]', "")
    _df = _df[['team', 'W-L%']]
    _df.rename(columns={"W-L%": "W/L%"}, inplace=True)
    dropList = []
    for i in range(_df.shape[0]):
        row = _df.iloc[i]
        if row['team'] == row['W/L%']:
            dropList.append(i)
    _df = _df.drop(dropList)

    _df['team'] = _df['team'].str.replace('[\w.]* ', '')
    _df['team'] = _df['team'].str.replace('+', '')
    _df = _df.astype({'team': str, 'W/L%': float})

    merge = pd.merge(team, _df, 'outer', on='team')
    merge = merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    return merge[['W/L%']]


def create_df(sport):
    if sport == 'NFL':
        return nfl_df()
    elif sport == 'NBA':
        return nba_df()
    elif sport == 'NHL':
        return nhl_df()
    elif sport == 'MLB':
        return mlb_df()
    else:
        print("ERROR with intput!")


def sports_team_performance():
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k: np.nan for k in sports}, index=sports)

    for i in sports:
        for j in sports:
            if i != j:
                merge = pd.merge(create_df(i), create_df(j), 'inner', on=['Metropolitan area'])
                p_values.loc[i, j] = stats.ttest_rel(merge['W/L%_x'], merge['W/L%_y'])[1]

    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values
sports_team_performance()


# In[ ]:




