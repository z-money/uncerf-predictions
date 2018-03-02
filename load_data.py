import pandas as pd
import numpy as np
import csv

def contributions():
	df = pd.read_csv('data/contributions.csv')
	return df

def economic_indicators():
	df = pd.read_csv('data/economic_indicators.csv')
	return df