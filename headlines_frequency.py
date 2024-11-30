# import pandas as pd

# # File path to the existing dataset
# file_path = 'final_dataset.xlsx'

# # Load the relevant sheet (assuming the sheet name is 'Headlines')
# df_headlines = pd.read_excel(file_path, sheet_name='Headlines')

# # Convert the 'Date' column to datetime format
# df_headlines['Date'] = pd.to_datetime(df_headlines['Date'])

# # Extract the month and year from the 'Date' column
# df_headlines['Month'] = df_headlines['Date'].dt.strftime('%B')
# df_headlines['Year'] = df_headlines['Date'].dt.year

# # Calculate the number of headlines published every month
# monthly_headlines = df_headlines.groupby(['Year', 'Month', 'SubCategory']).size().reset_index(name='Total Headlines')

# # Calculate the number of vaccine-related headlines
# df_headlines['Vaccine Related'] = df_headlines['Headline'].str.contains('vaccine', case=False, na=False)
# monthly_vaccine_headlines = df_headlines[df_headlines['Vaccine Related']].groupby(['Year', 'Month', 'SubCategory']).size().reset_index(name='Vaccine Headlines')

# # Merge the two dataframes to get a combined view
# monthly_data = pd.merge(monthly_headlines, monthly_vaccine_headlines, on=['Year', 'Month', 'SubCategory'], how='left')
# monthly_data['Vaccine Headlines'] = monthly_data['Vaccine Headlines'].fillna(0)

# # Calculate the frequency of vaccine-related articles and multiply by 100
# monthly_data['Vaccine Frequency (%)'] = (monthly_data['Vaccine Headlines'] / monthly_data['Total Headlines']) * 100

# # Save the information to a new sheet named 'Headline Frequency'
# with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
#     monthly_data.to_excel(writer, sheet_name='Headline Frequency', index=False)

# print("Headline frequency data has been added to 'final_dataset.xlsx'")


import pandas as pd

# File path to the existing dataset
file_path = 'final_dataset.xlsx'

# Load the relevant sheet (assuming the sheet name is 'Headlines')
df_headlines = pd.read_excel(file_path, sheet_name='Headlines')

# Convert the 'Date' column to datetime format
df_headlines['Date'] = pd.to_datetime(df_headlines['Date'])

# Extract the month and year from the 'Date' column
df_headlines['Month'] = df_headlines['Date'].dt.strftime('%B')
df_headlines['Year'] = df_headlines['Date'].dt.year

# Calculate the number of headlines published every month for each SubCategory
monthly_headlines = df_headlines.groupby(['Year', 'Month', 'SubCategory']).size().reset_index(name='Total Headlines')

# Calculate the number of vaccine-related headlines
df_headlines['Vaccine Related'] = df_headlines['Headline'].str.contains('vaccine', case=False, na=False)
monthly_vaccine_headlines = df_headlines[df_headlines['Vaccine Related']].groupby(['Year', 'Month', 'SubCategory']).size().reset_index(name='Vaccine Headlines')

# Merge the two dataframes to get a combined view
monthly_data = pd.merge(monthly_headlines, monthly_vaccine_headlines, on=['Year', 'Month', 'SubCategory'], how='left')
monthly_data['Vaccine Headlines'] = monthly_data['Vaccine Headlines'].fillna(0)

# Calculate the frequency of vaccine-related articles and multiply by 100
monthly_data['Vaccine Frequency (%)'] = (monthly_data['Vaccine Headlines'] / monthly_data['Total Headlines']) * 100

# Add the Source column, if needed
# monthly_data['Source'] = 'Daily Mail'  # Assuming source is static as 'Daily Mail'

with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    monthly_data.to_excel(writer, sheet_name='Headline Frequency', index=False)

print("Headline frequency data has been added to 'final_dataset.xlsx' under the 'Headline Frequency' sheet.")
