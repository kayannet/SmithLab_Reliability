#Create one .csv that contains total duration of each behavior for each video in the current directory
import os
import pandas as pd
import numpy as np

def process_csv_files(directory):
    behavior_durations_per_video = {}

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)

            # Dictionary to hold total duration for each behavior in the current file
            behavior_total_duration = {}

            # Assuming the columns are: [Behavior, Unknown, Start Time, End Time, Duration]
            for _, row in df.iterrows():
                behavior = row[0]
                duration = row[4]

                # Update the total duration for each behavior in the current video
                if behavior not in behavior_total_duration:
                    behavior_total_duration[behavior] = 0
                behavior_total_duration[behavior] += duration

            # Store the total durations for this video in the main dictionary
            # Use the filename (without extension) as the key
            behavior_durations_per_video[filename] = behavior_total_duration

    # Create a DataFrame to hold the summary of each video and behavior durations
    all_behaviors = set()
    for behavior_durations in behavior_durations_per_video.values():
        all_behaviors.update(behavior_durations.keys())
    
    all_behaviors = sorted(all_behaviors)  # Sort the behaviors for consistency

    # Create a list of dictionaries where each dictionary contains the video and its behavior durations
    summary_data = []
    for video, behavior_durations in behavior_durations_per_video.items():
        row_data = {'Video': video}
        for behavior in all_behaviors:
            row_data[behavior] = behavior_durations.get(behavior, 0)  # Fill with 0 if behavior not present
        summary_data.append(row_data)

    # Create the DataFrame from the summary data
    summary_df = pd.DataFrame(summary_data)

    # Save the summary DataFrame to a CSV file
    summary_csv = os.path.join(directory, 'video_behavior_durations.csv')
    summary_df.to_csv(summary_csv, index=False)

    print(f"Video behavior durations saved to {summary_csv}")

# Get the current working directory
directory_path = os.getcwd()

process_csv_files(directory_path)
