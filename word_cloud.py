import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# Load your dataset
file_path = 'final_dataset.xlsx'
df_headlines = pd.read_excel(file_path, sheet_name='Headlines')

# Extended stop words list for word cloud
stop_words_extended = [
    "vs", "could", "shows", "two", "top", "back", "amid", "say", "says", "england", "london", "uk", 
    "dont", "just", "much", "more", "after", "got", "go", "get", "been", "make", "made", 
    "come", "came", "take", "took", "give", "gave", "find", "found", "know", "knew", 
    "think", "thought", "see", "saw", "want", "wanted", "use", "used", "try", "tried", 
    "thing", "things", "stuff", "item", "items", "person", "people", "man", "woman", 
    "child", "children", "one", "ones", "place", "places", "time", "times", "day", 
    "days", "year", "years", "good", "bad", "better", "best", "big", "small", "large", 
    "old", "young", "new", "first", "last", "high", "low", "great", "little", "many", 
    "few", "some", "any", "other", "same", "different", "while", "since", "until", 
    "than", "into", "under", "over", "between", "through", "before", "among", "against", 
    "within", "without", "really", "still", "already", "again", "too", "never", 
    "always", "often", "sometimes", "now", "here", "oh", "wow", "hey", "hi", "hello", 
    "ouch", "oops", "ugh", "its", "u", "getting", "where", "even", "up", "down", 
    "going", "lot", "who", "using", "lol", "please", "im", "can't", "those", "didn't", 
    "didnt", "well", "then", "gonna", "isn't", "kya", "ki", "being", "also", "tell"
]

# Combine default NLTK stopwords with the extended list
all_stop_words = set(stopwords.words('english')).union(stop_words_extended)

# Function to generate word cloud for a specific filter
def generate_word_cloud(subcategory, source, title):
    filtered_df = df_headlines[(df_headlines['SubCategory'] == subcategory) & (df_headlines['Source'] == source)]
    
    if filtered_df.empty:
        print(f"No data available for SubCategory: {subcategory}, Source: {source}")
        return
    
    tokens_list = filtered_df['Tokens'].dropna().tolist()

    # Flatten the list of lists of tokens into a single list of words
    words = [word.strip("[]'") for tokens in tokens_list for word in tokens.split(", ") if word.strip("[]'") not in all_stop_words]
    clean_text = ' '.join(words)
    
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(clean_text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()

# Generate word clouds for the specified categories and sources
generate_word_cloud(subcategory='London', source='Evening Standard', title='London - Evening Standard')
generate_word_cloud(subcategory='National-Right', source='Daily Mail', title='National-Right - Daily Mail')
generate_word_cloud(subcategory='National-Left', source='The Guardian', title='National-Left - The Guardian')
