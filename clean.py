# import pandas as pd

# def clean_text(text):
#     replacements = {
#         'â€™': "'", 'â€œ': '"', 'â€': '"', 'â€˜': "'", 'â€”': '—', 'â€“': '-',
#         'ã': 'a', 'á': 'a', 'à': 'a', 'ä': 'a', 'é': 'e', 'è': 'e', 'ë': 'e',
#         'í': 'i', 'ì': 'i', 'ï': 'i', 'ó': 'o', 'ò': 'o', 'ö': 'o', 'ú': 'u',
#         'ù': 'u', 'ü': 'u', 'ć': 'c', 'ç': 'c', 'ń': 'n', 'õ': 'o', 'ô': 'o',
#         'œ': 'oe', 'ß': 'ss', 'ÿ': 'y', 'Æ': 'AE', 'æ': 'ae', 'Œ': 'OE',
#         '₹': 'INR', '€': 'EUR', '£': 'GBP', '™': '', '́': '', '̣': '', '—': '-',
#         '–': '-', '…': '...', '’': "'", '‘': "'", '“': '"', '”': '"',
#         '\ufeff': '', '\xa0': ' ', '\u2009': ' ', '\u200b': '', '🚀': '(rocket)',
#         '�': ''
#         # Add or adjust replacements as necessary based on further observations
#     }
#     for old, new in replacements.items():
#         text = text.replace(old, new)
#     return text

# # Load your CSV file
# df  = pd.read_excel('guardian_articles_dec2020_jun2021_combined.xlsx')

# df['Headline'] = df['Headline'].apply(clean_text)

# # Save the cleaned data
# df.to_csv('cleaned_GT_headlines.csv', index=False, encoding='utf-8')
# print("Cleaned headlines have been saved to 'cleaned_daily_mail_headlines.csv'.")


# import pandas as pd

# # Load the data
# df = pd.read_csv('Evening_Standard.csv', encoding='utf-8')

# # Extract unique characters from the headlines
# unique_chars = set(''.join(df['Headline']))
# print(unique_chars)

# df = pd.read_excel('daily_mail_headlines.xlsx')


# # Adjust the date format
# df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d').dt.strftime('%m/%d/%Y')

# # Add 'Source' and 'SubCategory' columns
# df['Source'] = 'Daily Mail'
# df['SubCategory'] = 'National'

# # Save the cleaned data to an Excel file
# df.to_excel('cleaned_daily_mail_headlines.xlsx', index=False, engine='openpyxl')
# print("Cleaned headlines have been saved to 'cleaned_daily_mail_headlines.xlsx'.")


import pandas as pd

# Load the cleaned Daily Mail headlines from the Excel file
cleaned_headlines = df = pd.read_csv('cleaned_GT_headlines.csv', encoding='utf-8')
# Try to load the existing final datasheet; if it doesn't exist, we create a new DataFrame
try:
    final_datasheet = pd.read_excel('final_dataset.xlsx', sheet_name='Headlines', engine='openpyxl')
except FileNotFoundError:
    final_datasheet = pd.DataFrame(columns=['Headline', 'Date', 'Source', 'Subcategory'])
except ValueError:
    # If the sheet does not exist, create a new DataFrame
    final_datasheet = pd.DataFrame(columns=['Headline', 'Date', 'Source', 'Subcategory'])

# Concatenate the cleaned headlines to the final datasheet
final_datasheet = pd.concat([final_datasheet, cleaned_headlines], ignore_index=True)

# Save the updated final datasheet back to the Excel file, specifying the sheet name
with pd.ExcelWriter('final_dataset.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    final_datasheet.to_excel(writer, sheet_name='Headlines', index=False)

print("Updated headlines have been saved to 'final_datasheet.xlsx' in the 'Headlines' sheet.")



import pandas as pd

# Load your dataset
file_path = 'final_dataset.xlsx'
df = pd.read_excel(file_path, sheet_name='Headlines')  # Adjust the sheet name if necessary

# Display the number of rows before cleaning
rows_before = len(df)
print(f"Number of rows before cleaning: {rows_before}")

# Define unwanted entries including the new terms
unwanted_entries = [

    
    "Follow", "DailyMail", "Subscribe", "Home", "News", "Royals", "U.S.", "Sport", "Showbiz", 
    "Femail", "Health", "Science", "Money", "Travel", "Podcasts", "Shopping", "Discounts",
    "TUI", "Booking.com", "ASOS", "Just Eat", "Deliveroo", "boohoo", "Very", "Nike", "Virgin Media",
    "Uber Eats", "Boots", "B&Q", "Amazon", "John Lewis", "Logout", "Login", "Breaking News",
    "Australia", "Video", "You Mag", "Olympics", "Promos", "Rewards", "Mail Shop", "Cars",
    "Property", "Columnists", "Games", "Jobs", "For You", "Back to top", "December", "2020", "2021",
    "Dreamy Summer Escapes", "California is the ultimate playground", "Win An Unforgettable Holiday",
    "January", "February", "March", "April", "June", "My Profile", "Best Buys"
]

# Filter out rows where the "Headline" exactly matches any of the unwanted entries
df_cleaned = df[~df['Headline'].str.strip().isin(unwanted_entries)]

# Convert 'National' in the 'SubCategory' column to 'National-Right'
df_cleaned['SubCategory'] = df_cleaned['SubCategory'].replace('National', 'National-Right')

# Ensure all dates are in the same format (YYYY-MM-DD)
df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Save the cleaned data back to the Excel file, replacing the original sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_cleaned.to_excel(writer, sheet_name='Headlines', index=False)

# Display the number of rows after cleaning
rows_after = len(df_cleaned)
print(f"Number of rows after cleaning: {rows_after}")
