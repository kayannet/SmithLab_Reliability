import pandas as pd
import numpy as np
import os
import re


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
reliability_df = pd.DataFrame(all_video_data).T.sort_index()

# Create all pairwise comparisons of unique values in a list 



# Create a method that outputs mean differences from a pairwise comparison of their behavior duration. 
