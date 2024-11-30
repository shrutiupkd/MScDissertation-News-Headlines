# %% Import necessary libraries
import pandas as pd


# # File path to the Excel file
# file_path = 'monthlyvaccinationrates202106.xlsx'

# # Read the relevant sheets from the Excel file, skipping the first two rows
# df_first_dose = pd.read_excel(file_path, sheet_name='First dose', skiprows=2)  # Reading the "First dose" sheet starting from the third row
# df_second_dose = pd.read_excel(file_path, sheet_name='Second dose', skiprows=2)  # Reading the "Second dose" sheet starting from the third row

# # Filter the data to include only rows where 'Category' or 'SubCategory' columns contain 'London'
# df_first_dose_all = df_first_dose[ 
#     df_first_dose['SubCategoryType'].str.contains('Region', na=False)
# ]

# df_second_dose_all = df_second_dose[
#     df_second_dose['SubCategoryType'].str.contains('Region', na=False)
# ]


# # Sort the data by unique region
# # first_dose_sorted = df_first_dose_all.sort_values(by='SubCategory')
# # second_dose_sorted = df_second_dose_all.sort_values(by='SubCategory')

# # Save the filtered and sorted data to a new Excel file
# output_path = 'final_dataset.xlsx'
# with pd.ExcelWriter(output_path) as writer:
#     df_first_dose_all.to_excel(writer, sheet_name='First dose', index=False)
#     df_second_dose_all.to_excel(writer, sheet_name='Second dose', index=False)

# csv_file_path = 'Evening_Standard.csv'
# additional_data_df = pd.read_csv(csv_file_path)
# print("Filtered and sorted data has been saved to 'final_dataset.xlsx'")



# %% File path to the existing filtered dataset
file_path = 'final_dataset.xlsx'

# %% Read the relevant sheets from the existing Excel file
df_first_dose = pd.read_excel(file_path, sheet_name='First dose')
df_second_dose = pd.read_excel(file_path, sheet_name='Second dose')

# %% Convert the 'Month' column to datetime format
df_first_dose['Month'] = pd.to_datetime(df_first_dose['Month'])
df_second_dose['Month'] = pd.to_datetime(df_second_dose['Month'])

# %% Define a function to calculate the vaccination rate
def calculate_vaccination_rate(df):
    df['Population'] = df['Population'].astype(float)
    df['Vaccinated'] = df['Vaccinated'].astype(float)
    vaccination_rate = df.groupby(['SubCategory', df['Month'].dt.to_period('M')]).apply(
        lambda x: (x['Vaccinated'].sum() / x['Population'].sum()) * 100
    ).reset_index()
    vaccination_rate.columns = ['SubCategory', 'Month', 'Vaccination rate (%)']
    vaccination_rate['Month'] = vaccination_rate['Month'].dt.strftime('%B')
    return vaccination_rate

# %% Calculate the vaccination rate for each region for each month
first_dose_rate = calculate_vaccination_rate(df_first_dose)
second_dose_rate = calculate_vaccination_rate(df_second_dose)

# %% Save the calculated vaccination rates to the existing Excel file
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
    first_dose_rate.to_excel(writer, sheet_name='First Dose Rate', index=False)
    second_dose_rate.to_excel(writer, sheet_name='Second Dose Rate', index=False)

print("Vaccination rates for each region and month have been added to 'final_dataset.xlsx'")


