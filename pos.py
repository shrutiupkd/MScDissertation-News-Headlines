import nltk
import ast
import pandas as pd
from nltk.corpus import stopwords

# Download necessary NLTK resources
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')

# Function to filter out verbs from tokenized words
def remove_verbs(tokens):
    # POS tagging
    pos_tags = nltk.pos_tag(tokens)

    # Filter out verbs (VB, VBD, VBG, VBN, VBP, VBZ are verb tags)
    filtered_tokens = [word for word, pos in pos_tags if not pos.startswith('VB')]

    return filtered_tokens

# Load your dataset
file_path = 'final_dataset.xlsx'
df_headlines = pd.read_excel(file_path, sheet_name='Headlines')

# Define additional stopwords
additional_stopwords = [
    "reveals", "share","show","may","april",  "v", "vs", "could", "shows",
    "two", "top", "back", "amid", "say", "says", "england", "london", "uk", 
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
    "didnt", "well", "then", "gonna", "isn't", "kya", "ki", "being", "also", "tell" , "best",
    "for", "the", "and", "to", "of", "in", "a", "on", "is", "with", "from", "at", "by",
    "an", "be", "this", "it", "as", "that", "are", "your", "has", "was", "which", "or", "you",
    "can", "we", "all", "have", "more", "but", "one", "do", "about", "than", "so", "many",
    "no", "just", "much", "other", "some", "out", "when", "will", "their", "new", "most", "not", "say", "new", "u", "year","top"
]

# Combine with NLTK stopwords
stop_words = set(stopwords.words('english'))
all_stop_words = stop_words.union(additional_stopwords)

# Function to remove stopwords from tokenized words
def remove_stopwords(tokens):
    return [word for word in tokens if word.lower() not in all_stop_words]

# Process each row: filter verbs and remove stopwords
df_headlines['Filtered_Tokens'] = df_headlines['Tokens'].apply(
    lambda x: remove_stopwords(remove_verbs(ast.literal_eval(x)))
)

# Save to new Excel sheet
df_headlines.to_excel("final_dataset_filtered.xlsx", index=False)

print("iit is done")




