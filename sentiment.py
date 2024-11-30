import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
# Load your dataset
file_path = 'final_dataset.xlsx'
df = pd.read_excel(file_path, sheet_name='Headlines')  # Adjust the sheet name if necessary

# Text Preprocessing
# 1. Lowercasing
df['Processed_Headline'] = df['Headline'].str.lower()

# 2. Removing punctuation and numbers
df['Processed_Headline'] = df['Processed_Headline'].str.replace('[^\w\s]', '', regex=True)
df['Processed_Headline'] = df['Processed_Headline'].str.replace('\d+', '', regex=True)


# 3. Tokenization
df['Processed_Headline'] = df['Processed_Headline'].astype(str).fillna('')
df['Tokens'] = df['Processed_Headline'].apply(word_tokenize)

# 4. Removing stop words
stop_words = set(stopwords.words('english'))
df['Tokens'] = df['Tokens'].apply(lambda x: [word for word in x if word not in stop_words])

# 5. Lemmatization
lemmatizer = WordNetLemmatizer()
df['Tokens'] = df['Tokens'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

# 6. Rejoining tokens into a single string (for models like BERT)
df['Processed_Headline'] = df['Tokens'].apply(lambda x: ' '.join(x))

vader_analyzer = SentimentIntensityAnalyzer()

def vader_sentiment(text):
    scores = vader_analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    return sentiment, scores['compound']

# Apply VADER sentiment analysis and save both the sentiment and compound score
df['Sentiment'], df['Compound_Score'] = zip(*df['Processed_Headline'].apply(vader_sentiment))

# Display the first few rows to check the results
print(df[['Headline', 'Sentiment', 'Compound_Score']].head())


# Save the updated DataFrame with sentiment results back to the original Excel sheet
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Headlines', index=False)