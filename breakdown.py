import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def add_page_pct(df):
    df=df.reset_index()
    page_pct = {}
    for i in df.user_id.to_list():
        page_pct[i]=(len(df[df.user_id==i].endpoint.value_counts())/len(df.endpoint.value_counts()))
        
    page_pct=pd.DataFrame(page_pct,index=range(1)).T
    page_pct=page_pct.reset_index()
    page_pct.columns = ['user_id','pct_of_pages_visited']
    
    df=df.merge(right=page_pct,on='user_id')
    df=df.set_index(df.datetime)
    df=df.drop(columns='datetime')
    return df

def find_sus_accounts(df):
    sus_1 = df[df.pct_of_pages_visited >.20]
    sus_2 = df[df.cohort_id.isna()]
    alot_of_ips = pd.DataFrame(df.groupby('user_id').ip.nunique()).reset_index()
    alot_of_ips = alot_of_ips[alot_of_ips.ip>20].user_id.to_list()
    sus_3 = df[df.user_id.isin(alot_of_ips)]
    return sus_1,sus_2, sus_3
   
    
def breakdown(df):
    df = add_page_pct(df)
    sus_1,sus_2,sus_3 = find_sus_accounts(df)
    sus_list = []
    for i in sus_1.user_id.to_list():
        if i not in sus_list:
            sus_list.append(i)
        else:
            continue

    for i in sus_2.user_id.to_list():
        if i not in sus_list:
            sus_list.append(i)
        else:
            continue

    for i in sus_3.user_id.to_list():
        if i not in sus_list:
            sus_list.append(i)
        else:
            continue
    for i in sus_list:
        plt.figure(figsize=(7,5))
        df[df.user_id==i].resample('M').user_id.sum().plot()
        plt.title(f'User {i} activity over time')
        plt.show()
        print(f'user {i} is a {str(df[df.user_id==i].program.to_list()[:1])} student. ')
        print( df[df.user_id==i].resample('M').endpoint.value_counts())
        