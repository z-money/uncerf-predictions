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


| Preds        | Decrease           | Increase  | Same
| ------------- |:-------------:|:-----:|:---:
| **Actual** | | |
| **Decrease**      | 70 | 38 | 0
| **Increase**      | 49     |   67 | 0
| **Same** | 0 | 0 | 40

As an example of how to read this table we can look at the Decrease column.  This column tells us that we predicted a decrease in donation 70 times and were correct, 49 other times we predicted a decrease but the donations actually increased.  The same logic can be applied to the increase column and we can see we were right 67 times and wrong 38 when we predicted an increase.

This table seems to suggest we have decent predictive power but we should be hesitant to accept it's findings.  Random forests don't produce the same model every time, so we should probably average this out over many runs.  Also, random forests are in danger of overfitting, which we should be especially concerned about in the Same column where we were always right.  In fact, if we look at the data it appears that certain countries make the same round number donation every year which could be skewing our data some.

Another thing we should consider is that this only looks at direction of change, not magnitude, which could drastically change the meaning of these results.

## Possible Improvements
1. Add time sensitivity to the data, i.e look at donation trends over time, rather than year by year
2. Remove round number donations that are repeated every year
3. Look at Nations that enter/exit the set rather than donation amounts, i.e. churn
4. Explore different economic indicators, GDP may not be the best indicator to predict donations

## Conclusion
All in all this was a fun project. For viability this would probably need some more real-world knowledge about the donation dataset and how donation decisions are made.