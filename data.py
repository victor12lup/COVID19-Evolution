#12061468
# Victor Salazar
from datetime import datetime, timedelta
import datetime
import pandas as pd
import pycountry_convert as pc

def date(x):
    """ Given a string type of date 2020-11-23 return a datetime object in the format month day year
        
        Parameters:
        string date
    """
    return datetime.datetime.strptime(x,'%m/%d/%y') 

def date_name(x):
    """ Given a datetime object  return a string 20May, 27  
        
        Parameters:
        datetime object
    """
    return datetime.datetime.strptime(x,'%y%b,%d')

def daily_increase(df,df_cumu):
    """ Transforms the columns from a cumulative dataframe df into a snpashot type data 
        
        Parameters:
        dataframe 
    """
    x = 0
    for column in df:
        # with the help of datetime object is possible to use timedelta
        if x>1:
            df[column] = df_cumu[column] - df_cumu[column-timedelta(1)]
        x+= 1
    return df 

def monthly(df):
    """ From a dataframe with daily increases returns a a montlhy average of the data 
        
        Parameters:
        dataframe with daily entries
    """    
    
    #df = df.groupby("Country/Region").sum()
    df = df.transpose()
    #Grouping monthly to get an average ,as data is daily and not monthly
    df_monthly = df.groupby(pd.Grouper(freq='M')).mean()
    df_monthly.index.name = 'Date'
    #Give a shorter name to the dates, to be easily interpretable
    df_monthly.index = df_monthly.index.strftime("%b%y")
    df_monthly.columns.name = 'Country'
    df_monthly
    return  df_monthly

def country_to_continent(country_name):
    """ Returns the continent name of a country
        
        Parameters:
        country string
    """    

    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def prueba(x):
    return datetime(x,x,x) 

