import pandas as pd
import numpy as np

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('HTS-results-1.csv')

# Extract the parameter columns and the RealizedProfits column
params = df.iloc[:, 11:20]
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

# Create a new dataframe to store the recommended parameter ranges
ranges = pd.DataFrame()
for i, param in enumerate(results['Parameter']):
    ranges[param] = [means[i] - 2 * stds[i], means[i] + 2 * stds[i]]

# Print the parameter ranges dataframe
print(ranges)

# Calculate the minimum and maximum RealizedProfits
valid_params = params[(params >= ranges.iloc[:,0]) & (params <= ranges.iloc[:,1])].dropna()
if len(valid_params) > 0:
    min_profit = np.inf
    max_profit = -np.inf
    for i in range(len(valid_params)):
        row = valid_params.iloc[i]
        profits = df.loc[(df.iloc[:, 11] == row[0]) & (df.iloc[:, 12] == row[1]) & (df.iloc[:, 13] == row[2]) & (df.iloc[:, 14] == row[3]) & (df.iloc[:, 15] == row[4]) & (df.iloc[:, 16] == row[5]) & (df.iloc[:, 17] == row[6]) & (df.iloc[:, 18] == row[7]), 'RealizedProfits']
        if len(profits) > 0:
            curr_min = profits.min()
            curr_max = profits.max()
            if curr_min < min_profit:
                min_profit = curr_min
            if curr_max > max_profit:
                max_profit = curr_max

    # Print the minimum and maximum RealizedProfits
    print("Minimum RealizedProfits within recommended parameter ranges:", min_profit)
    print("Maximum RealizedProfits within recommended parameter ranges:", max_profit)

else:
    print("No valid parameter combinations within recommended ranges.")