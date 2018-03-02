# Donation Predictions Using Random Forest 

## What
The idea behind this project is to look at certain economic indicators for a given year (mostly GDP related) and predict whether a donor will increase, decrease, or remain consistent in their donations to the UNCERF (United Nations Central Emergency Response Fund).

## Why
1. Demonstrate basic data cleaning and analysis skills
2. Practice pandas/scikit/sklearn
3. Fun

## How
Using pandas and scikit-learn, as follows:
1. Load csvs from UNCERF for donations and the World Bank for GDP data
2. Clean/transform datasets and join on Country Code and Year
3. Run random forest classification to estimate donation change

## Findings
Results from a single run of predict_donations.py:
| preds		| decrease	| increase	| same	|
| --------- |:---------:|:---------:|:-----:|
| actual	|			|			|		|
| decrease	| 70        |  38       | 0		|
| increase	|        49 |       67  |  0	|
| same		|      0    |     0     |  40	|
