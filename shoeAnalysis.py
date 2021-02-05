import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sn
#reading in excel file
stockX = pd.read_excel("stockXData.xlsx")

#printing information about data to verify we dont have any issues and to know what variables it wrote its data into
print(stockX.shape)
print(stockX.info())

#dropping the brand and release date column
stockX = stockX.drop(['Brand'], axis=1)
stoxkX = stockX.drop(['Release Date'], axis = 1)
print(stockX.head())   

#Renaming Columns to be a little easier to work with
newColNames = {'Order Date':'orderDate','Sneaker Name':'model','Sale Price':'salePrice', 'Retail Price':'retailPrice','Shoe Size':'shoeSize','Buyer Region':'buyerState'}
stockX.rename(columns=newColNames, inplace=True)
    #print(stockX.head())

#removing the retail price column and making a new column that is the difference between the retail and sales price
stockX['profit'] = stockX['salePrice'] - stockX['retailPrice'] 
print(stockX.head())

#printing a correlation matrix
stockX.plot(x ='orderDate', y='profit', kind = 'scatter')
column_1 = stockX["shoeSize"]
column_2 = stockX["profit"]
plt.show()
correlation = column_1.corr(column_2)
print(correlation)

#grouping similar show models together and taking their mean
stockXbyDate = stockX.groupby('model').mean('profit')
print(stockXbyDate.head())

#importing s&p 500 .csv file
sp500 = pd.read_csv('s&p500.csv')
print(sp500.head())

#deleting unecessary columns
sp500['SP500'] = sp500.mean(axis=1)
sp500 = sp500.drop([' Close/Last'], axis=1)
sp500 = sp500.drop([' Volume'], axis=1)
sp500 = sp500.drop([' Open'], axis=1)
sp500 = sp500.drop([' High'], axis=1)
sp500 = sp500.drop([' Low'], axis=1)
print(sp500.head())

#converting dates to a format in which panda can understand them
#not 100% fully what the errors does but it has to do something with error catching
sp500['Date'] = pd.to_datetime(sp500['Date'], errors='coerce')

#removing all rows from old dates
sp500 = sp500[(sp500['Date'].dt.year > 1970) & (sp500['Date'].dt.year < 2020)]
print(sp500.head())

#creating a scatter plot of sp500 against time
sp500.plot(x ='Date', y='SP500', kind = 'scatter')
plt.show()

#grouping stockX data by date
stockX1 = stockX.groupby('orderDate').mean('profit')
print(stockX1.head())


#merging the dataframes on date
merger = pd.merge(stockX1, sp500,left_on=['orderDate'],right_on=['Date'])

# create figure and axis objects with subplots()
fig,ax = plt.subplots()

# make a plot
ax.plot(merger['Date'], merger['SP500'], color="red", marker="o")

# set x-axis label
ax.set_xlabel("Date",fontsize=14)

# set y-axis label
ax.set_ylabel("S&P500",color="red",fontsize=14)

# twin object for two different y-axis on the sample plot
ax2=ax.twinx()

# creating a second y axis
ax2.plot(merger['Date'], merger['profit'],color="blue",marker="o")
ax2.set_ylabel("salePrice",color="blue",fontsize=14)

#question #1
#What is the correlation between the reselling of high end trainers and the stock market
plt.show()
column_1 = merger["salePrice"]
column_2 = merger["SP500"]
correlation = column_1.corr(column_2)
print(correlation)

#What years had the highest profits for shoe reselling
#Grouping data by year
mergedByyear = stockX.groupby(stockX['orderDate'].dt.month).mean('profit')
print(mergedByyear)
