from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import load_data
import math

# Load UNCERF contribution data, sourced from:
# https://data.humdata.org/dataset/cerf-donor-contributions/resource/44cdab26-e9f8-4084-a5d3-18e8fde8a3e0
contributions = load_data.contributions()
# Clean contributions up a bit

# self join so we can see next years donor commitment
# and get just years where we know what happens next year
contributions = pd.merge(contributions, contributions, how= 'left', on=['countryCode'], suffixes=('','_next_year'))
contributions = contributions[contributions.year == contributions.year_next_year - 1]

# get just the columns we're interested in
contributions = contributions[['year', 'contributionID','countryCode', 'donor', 'donorcommitment', 'donorcommitment_next_year']]

# that's all the cleaning we need to do for contributions




# Load World Bank economic indicator data, sourced from:
# http://databank.worldbank.org/data/home.aspx
indicators = load_data.economic_indicators()
# Clean indicators up a bit

# we're gonna have to 'melt' these years so we can get from
# 	country, series, year1value, year2value, ...
# to:
# 	country, series, year, value
indicators = pd.melt(indicators, id_vars=["Country Name", "Country Code", "Series Name", "Series Code"], var_name = "Year", value_name="Value")
indicators = indicators[["Country Name", "Country Code", "Series Name", "Year", "Value"]]

# this dataset uses '..' to indicate missing values, let's fix that
indicators[indicators == '..'] = np.nan


# convert from "2006 [YR2006]" format to 2006 as an int
# apply might be overkill here, but it should give good future modularity
indicators['Year'] = indicators['Year'].apply(lambda x: int(x[:4]))

# similarly for Value, except as float
indicators['Value'] = indicators['Value'].apply(lambda x: float(x))


# now we need to pivot the series back up so we can get to
# country, year, series1value, series2value, ...
indicators = indicators.pivot_table(index=["Country Name", "Country Code", "Year"], columns="Series Name",
	values = "Value")

#get rid of the weird MultiIndex pivot table
# TODO: get these columns algorithmically, listing them manually is NOT SCALABLE
indicators.reset_index(drop=False,inplace=True)
indicators = indicators.reindex(["Country Name", "Country Code", "Year",
	"GDP (constant LCU)",
	"Central government debt, total (% of GDP)",
	"Current account balance (% of GDP)",
	"GDP growth (annual %)",
	"GDP per capita (constant LCU)",
	"GDP per capita growth (annual %)",
	"GDP per unit of energy use (constant 2011 PPP $ per kg of oil equivalent)"], axis = 1)
# limit this further, as it turns out there are a lot of NaNs
# in those other indicators
indicators = indicators[["Country Name", "Country Code", "Year",
	"GDP (constant LCU)",
	"GDP growth (annual %)",
	"GDP per capita (constant LCU)",
	"GDP per capita growth (annual %)"]]

# drop columns with NaN in them
indicators = indicators.dropna()

# we need to rename some columns so we can join with contributions
indicators.rename(columns = {'Year':'year','Country Code':'countryCode'}, inplace=True)

# that's all the cleaning we need to do for indicators



# now let's merge indicators and contributions into one dataframe
donor_data = pd.merge(contributions, indicators, how='inner', left_on=['year','countryCode'], right_on=['year','countryCode'])

# build up a donation_change_direction column, which just indicates if
# donations increase, decrease or stay the same next year
donor_data['donation_change'] = donor_data.donorcommitment_next_year - donor_data.donorcommitment
donor_data['donation_change_direction'] = donor_data.donation_change/abs(donor_data.donation_change)
donor_data[np.isnan(donor_data['donation_change_direction'])] = 0.0
donor_data['donation_change_direction'] = donor_data['donation_change_direction'].map({1.0:'increase',-1.0:'decrease',0.0:'same'})

# add an is_train column to split the set into training and test
donor_data['is_train'] = np.random.uniform(0,1,len(donor_data)) <= .75
train, test = donor_data[donor_data['is_train'] == True], donor_data[donor_data['is_train']==False]

# choose which columns should be our features
features = donor_data.columns[7:-3]

# build the classifier and train it on the training set
clf = RandomForestClassifier(n_jobs=2)
y, _ = pd.factorize(train['donation_change_direction'])
clf.fit(train[features],y)

# get our predictions for the testing set
preds = _[clf.predict(test[features])]

# print out the results of our predictions compared to 
print(pd.crosstab(test['donation_change_direction'], preds, rownames=['actual'], colnames=['preds']))
