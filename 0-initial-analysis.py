import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# # Load the CSV file into a Pandas dataframe
# df = pd.read_csv('HTS-results-1.csv')


# Get all CSV files in the current directory
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

# Show the list of files with their creation date and number of rows
print('Select a CSV file to load:')
for i, file in enumerate(csv_files):
    stats = os.stat(file)
    created_date = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    num_rows = sum(1 for line in open(file)) - 1
    print(f'[{i+1}] {file} ({created_date}, {num_rows} rows)')

# Get user input for the file to load
while True:
    try:
        choice = int(input('\nEnter the number of the file to load: '))
        file_to_load = csv_files[choice-1]
        break
    except (ValueError, IndexError):
        print('Invalid input. Please enter a valid number.')

# Load the chosen CSV file into a Pandas dataframe
df = pd.read_csv(file_to_load)

# Show the list of columns with their index
print('\nSelect the range of columns to analyze:')
for i, col in enumerate(df.columns):
    print(f'[{i}] {col}')

# Get user input for the range of columns to analyze
while True:
    try:
        first_col = int(input('\nEnter the index of the first column: '))
        last_col = int(input('Enter the index of the last column: '))
        break
    except ValueError:
        print('Invalid input. Please enter a valid number.')

# Save the chosen range of columns into variables
FIRST_COL = df.columns[first_col]
LAST_COL = df.columns[last_col]


# Extract the parameter columns and the RealizedProfits column
# params = df.iloc[:, 11:20]
params = df.iloc[:, FIRST_COL:LAST_COL]
profits = df.iloc[:, 6]

# Calculate the mean and standard deviation of each parameter
means = params.mean(axis=0)
stds = params.std(axis=0)

# Calculate the mean and standard deviation of the RealizedProfits column
profit_mean = profits.mean()
profit_std = profits.std()

# Create a new dataframe to store the results
results = pd.DataFrame(columns=['Parameter', 'Mean', 'Std'])

# Add the parameter means and standard deviations to the results dataframe
results['Parameter'] = means.index
results['Mean'] = means.values
results['Std'] = stds.values

# Print the results dataframe
print(results)

# Calculate the correlation between each parameter and the RealizedProfits column
correlations = params.corrwith(profits)

# Create a new dataframe to store the correlations
corr_results = pd.DataFrame(columns=['Parameter', 'Correlation'])

# Add the parameter correlations to the corr_results dataframe
corr_results['Parameter'] = correlations.index
corr_results['Correlation'] = correlations.values

# Print the corr_results dataframe
print(corr_results)

# Calculate the z-scores for each parameter and RealizedProfits column value
z_params = (params - means) / stds
z_profits = (profits - profit_mean) / profit_std

# Calculate the mean and standard deviation of the z-scores for each parameter
z_means = z_params.mean(axis=0)
z_stds = z_params.std(axis=0)

# Create a new dataframe to store the z-score results
z_results = pd.DataFrame(columns=['Parameter', 'Mean z-score', 'Std z-score'])

# Add the z-score means and standard deviations to the z_results dataframe
z_results['Parameter'] = z_means.index
z_results['Mean z-score'] = z_means.values
z_results['Std z-score'] = z_stds.values

# Print the z_results dataframe
print(z_results)

text = """Here's how to interpret the output:

The first dataframe shows the mean and standard deviation of each parameter used in the backtests.

The second dataframe shows the correlation between each parameter and the RealizedProfits column. A positive correlation means that as the parameter value increases, so does the RealizedProfits value. A negative correlation means that as the parameter value increases, the RealizedProfits value decreases.

The third dataframe shows the mean z-score and standard deviation z-score for each parameter. The z-score represents the number of standard deviations away from the mean a value is. A z-score of 0 means that the value is equal to the mean. A positive z-score means that the value is above the mean, and a negative z-score means that the value is below the mean."""

print(text)

# Calculate the recommended parameter ranges based on the z-scores
ranges = []
for i in range(len(z_means)):
    if z_means[i] >= 0:
        lower = max(0, round(means[i] - (2 * stds[i])))
        upper = round(means[i] + (2 * stds[i]))
    else:
        lower = round(means[i] - (2 * stds[i]))
        upper = round(means[i] + (2 * stds[i]))
    ranges.append((lower, upper))

# Create a list of dictionaries to store the recommended parameter ranges
range_data = []

# Loop through each parameter column and calculate the recommended range
for param in params.columns:
    param_mean = means[param]
    param_std = stds[param]
    lower_range = param_mean - param_std
    upper_range = param_mean + param_std
    range_data.append({'Parameter': param, 'Min': lower_range, 'Max': upper_range})

# Create a new dataframe to store the recommended parameter ranges
range_df = pd.DataFrame(range_data)

# Print the range dataframe
print(range_df)


################################


