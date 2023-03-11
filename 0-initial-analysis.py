import pandas as pd

# Load the CSV file into a Pandas dataframe
df = pd.read_csv('backtests.csv')

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

