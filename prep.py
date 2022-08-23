#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
from env import get_db_url



def acquire():
    
    filename = 'curriculum.csv'
    
    if os.path.exists(filename):
        
        return pd.read_csv(filename)
    
    else:
        query = """SELECT * FROM logs LEFT JOIN cohorts ON logs.user_id = cohorts.id"""
        df = pd.read_sql(query, get_db_url('curriculum_logs'))
        
        df.to_csv(filename, index=False)
        
        return df
    
def prepare_curriculum(df):
    """ Prepare the curriculum access logs dataframe """
    df = df.copy()
    
    # Only select specific columns
    df = df[['date','path','user_id','cohort_id','ip']]
    
    # Convert date to datetime
    df.date = pd.to_datetime(df.date)
    
    df = df.set_index(df.date)
    
    return df

def one_user_df_prep(df, user):
    '''
    This function returns a dataframe consisting of data for only a single defined user
    '''
    df = df[df.user_id == user]
    df.date = pd.to_datetime(df.date)
    df = df.set_index(df.date)
    pages_one_user = df.path.resample('d').count()
    return pages_one_user

def compute_pct_b(pages_one_user, span, weight, user):
    '''
    This function adds the %b of a bollinger band range for the page views of a single user's log activity
    '''
    # Calculate upper and lower bollinger band
    midband = pages_one_user.ewm(span=span).mean()
    stdev = pages_one_user.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    
    # Add upper and lower band values to dataframe
    bb = pd.concat([ub, lb], axis=1)
    
    # Combine all data into a single dataframe
    my_df = pd.concat([pages_one_user, midband, bb], axis=1)
    my_df.columns = ['pages_one_user', 'midband', 'ub', 'lb']
    
    # Calculate percent b and relevant user id to dataframe
    my_df['pct_b'] = (my_df['pages_one_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def plot_bands(my_df, user):
    '''
    This function plots the bolliger bands of the page views for a single user
    '''
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages_one_user, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()

def find_anomalies(df, user, span, weight, plot=False):
    '''
    This function returns the records where a user's daily activity exceeded the upper limit of a bollinger band range
    '''
    
    # Reduce dataframe to represent a single user
    pages_one_user = one_user_df_prep(df, user)
    
    # Add bollinger band data to dataframe
    my_df = compute_pct_b(pages_one_user, span, weight, user)
    
    # Plot data if requested (plot=True)
    if plot:
        plot_bands(my_df, user)
    
    # Return only records that sit outside of bollinger band upper limit
    return my_df[my_df.pct_b>1]

def get_lower_and_upper_bounds(x, k = 1.5):
    """Returns lower and upper bounds of series x using IQR range rule with multiplier k"""
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3-q1
    upper = q3 + k * iqr
    lower = q1 - k * iqr
    
    return upper, lower

def prepare_data(df):
    pnames = {  1: 'Full Stack PHP',
            2: 'Full Stack Java',
            3: 'Data Science',
            4: 'Front-End'
            }
    df['program'] = df.program_id.replace(pnames)
    df=df.rename(columns={'path': 'endpoint', 'name':'cohort'})
    df=df.drop(columns=['id'])
    df.date=pd.to_datetime(df.date)
    df.start_date=pd.to_datetime(df.start_date)
    df.end_date=pd.to_datetime(df.end_date)
    df.time=pd.to_timedelta(df.time)
    df['datetime']=df.date+df.time
    df=df.set_index('datetime')
    df= df.drop(columns = ['date', 'time','deleted_at'])
    df['role'] = df['cohort'].apply(lambda x: 'staff' if x == 'staff' else 'student')
    
    return df

    