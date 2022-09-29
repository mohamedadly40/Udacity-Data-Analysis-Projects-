#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a Dataset - [No Show Application]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### > Dataset Description 
# 
# > This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row 
# 
# 
# ### > Questions
# >**Q1. Gender effect on the show status**
# <br>**Q2. Reservation days before appointment and thier effect on the show status**
# <br>**Q3. Age categories effect on the show status**
# <br>**Q4. SMS received effect on the show status**
# <br>**Q5. "Scholarship", "Hypertension", "Diabetes","Alcoholism" and "Handicap" effect on the show status**

# <a id='wrangling'></a>
# ## Data Wrangling
# ### > Assessing Data
# 
# 
# > In this section of the report, we will load the data, check for cleanliness, and then trim and clean the dataset for analysis.
# 

# In[1]:


# Imported Packages 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.set()


# In[2]:


# Read Data

df = pd.read_csv('Database_No_show_appointments/noshowappointments-kagglev2-may-2016.csv')
print(df.head())


# ### Comments
# >**1. PatientId & AppointmentID**: Unused columns in the analysis **need to drop**
# <br>**2. Gender**: Need to change the data from ( F & M ) to ( Female & Male ) as it will facilate the show style
# <br>**3. ScheduledDay & AppointmentDay**: Need to split the remove the time and let the date only as specally that the AppointmentDay with unaccuracy time ('T00:00:00Z') also i need to calculate the reservation days between (Scheduled day & Appointment day) so need need to remove the time as it will facilitate the calculations
# <br>**4. Age Categories "New Column"**: Will create new column with age category (Kids, Child, Adults and Seniors)
# <br>**5. No-show**: Need to rename the column name to (Show) and change the data (No >> Yes & Yes >> No) which mean that "Yes" mean show and "No" mean  no show
# <br>**6. Update Columns name**: ("Hipertension" >> "Hypertension") and ("Handcap" >> "Handicap")
# 

# In[3]:


print(df.info())


# ### Comments
# >**Scheduled day & Appointment day**: need to change the data type to **timedate**
# >

# In[4]:


print(df.describe())


# ### Comments
# 
# >**Age**: there is unlogic element equal -1 need to update to the mean 

# 
# ### > Data Cleaning
# > In this section of the report, we will clean the data, to prepare the dataset for analysis.
# 

# In[ ]:


# create new columns with (Scheduled day & Appointment day) after the removing the time to be date only and change the type to be datatime

df['ScheduledDay_date'] = pd.to_datetime(df['ScheduledDay']).dt.date
df['ScheduledDay_date'] = pd.to_datetime(df['ScheduledDay_date'])
df['AppointmentDay_date'] = pd.to_datetime(df['AppointmentDay']).dt.date
df['AppointmentDay_date'] = pd.to_datetime(df['AppointmentDay_date'])

print(df.info())


# <font color='green'>
# New columns ( "ScheduledDay_date" & "AppointmentDay_date" ) created done and the type updated to datetime
# </font>
# 

# In[ ]:


# Rename columns ( Hipertension >> Hypertension % Handcap >> Handicap ) as correction typing
# Rename column ( No-show >> Show ) to facility presentation style

df.rename(columns={'Hipertension': 'Hypertension'}, inplace=True)
df.rename(columns={'Handcap': 'Handicap'}, inplace=True)
df.rename(columns={'No-show': 'Show'}, inplace=True)

print(df.columns)


# <font color='green'>
# Rename updated Done
# </font>
# 

# In[ ]:


# update unlogic -1 in the age with the mean 

df['Age'] = df['Age'].replace([-1], [df['Age'].mean()])
df['Age'] = df['Age'].astype(int)
print(df['Age'].describe())


# <font color='green'>
# Updated Done as the min Age equal 0 instead of -1
# </font>
# 

# In[ ]:


# check the columns of ( ScheduledDay_date & AppointmentDay_date ) as supposed Scheduled day less or equal the Appointment day

Check_ScheduledDay_date = df['ScheduledDay_date'] <= df['AppointmentDay_date']
print(Check_ScheduledDay_date.value_counts())


# <font color='red'>
# !! There are 5 dates of ScheduledDay_date larger than AppointmentDay_date which unlogic need to update
# </font>
# 

# In[ ]:


# update 5 dates of ScheduledDay_date to be equal the AppointmentDay_date 

new_ScheduledDay_date = []
for x, y in zip(df['ScheduledDay_date'], df['AppointmentDay_date']):
    if x <= y:
        new_ScheduledDay_date.append(x)
    else:
        new_ScheduledDay_date.append(y)
df['ScheduledDay_date'] = new_ScheduledDay_date

Check_ScheduledDay_date_after_update = df['ScheduledDay_date'] <= df['AppointmentDay_date']
print(Check_ScheduledDay_date_after_update.value_counts())


# <font color='green'>
# Updated Done as all the ScheduledDay_date less than or equal the AppointmentDay_date
# </font>

# In[ ]:


# Replacing ('F', 'M'), ('Female', 'Male') to facilite the presentaion style

df['Gender'] = df['Gender'].replace(['F', 'M'], ['Female', 'Male'])
print(df['Gender'].unique())


# <font color='green'>
# Updated Done
# </font>

# In[ ]:


# as mentioned above that we will update the "No-show" column to be "Show" 
#and update the data which (No >> Yes & Yes >> No) which mean that "Yes" mean show and "No" mean no show

new_Show = []
for s in df['Show']:
    if s == 'Yes':
        new_Show.append('No')
    elif s == 'No':
        new_Show.append('Yes')
df['Show'] = new_Show
print(df['Show'].unique())


# <font color='green'>
# Updated Done
# </font>

# In[ ]:


# Create New Column with Reservation days before AppointmentDay date 

df['Reservation_Days'] = df['AppointmentDay_date'].dt.date - df['ScheduledDay_date'].dt.date
df['Reservation_Days'] = (df['Reservation_Days'] / 86400000000000).astype(int)
new_Reservation_Days = []
for i in df['Reservation_Days']:
    if i == 0:
        new_Reservation_Days.append('1-During Same day')
    elif i > 0 and i <= 7:
        new_Reservation_Days.append('2-During 1st week')
    elif i > 7 and i <= 14:
        new_Reservation_Days.append('3-During 2nd week')
    elif i > 14 and i <= 31:
        new_Reservation_Days.append('4-During 2nd of half month')
    else:
        new_Reservation_Days.append('5-During more than one month')

df['Reservation_Days'] = new_Reservation_Days
print(df['Reservation_Days'].value_counts())


# <font color='green'>
# Create column with reservation days with the diferrent between ScheduledDay date and AppointmentDay date
# then divided this number on 86400000000000 with equal ( 24 hour * 60 min * 60 seconds * 1000000000 ) to can calculate the days
#     and divided to categories
#     <br>-- 1-During Same day
#     <br>-- 2-During 1st week
#     <br>-- 3-During 2nd week
#     <br>-- 4-During 2nd of half month
#     <br>-- 5-During more than one month
# </font>

# In[ ]:


# create categories for the Age in new column ( 'Kids', 'Childs', 'Adults', 'Seniors' )

df.loc[:, 'Age_cust'] = pd.cut(df['Age'], bins=[0, 10, 18, 37, 55, 115], labels=['Kids', 'Childs', 'Adults', 'Seniors', 'Retirement age'])
group_age_cust = df.groupby(['Age_cust', 'Show']).count().loc[:, 'Gender']
print(df['Age_cust'].unique())


# <font color='green'>
#     Creation of the new column done with the selected categories 
# <font color='green'>
#     <br>-- kids till 10 years
#     <br>-- Childs till 18 years
#     <br>-- Adults till 37 years
#     <br>-- Seniors till 55 years
#     <br>-- Retirement age above 55
# </font>

# In[ ]:


df.drop(['PatientId', 'AppointmentID', 'ScheduledDay', 'AppointmentDay'], axis=1, inplace=True)


# <font color='green'>
#     Drop unused columns
#     </font>

# In[ ]:


# Rearrange the columns 

df = df[['Gender', 'Age', 'Age_cust', 'ScheduledDay_date', 'AppointmentDay_date',
       'Reservation_Days', 'Neighbourhood', 'Scholarship', 'Hypertension',
       'Diabetes', 'Alcoholism', 'Handicap', 'SMS_received', 'Show']]
print(df.columns)


# In[ ]:


print(df.head())
print(df.info())


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > In this section of the report, we will **Compute statistics** and **create visualizations** for the data with the goal of addressing the research questions that we posed in the **Introduction section**.
# 

# In[ ]:


def analysis(df, col_name, show_col, col):
    group = df.groupby([col_name, show_col]).count().loc[:, col]
    keys = []
    for i in group.keys():
        item = i[0]
        if item not in keys:
            keys.append(item)

    no_show_percentage_list = []

    print('\nShowing Analysis:- Depend on {}\n'.format(col_name))
    if col_name == 'Age_cust':
        plt.figure(figsize=(3,5))
        Age_Boxplot = sns.boxplot(y=df["Age"])
        Age_Boxplot.set_title('Age Range')
        plt.ylabel('Age')
        plt.xlabel('Patients')
        plt.show()
        
        print(df["Age"].describe())
 
    elif col_name == 'Gender':
        female_df = df.Gender == 'Female'
        male_df = df.Gender == 'Male'

        def Gender_analysis(dataframe, col_name, Age_col):
            group = dataframe.groupby(col_name).count()[Age_col]
            data_group = pd.DataFrame(group.values, group.keys())
            data_group.columns = ['Numbers']
    
            explode = (0.05, 0.05)
            colors = ['pink', 'steelblue']
            plot = data_group.plot.pie(y='Numbers', figsize=(5, 5), autopct='%1.1f%%', colors=colors, explode=explode)
            plt.ylabel(' ')
            if Age_col == 'Hypertension':
                plt.title('Female VS Male')
            elif Age_col == 'Age':
                plt.title('Female Showing Status\n Yes: Show \nNo: No Show')
            else:
                plt.title('Male Showing Status\n Yes: Show \nNo: No Show')

        Gender_analysis(df, 'Gender', 'Hypertension')
        Gender_analysis(df[female_df], 'Show', 'Age')
        Gender_analysis(df[male_df], 'Show', 'Scholarship')
        
    
    else:    
        plt.figure(figsize=(14,4))
        analysis = sns.countplot(x=col_name, hue=df.Show, data=df, palette="Set2")
        analysis.set_title('{}\nShow / No Show'.format(col_name))
        plt.ylabel('Number of Patient')
        plt.show()
    
    for k in range(len(keys)):
        no_show_result = group[keys[k]]['No']
        show_result = group[keys[k]]['Yes']
        subtotal = group[keys[k]].sum()
        show_percentage = round(((show_result / subtotal) * 100), 1)
        show_percentage = "{}%".format(show_percentage)
        no_show_percentage = round(((no_show_result / subtotal) * 100), 1)
        no_show_percentage = "{}%".format(no_show_percentage)
        no_show_percentage_list.append(no_show_percentage)
        print(keys[k])
        print('-- Show Patient: {} ({})'.format(show_result, show_percentage))
        print('-- No Show Patient: {} ({})\n'.format(no_show_result, no_show_percentage))
    chart = pd.Series(keys, no_show_percentage_list)
    


# ### Q1. Gender effect on the show status 

# In[ ]:


analysis(df, 'Gender', 'Show', 'Age')


# <font color='brown'>
# As the above chart and statistics 
#     <br>-- As the above chart we will find that the female appointments almost double the male with percentage (65% : 35%)
#     <br>-- About the percetage of Show there are almost no effect by gender as the no show percentage almost the same average 20% evenif female or male 
#     <br> conclusion :-
#     <br>-- Almost there is no effect by Gender with considration that the female appointments almost double male 
# </font>
# 

# ### Q2. Reservation days before appointment and thier effect on the show status

# In[ ]:


analysis(df, 'Reservation_Days', 'Show', 'Age')


# <font color='brown'>
# <br>As the above chart and statistics**
#     <br> -- The highest show percentage with 95% for who make reservation in the same day
#     <br> -- The show percentage going to decrease when the reservation days before the Appointment increase which mean that the longer the reservation period effect negative on the show status.
#     <br>
#     <br> Reasons return to :-
#     <br> -- Maybe Patients forget the Appointment 
#     <br> -- Maybe Patients look better and feel there are no need to make the medical visit
#     <br>
#     <br> Solutions :-
#     <br> -- confirmation sms or confirmation call for the Patients to confirm the medical appointment
#     <br> -- Obliging the patient to confirm the date regardless of number of reservasion days before appointments
#     <br>
#     <br> conclusion :-
#     <br> -- Almost there is no effect by Gender
# </font>

# ### Q3. Age categories effect on the show status

# In[ ]:


analysis(df, 'Age_cust', 'Show', 'Age')


# <font color='brown'>
# Age Categories
#     <br>-- kids till 10 years
#     <br>-- Childs till 18 years
#     <br>-- Adults till 37 years
#     <br>-- Seniors till 55 years
#     <br>-- Retirement age above 55
#     <br>
# <br>As the above chart and statistics**
#     <br> -- The median age of our sample is "37" and 25% to 75% of the data in age range between 18 to 55 years old
#     <br> -- The Patients in Retirement age have the highest Show percentage of medical appointments with almost 84.4% from all medical appointments, this category almost have 25% form our data
#     <br> -- Other categories have show percentage average 80% 
#     <br>
#     <br> conclusion :-
#     <br> -- There is no big effect of the showing status comparing with Age categories except the Patients in Retirement age which may return to more caring on thier health status
#     
# </font>

# ### Q4. SMS received effect on the show status

# In[ ]:



group = df.groupby('SMS_received').count()['Age']
data_group = pd.DataFrame(group.values, group.keys())
data_group.columns = ['Numbers']

explode = (0.05, 0.05)
colors = ['pink', 'steelblue']
plot = data_group.plot.pie(y='Numbers', figsize=(5, 5), autopct='%1.1f%%', colors=colors, explode=explode)
plt.title('SMS Received\n 0 = Not Received\n 1 = Received')
plt.ylabel(' ')


analysis(df, 'SMS_received', 'Show', 'Age')


# <font color='brown'>
# As the above chart and statistics**
#     <br> -- The majority didn't recieve sms ( as 67% didn't receieved )on the other hand they have percetage of showing more that who didn't recieve, which mean that the sms doesn't effect postitve on the showing percentage 
#     <br> -- We have to revisit the sms criteria and it sent for who and check when the sms sent if it send in the Scheduled day or before the day of reservasion 
#     <br>
#     <br> conclusion :-
#     <br> -- Need to recheck the sms criteria to make this tool more efficient
#     <br> >>>> Q1 sms sent for who
#     <br> >>>> Q2 when it sent
#     <br> >>>> Q3 if it just sms with the reservation or it confirmation or automated sms that the patient has to replay with confirmation or not 
#     
# </font>

# ### Q5. "Scholarship", "Hypertension", "Diabetes","Alcoholism" and "Handicap" effect on the show status

# In[ ]:


def visualization(df, col_name, show_col, col):
    plt.figure(figsize=(6,2))
    visualization_analysis = sns.countplot(x=col_name, hue=df.Show, data=df, palette="Set2")
    visualization_analysis.set_title('{}\nShow / No Show'.format(col_name))
    plt.ylabel('Number of Patient')
    plt.show()


# In[ ]:


visualization(df, 'Scholarship', 'Show', 'Age')
visualization(df, 'Hypertension', 'Show', 'Age')
visualization(df, 'Diabetes', 'Show', 'Age')
visualization(df, 'Alcoholism', 'Show', 'Age')
visualization(df, 'Handicap', 'Show', 'Age')


# <font color='brown'>
# As the above charts and statistics for "Scholarship", "Hypertension", "Diabetes","Alcoholism" and "Handicap"
#     <br> -- There are no high effect on the showing status as all the show percentage and no show percentage almost the same 
# </font>

# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Finally**: 
# <br>We have to put in our considration the sample of data that we make the analysis on it as the sample related with histry from 6 years from 2016, maybe currently their are some updates will effect on our analysis
# <br>
# <br> Through our sample we find:-
# <br>-- we find that the patients make the reservations in the same day have the highest percentage of showing
# <br>-- We need to increase the effectiveness of the sms as currently there is no effict on the showing numbers 
# <br>-- The **Gender** and **Age** have little effect on the showing numbers
# <br>-- The numbers of **Scholarship** very little but till now there is no effect on the showing status, maybe once there is increase in the **Scholarship** between Patients will effect positive on the showing numbers
# <br>-- "Hypertension", "Diabetes","Alcoholism" and "Handicap" have very low effect on the showing status 

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

