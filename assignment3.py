#!/usr/bin/env python
# coding: utf-8

# # Assignment 3
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. All questions are worth the same number of points except question 1 which is worth 17% of the assignment grade.
# 
# **Note**: Questions 3-13 rely on your question 1 answer.

# In[1]:




# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
#import warnings
#warnings.filterwarnings('ignore')


# ### Question 1
# Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`
# 
# Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.
# 
# Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*

# In[2]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge
answer_one()


# In[3]:


assert type(answer_one()) == pd.DataFrame, "Q1: You should return a DataFrame!"

assert answer_one().shape == (15,20), "Q1: Your DataFrame should have 20 columns and 15 entries!"


# In[4]:


# Cell for autograder.


# ### Question 2
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[5]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[6]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_two():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    merge = Energy.merge(GDP, on = "Country")
    merge1 = merge.merge(ScimEn,on = "Country")
    merge1.set_index("Country", inplace = True)
    
    merge2 = Energy.merge(GDP,how="outer", on = "Country")
    merge3 = merge2.merge(ScimEn,how="outer",on = "Country")
    merge3.set_index("Country", inplace = True)
 
    return (merge3.shape[0]-merge1.shape[0])
    #raise NotImplementedError()
answer_two()


# In[7]:


assert type(answer_two()) == int, "Q2: You should return an int number!"


# ### Question 3
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[34]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge

def answer_three():
    Top15 = answer_one()
    avgGDP = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis = 1).rename('avgGDP').sort_values(ascending= False)
    return pd.Series(avgGDP)
                    
answer_three()
    #raise NotImplementedError()


# In[9]:


assert type(answer_three()) == pd.Series, "Q3: You should return a Series!"


# ### Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[10]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge

def answer_three():
    avgGDP = answer_one().iloc[:,10:].T.mean(skipna = True).sort_values(ascending = False)
    return avgGDP
def answer_four():
    # YOUR CODE HERE
    Top15 = answer_one()
    Top15["AvgGDP"] = answer_three()
    Top15.sort_values("AvgGDP", ascending=False, inplace=True)
    final = Top15.iloc[5]['2015']
    initial = Top15.iloc[5]['2006']
    return abs(final - initial)    
answer_four()
    #raise NotImplementedError()


# In[11]:


# Cell for autograder.


# ### Question 5
# What is the mean energy supply per capita?
# 
# *This function should return a single number.*

# In[12]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge

def answer_five():
 
    return(answer_one()['Energy Supply per Capita'].agg("mean"))
    # YOUR CODE HERE
answer_five()
    #raise NotImplementedError()


# In[13]:


# Cell for autograder.


# ### Question 6
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[7]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge

def answer_six():
    merge2=answer_one()
    return((merge2["% Renewable"].idxmax(),merge2["% Renewable"].max()))
    # YOUR CODE HERE
answer_six()
    #raise NotImplementedError()

 
    
    


# In[15]:


assert type(answer_six()) == tuple, "Q6: You should return a tuple!"

assert type(answer_six()[0]) == str, "Q6: The first element in your result should be the name of the country!"


# ### Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[19]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
    
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge

def answer_seven():
    Top15 = answer_one()
    Top15['Ratio'] = Top15.iloc[:,4]/Top15.iloc[:,3]
    return ('China',Top15.iloc[:,20].max())
answer_seven()
    # YOUR CODE HERE
    #raise NotImplementedError()


# In[17]:


assert type(answer_seven()) == tuple, "Q7: You should return a tuple!"

assert type(answer_seven()[0]) == str, "Q7: The first element in your result should be the name of the country!"


# ### Question 8
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return the name of the country*

# In[21]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos] 
    
  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge
def answer_eight():
    population = ((answer_one()["Energy Supply"]/
              answer_one()["Energy Supply per Capita"])
              .sort_values(ascending = False))
    return population.index[2]
answer_eight()
    #raise NotImplementedError()


# In[19]:


assert type(answer_eight()) == str, "Q8: You should return the name of the country!"


# ### Question 9
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[32]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos]  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True)
    return merge
def answer_nine():
    Top15 = answer_one()
    Top15['Pop'] = Top15.iloc[:,7]/Top15.iloc[:,8]
    Top15['Citable docs per Capita'] = Top15.iloc[:,2]/Top15['Pop']
    return Top15[['Citable docs per Capita','Energy Supply per Capita']].corr(method='pearson').iloc[0,1]
answer_nine()


# In[25]:


def plot9():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[ ]:


assert answer_nine() >= -1. and answer_nine() <= 1., "Q9: A valid correlation should between -1 to 1!"


# ### Question 10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[63]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos]  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True,ascending= True)
    return merge
def answer_ten():
    Top15 = answer_one()

    # T / F for % renewable over median or not
    Top15['HighRenew'] = Top15['% Renewable'] >= Top15['% Renewable'].median()
    Top15['HighRenew'] = Top15['HighRenew'].apply(lambda x: 1 if x else 0)

    # sorted by Rank
    Top15.sort_values(by='Rank', inplace=True)

    return Top15['HighRenew']

answer_ten()  
    #raise NotImplementedError()


# In[49]:


assert type(answer_ten()) == pd.Series, "Q10: You should return a Series!"


# ### Question 11
# Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[57]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos]  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True,ascending= True)
    return merge
def answer_eleven():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15 = answer_one()
    Top15['size'] = None
    Top15['Pop'] = Top15.iloc[:,7]/Top15.iloc[:,8]
    Top15['Continent'] = None
    for i in range(len(Top15)):
        Top15.iloc[i,20] = 1
        Top15.iloc[i,22]= ContinentDict[Top15.index[i]]
    ans = Top15.set_index('Continent').groupby(level=0)['Pop'].agg({'size': np.size, 'sum': np.sum, 'mean': np.mean,'std': np.std})
    ans = ans[['size', 'sum', 'mean', 'std']]
    return ans
answer_eleven()


# In[ ]:


assert type(answer_eleven()) == pd.DataFrame, "Q11: You should return a DataFrame!"

assert answer_eleven().shape[0] == 5, "Q11: Wrong row numbers!"

assert answer_eleven().shape[1] == 4, "Q11: Wrong column numbers!"


# ### Question 12
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[66]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos]  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True,ascending= True)
    return merge
def answer_twelve():
    Top15 = answer_one()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'
                     }

    Top15['Continent'] = Top15.index.map(lambda c: ContinentDict[c])

    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html
    Top15['% Renewable bins'] = pd.cut(Top15['% Renewable'], 5)

    return Top15.groupby(['Continent', '% Renewable bins']).size()

answer_twelve()


# In[ ]:


assert type(answer_twelve()) == pd.Series, "Q12: You should return a Series!"

assert len(answer_twelve()) == 9, "Q12: Wrong result numbers!"


# ### Question 13
# Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results).
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a series `PopEst` whose index is the country name and whose values are the population estimate string*

# In[61]:


import pandas as pd
import numpy as np
import re
def no_parenthesis(data): 
    # Search for opening bracket in the name followed by 
    # any characters repeated any number of times 
    if re.search('\s\(.*', data): 
  
        # Extract the position of beginning of pattern 
        pos = re.search('\s\(.*', data).start() 
  
        # return the cleaned name 
        return data[:pos]  
    else: 
        # if clean up needed return the same name 
        return data
def answer_one():
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                   header=  17, #Drop header
                   skipfooter = 38, #Drop footer (counting from the bottom)
                   usecols = "B,D:F", #Select useful columns
                   na_values= "...", #define "..." as NaN
                   names = ["Country", "Energy Supply", "Energy Supply per Capita", "% Renewable"])
                   #rename columns

    Energy["Country"].replace({"Republic of Korea": "South Korea",
                "United States of America": "United States",
                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                "China, Hong Kong Special Administrative Region": "Hong Kong"},
                inplace = True) #change some names          
    Energy["Energy Supply"] = Energy["Energy Supply"] * 1_000_000 #Pentajoules to Gigajoules
    Energy['Country'] = Energy['Country'].apply(no_parenthesis) 


    GDP = pd.read_csv("assets/world_bank.csv",
                     header = 4) 

    GDP.rename(columns = {"Country Name":"Country"}, inplace = True) 

    GDP["Country"].replace({"Korea, Rep.": "South Korea", 
                                    "Iran, Islamic Rep.": "Iran",
                                    "Hong Kong SAR, China": "Hong Kong"},
                                    inplace = True) #change some names  

    GDP = GDP.iloc[:, [0] + list(range(50,60))]


    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")


    merge = Energy.merge(GDP, on = "Country")
    merge = merge.merge(ScimEn[ScimEn["Rank"] <= 15], on = "Country")
    merge.set_index("Country", inplace = True)
    merge = merge.reindex(columns =  ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                              'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                              '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                              '2015'])
    merge.sort_values("Rank", inplace = True,ascending= True)
    return merge
def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15.iloc[:,7]/Top15.iloc[:,8]).astype(str)
    return Top15['PopEst']
answer_thirteen()


# In[62]:


assert type(answer_thirteen()) == pd.Series, "Q13: You should return a Series!"

assert len(answer_thirteen()) == 15, "Q13: Wrong result numbers!"


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[ ]:


def plot_optional():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

