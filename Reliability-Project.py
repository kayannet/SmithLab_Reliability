import pandas as pd
import numpy as np
import sys 
import os
import re

#!/usr/bin/env python3

# terminal 
if len(sys.argv) != 3: 
    print("Invalid arguments. Should be in the form: ./file <initial> <initial>")
    sys.exit(1)

initial_1 = sys.argv[1]
initial_2 = sys.argv[2]


# assuming all data is in same folder as this file, with folder name 'csv'
folder_path = 'csv'

# Clean data 
def standardize(x):
    '''
    takes a column of text, and standardizes it to all lowercase, no spaces, no punctuation
    
    '''
    
    # Remove all non-alphanumeric characters (punctuation, spaces, etc.)
    label_cleaned = re.sub(r'[^a-zA-Z]', '', x)
    # Convert to lowercase
    label_standardized = label_cleaned.lower()
    
    if 'self' in label_standardized:
        label_standardized = 'selflicking'
    elif 'groom' in label_standardized:
        label_standardized = 'allogrooming'
    else:
        label_standardized = 'allolicking'
    
    return label_standardized




# Loop through all files in the folder

# dictionary to hold all the data that will be turned into final df
all_video_data = {}
large_df = pd.DataFrame()
all_initials = set()



# loop through each file 
for filename in os.listdir(folder_path):
    
    if filename.endswith('.csv'):  # Check if the file is a CSV
        file_path = os.path.join(folder_path, filename)
        
        # temp dictionary that'll be added to all_video_data at the end of the loop
        curr_vid_data = {}
        
        # extract initials and file name for labeling purposes
        initials = filename.strip('.csv')[-2:]
        video_name = filename.split('_')[0]

        all_initials.add(initials)

    
   
        # turn current csv file into a data frame
        df = pd.read_csv(file_path, header = None)
        
        # standardize the labeling to all lowercase and no spaces/punctuation
        df[0] = df[0].apply(standardize)
        
        # get the total duration of each behavior
        # 0 = behavior name
        # 1 = NaN column
        # 2 = start time
        # 3 = end time
        # 4 = duration
        # 5 = NaN column
        
        d = dict(df.groupby(0).sum()[4])
        
        # rename the keys using initial and behavior name ex) allogrooming_KT
        for key, value in d.items():
            curr_vid_data[f'{key}_{initials}'] = value
        
        
        # first time this video appears,  not yet in large dict (creates new row for the video)
        if video_name not in all_video_data:
            all_video_data[video_name] = curr_vid_data  
            
        # video already in the dictonary, just append the data to existing row
        else:
            all_video_data[video_name].update(curr_vid_data)      
        
        


# Create a dataframe per behavior with column = initials, rows = video and values = total duration of behavior
reliability_df = pd.DataFrame(all_video_data).T.sort_index().fillna(0)

# Create all pairwise comparisons of unique values in a list
initials_list = list(all_initials)
pairwise_comparisons = [(g1, g2) for i, g1 in enumerate(initials_list) for g2 in initials_list[i+1:]]


# Create a method that outputs mean differences from a pairwise comparison of their behavior duration. 

# Filters dataframe with argument comparison 
compare_df = reliability_df.loc[:, reliability_df.columns.str.contains(f'{initial_1}|{initial_2}')]

# Find msec difference and percentage difference
time_differences = {}
percentage_differences = {}

for index, row in compare_df.iterrows(): 
    behaviors = reliability_df.columns.str[:-3].unique()
    time_diff = {}
    percent_diff = {}

    for behavior in behaviors: 
        cols = [col for col in compare_df.columns if behavior in col]

        if len(cols) == 2: 
            val1 = row[cols[0]]
            val2 = row[cols[1]]
            diff = float(abs(val1 - val2))
            avg = (abs(val1 + val2)) / 2 

            if avg != 0: 
                pdiff = float(round((diff / avg) * 100, 2))
            else:
                pdiff = 0
            
            percent_diff[behavior] = pdiff

            time_diff[behavior] = round(diff)
    
time_differences[index] = time_diff
percentage_differences[index] = percent_diff


# printing output to terminal 
print("\n=== Time Differences (ms) ===")
print (f"How to Read: {initial_2} is x msec off from {initial_1}\n")

for video, behavior_diff in time_differences.items():
    print(f"{video} : {behavior_diff}")
    sys.stdout.flush()

print("\n=== Percentage Differences (%) ===")
print (f"How to Read: {initial_2} is x percent off from {initial_1}\n")

for v, p in percentage_differences.items():
    print(f"{v} : {p}")
    sys.stdout.flush()
   

#Exit the program
sys.exit(0)
