import pandas as pd

# Load the Excel file
file_path = 'final_dataset.xlsx'
df_headlines = pd.read_excel(file_path, sheet_name='Headlines')

# Define the keywords to search for in the headlines
keywords = ['covid', 'vaccine', 'vaccination', 'coronavirus', 'covid-19']

# Function to filter headlines containing the keywords
def filter_headlines_by_keywords(df, keywords):
    # Create a regex pattern to match any of the keywords
    pattern = '|'.join(keywords)
    
    # Filter the DataFrame to include only rows where the headline contains any of the keywords
    filtered_df = df[df['Headline'].str.contains(pattern, case=False, na=False)]
    
    return filtered_df

# Apply the filter to the dataset
covid_related_headlines = filter_headlines_by_keywords(df_headlines, keywords)

# Save the filtered headlines to a new Excel sheet or CSV file
covid_related_headlines.to_excel('covid_related_headlines.xlsx', index=False)
# or save as CSV
# covid_related_headlines.to_csv('covid_related_headlines.csv', index=False)

print(f"Extracted {len(covid_related_headlines)} COVID-related headlines.")
