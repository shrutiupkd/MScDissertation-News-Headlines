import pandas as pd
from collections import Counter
import ast

# Load the Excel file with filtered tokens
file_path = 'final_dataset_filtered.xlsx'
df_headlines = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert the 'Date' column to datetime format
df_headlines['Date'] = pd.to_datetime(df_headlines['Date'], errors='coerce')

# Ensure the 'Month' column exists, and if not, create it
df_headlines['Month'] = df_headlines['Date'].dt.strftime('%B %Y')
# Function to get top keywords from tokenized words, removing stop words
def get_top_keywords(df, sentiment, top_n=5):
    # Filter by sentiment
    sentiment_df = df[df['Sentiment'] == sentiment]

    # Collect all tokenized words
    all_words = []
    for words in sentiment_df['Filtered_Tokens']:
        words_list = ast.literal_eval(words)  # Convert string representation of list back to list
        all_words.extend(words_list)

    # Count word frequencies
    word_counts = Counter(all_words)

    # Get the top N keywords
    top_keywords = word_counts.most_common(top_n)
    return top_keywords

# Function to get top keywords for each sentiment, month, and source
def get_top_keywords_by_source(df):
    # Group by Source, Month, and Sentiment
    grouped = df.groupby(['Source', 'Month', 'Sentiment'])

    # Initialize an empty DataFrame to store the results
    results_df = pd.DataFrame()

    for (source, month, sentiment), group in grouped:
        # Get top keywords for this group
        top_keywords = get_top_keywords(group, sentiment)
        
        # Combine results into a DataFrame
        group_results = pd.DataFrame({
            'Source': [source],
            'Month': [month],
            'Sentiment': [sentiment],
            'Top_Keywords': [', '.join([kw[0] for kw in top_keywords])],
            'Frequency': [sum([kw[1] for kw in top_keywords])]
        })

        # Append to the main results DataFrame
        results_df = pd.concat([results_df, group_results], ignore_index=True)
    
    return results_df

# Calculate top keywords by source, month, and sentiment
top_keywords_by_source_df = get_top_keywords_by_source(df_headlines)

# Save the results to the existing Excel sheet, overwriting the "Top Keywords by Source" sheet
with pd.ExcelWriter('final_dataset.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    top_keywords_by_source_df.to_excel(writer, sheet_name='Top Keywords by Source', index=False)

print("Top keywords by source, month, and sentiment have been saved to the 'Top Keywords by Source' sheet.")
