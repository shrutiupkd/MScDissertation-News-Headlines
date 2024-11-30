import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import base64
from nltk.corpus import stopwords
import ast




# Load data 
file_path = 'final_dataset.xlsx'
df_first_dose = pd.read_excel(file_path, sheet_name='First dose')
df_second_dose = pd.read_excel(file_path, sheet_name='Second dose')
df_headline_frequency = pd.read_excel(file_path, sheet_name='Headline Frequency')
df_first_dose_rate = pd.read_excel(file_path, sheet_name='First Dose Rate')

df_second_dose_rate = pd.read_excel(file_path, sheet_name='Second Dose Rate')
df_headlines = pd.read_excel(file_path, sheet_name='Headlines')
df_headlines.dropna(inplace=True)
df_keywords = pd.read_excel(file_path, sheet_name='Keywords')
df_top_keywords = pd.read_excel(file_path, sheet_name='Top Keywords by Source')
file_path_2 = 'covid_related_headlines.xlsx'
df_covid_headlines = pd.read_excel(file_path_2)
df_covid_headlines['Date'] = pd.to_datetime(df_covid_headlines['Date'], errors='coerce')
df_covid_headlines['Month'] = df_covid_headlines['Date'].dt.strftime('%B %Y')
df_covid_headlines_grouped = df_covid_headlines.groupby(['Month', 'SubCategory', 'Sentiment']).size().reset_index(name='Frequency')
df_total_headlines = df_covid_headlines.groupby(['Month', 'SubCategory']).size().reset_index(name='Total_Headlines')
df_covid_headlines_grouped = pd.merge(df_covid_headlines_grouped, df_total_headlines, on=['Month', 'SubCategory'])
df_covid_headlines_grouped['Normalized_Frequency'] = df_covid_headlines_grouped['Frequency'] / df_covid_headlines_grouped['Total_Headlines']

# Pre-process data
df_first_dose_rate['Month'] = df_first_dose_rate['Month'].apply(lambda x: f"{x} 2020" if x == 'December' else f"{x} 2021")
df_second_dose_rate['Month'] = df_second_dose_rate['Month'].apply(lambda x: f"{x} 2020" if x == 'December' else f"{x} 2021")
df_headline_frequency = df_headline_frequency[~df_headline_frequency['Month'].str.contains('December', na=False)]
df_first_dose_rate = df_first_dose_rate[~df_first_dose_rate['Month'].str.contains('December', na=False)]
df_second_dose_rate = df_second_dose_rate[~df_second_dose_rate['Month'].str.contains('December', na=False)]
df_first_dose['Dose'] = 'First'
df_second_dose['Dose'] = 'Second'
vaccination_data = pd.concat([df_first_dose, df_second_dose])
vaccination_data['Month'] = pd.to_datetime(vaccination_data['Month'], errors='coerce')
df_headlines['Date'] = pd.to_datetime(df_headlines['Date'], errors='coerce')
df_headlines['Month'] = df_headlines['Date'].dt.strftime('%B %Y')


# Extract unique options only once
month_year_options = vaccination_data['Month'].dt.strftime('%B %Y').unique()
headline_subcategory_options = df_headline_frequency['SubCategory'].unique()
first_dose_subcategory_options = df_first_dose_rate['SubCategory'].unique()
second_dose_subcategory_options = df_second_dose_rate['SubCategory'].unique()
month_options = sorted(df_top_keywords['Month'].unique())

custom_colors = {
    'December': '#1f77b4',
    'January ': '#8c564b',
    'February ': '#e377c2',
    'March ': '#d62728',
    'April ': '#9467bd',
    'May ': '#ff7f0e',
    'June ': '#2ca02c'
}

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

stop_words = set(stopwords.words('english'))
all_stop_words = stop_words.union(stop_words_extended)
default_location = 'London'  

#for Wordcloud
def encode_image(image_file):
    with open(image_file, 'rb') as file:
        encoded_image = base64.b64encode(file.read()).decode('utf-8')
    return f'data:image/png;base64,{encoded_image}'

img_london = encode_image('Figure_1.png')
img_national_right = encode_image('Figure_2.png')
img_national_left = encode_image('Figure_3.png')


#Initialise Dash app
app = dash.Dash(__name__)
app.title = "Dissertation"

#App layout
app.layout = html.Div([

#Header
    html.H1("Coronavirus News Dashboard UK", className="header-title"),   
    
#DropDown and Graph for Bar Chart Vaccination Trend 
    html.Div([
        html.Div([
            html.Label("Type of Dose"),
            dcc.Dropdown(
                id='dose-dropdown',
                options=[{'label': dose, 'value': dose} for dose in vaccination_data['Dose'].unique()],
                value='First'
            ),
            html.Label("Category Type"),
            dcc.Dropdown(
                id='categoryType-dropdown',
                options=[{'label': cat, 'value': cat} for cat in vaccination_data['CategoryType'].unique()],
                value=vaccination_data['CategoryType'].unique()[0]
            ),
            html.Label("Category"),
            dcc.Dropdown(id='category-dropdown', options=[], value=None),

            html.Label("Location"),
            dcc.Dropdown(id='bar-subcategory-dropdown', options=[], value=None),

            html.Label("Select Months"),
            html.Div([
                dcc.Checklist(
                    id='month-checklist',
                    options=[{'label': month, 'value': month} for month in month_year_options],
                    value=[month_year_options[0]],
                    inline=True
                ),
            ], className="month-checkboxes"),
        ], className="filter-card"),
        html.Div([dcc.Graph(id='vaccination-trends')
    ], className="graph-card"),
    ], className="content"),

#DropDown and Graph for Bar Chart and line chart Vaccination and population
    html.Div([
        html.Div([
            html.Label("Type of Dose"),
            dcc.Dropdown(
                id='linechart-dose-dropdown',
                options=[{'label': dose, 'value': dose} for dose in vaccination_data['Dose'].unique()],
                value='First',
                className='linechart-dropdown'
            ),
            html.Label("Category Type "),
            dcc.Dropdown(
                id='linechart-categoryType-dropdown',
                options=[{'label': cat, 'value': cat} for cat in vaccination_data['CategoryType'].unique()],
                value=vaccination_data['CategoryType'].unique()[0],
                className='linechart-dropdown'
            ),
            html.Label("Location"),
            dcc.Dropdown(
                id='linechart-subcategory-dropdown',
                options=[], value=None, className='linechart-dropdown'
            ),
        ], className="linechart-filter-card"),
        html.Div([
            dcc.RadioItems(
                id='chart-type-radio',
                options=[{'label': 'Line Chart', 'value': 'line'}, {'label': 'Bar Chart', 'value': 'bar'}],
                value='line',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='vaccination-rate-trends')
        ], className="graph-card"),
    ], className="content"),
    html.Div([
        html.Div([
            html.Label("Location for Headline Frequency"),
            dcc.Dropdown(
                id='headline-subcategory-dropdown',
                options=[{'label': loc, 'value': loc} for loc in headline_subcategory_options],
                value=default_location
            ),
            dcc.Graph(id='headline-frequency-pie')
        ], className="pie-chart"),
        html.Div([
            html.Label("Location for First Dose Rate"),
            dcc.Dropdown(
                id='first-dose-subcategory-dropdown',
                options=[{'label': loc, 'value': loc} for loc in first_dose_subcategory_options],
                value=default_location
            ),
            dcc.Graph(id='first-dose-rate-pie')
        ], className="pie-chart"),
        html.Div([
            html.Label("Location for Second Dose Rate"),
            dcc.Dropdown(
                id='second-dose-subcategory-dropdown',
                options=[{'label': loc, 'value': loc} for loc in second_dose_subcategory_options],
                value=default_location
            ),
            dcc.Graph(id='second-dose-rate-pie')
        ], className="pie-chart"),
    ], className="content"),

#Wordcloud For All headlines 
 html.Div([
        html.Div([
            html.H3("London - Evening Standard"),
            html.Img(src=img_london)
        ], className="word-cloud"),

        html.Div([
            html.H3("National-Right - Daily Mail"),
            html.Img(src=img_national_right)
        ], className="word-cloud"),

        html.Div([
            html.H3("National-Left - The Guardian"),
            html.Img(src=img_national_left)
        ], className="word-cloud"),
        
    ], className="content"),

#Sentiment Trend for all the headlines   
    html.Div([
    html.Div([
        html.H3("Sentiment Analysis Over Time - Daily Mail"),
        dcc.Graph(id='sentiment-trend-daily-mail')
    ]),
    
    html.Div([
        html.H3("Sentiment Analysis Over Time - Evening Standard"),
        dcc.Graph(id='sentiment-trend-evening-standard')
    ]),
    
    html.Div([
        html.H3("Sentiment Analysis Over Time - The Guardian"),
        dcc.Graph(id='sentiment-trend-the-guardian')
    ]),
], className = " sentiment-trend"),

#Sentiment pie for all the headlines
    html.Div ([
    html.Div([
        html.H2("London Sentiments"),
        dcc.Dropdown(
            id='month-dropdown-london',
            options=[{'label': month, 'value': month} for month in ['All'] + sorted(df_headlines['Month'].unique())],
            value='All',
            placeholder="Select a month "
        ), dcc.Graph(id='pie-london'),
        html.Div(id='pie-london-info'),
        
    ], className = "sentiment-pie" ),
    html.Div([
        html.H2("National Right Sentiments"),
        dcc.Dropdown(
            id='month-dropdown-national-right',
            options=[{'label': month, 'value': month} for month in ['All'] + sorted(df_headlines['Month'].unique())],
            value='All',
            placeholder="Select a month "
        ),dcc.Graph(id='pie-national-right'),
        html.Div(id='pie-national-right-info'),
        
    ], className = "sentiment-pie"),

        html.Div([
        html.H2("National Left Sentiments"),
        dcc.Dropdown(
            id='month-dropdown-national-left',
            options=[{'label': month, 'value': month} for month in ['All'] + sorted(df_headlines['Month'].unique())],
            value='All',
            placeholder="Select a month "
        ),dcc.Graph(id='pie-national-left'),
         html.Div(id='pie-national-left-info'),
        
    ], className = "sentiment-pie"),
    ], className = "content"),

#Top five keywords stacked bar chart by selecting source over time for all the headlines 
html.Div([
    html.Div([
        html.H2("Top Keywords Visualisation by Source"),
        html.Label("Select News Source"),
        dcc.Dropdown(
            id='source-dropdown',
            options=[{'label': source, 'value': source} for source in df_top_keywords['Source'].unique()],
            value=df_top_keywords['Source'].unique()[0]
        )
    ], className="dropdown-container"),

    
    dcc.Graph(id='stacked-bar-chart')
], className="keyword-visualization"),

#Top five keywords stacked bar chart by selecting month over source for all the headlines 
html.Div([
        html.H2("Top Keywords Visualisation by Month "),

        html.Div([
            html.Label("Select Month"),
            dcc.Dropdown(
                id='month-dropdown',
                options=[{'label': month, 'value': month} for month in month_options],
                value=month_options[0],
                className="dropdown"
            )
        ], className="dropdown-container"),

        dcc.Graph(id='keyword-frequency-bar-chart')
    ], className="keyword-visualization"),

#ONLY COVID RELATED HEADLINES 

#Sentiment trend analysis with date range picker for covid related headlines by selecting source 
html.Div([
    html.H1("COVID-19 Headlines Sentiment Analysis", style={'textAlign': 'center'}),
    html.Div([
    html.H3("Sentiment Over Time"),
    html.Div([
        html.Div([
            html.Label("Select Date Range for Time Series:"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=df_covid_headlines['Date'].min(),
                end_date=df_covid_headlines['Date'].max(),
                display_format='YYYY-MM-DD',
                start_date_placeholder_text='YYYY-MM-DD'
            ),
        ], className='inline-elements'),

        html.Div([
            html.Label("Select News Source for Time Series:"),
            dcc.Dropdown(
                id='source-dropdown-timeseries',
                options=[{'label': source, 'value': source} for source in df_covid_headlines['Source'].unique()],
                value=df_covid_headlines['Source'].unique()[0] 
            ),
        ], className='inline-elements'),
    ], className='inline-elements'),
    
    dcc.Graph(id='sentiment-time-series')
], className="covid-senti"),

#Sentiment distribution bar graph by selecting sentiment only covid related headlines
    html.Div([
        html.H3("Sentiment Distribution Across All Sources (Normalized)"),
        html.Label("Select Sentiment for Sentiment Distribution:"),
        dcc.Dropdown(
            id='sentiment-dropdown-distribution',
            options=[{'label': sentiment, 'value': sentiment} for sentiment in df_covid_headlines['Sentiment'].unique()],
            value='Positive'  
        ), 
        dcc.Graph(id='sentiment-distribution')
    ], className = "covid-distribution"),

#Top Keywords by selecting news source covid related headlines 
    html.Div([
        html.H3("Top Keywords by Sentiment"),
        html.Label("Select News Source for Top Keywords:"),
        dcc.Dropdown(
            id='source-dropdown-keywords',
            options=[{'label': source, 'value': source} for source in df_covid_headlines['Source'].unique()],
            value=df_covid_headlines['Source'].unique()[0]  
        ), dcc.Graph(id='top-keywords')
    ], className = "covid-keyword"),  
],),

#Dropdown and Graph for Vaccine Rate and Sentiment Trend
    html.Div([
        html.Div([
            html.Label("Select Dose Type"),
            dcc.Dropdown(
                id='dose-type-dropdown',
                options=[
                    {'label': 'First Dose', 'value': 'First Dose'},
                    {'label': 'Second Dose', 'value': 'Second Dose'}
                ],
                value='First Dose',
                className="dropdown"
            ),
            html.Label("Select Sentiment"),
            dcc.Dropdown(
                id='sentiment-type-dropdown',
                options=[
                    {'label': 'Positive', 'value': 'Positive'},
                    {'label': 'Negative', 'value': 'Negative'},
                    {'label': 'Neutral', 'value': 'Neutral'}
                ],
                value='Positive',
                className="dropdown"
            ),
            html.Label("Select SubCategory"),
            dcc.Dropdown(
                id='subcategory-dropdown',
                options=[{'label': subcat, 'value': subcat} for subcat in df_first_dose_rate['SubCategory'].unique()],
                value=df_first_dose_rate['SubCategory'].unique()[0],
                className="dropdown"
            )
        ], className="filter-card"),

        html.Div([
            dcc.Graph(id='vaccine-sentiment-trend')
        ], className="graph-card"),
    ], className="content"),

#Footer
    html.Footer([
        html.P("Figures based on first dose of vaccine administered between 08 Dec 2020 and 30 Jun 2021 for residents in England who could be linked to the 2011 Census and General Practice Extraction Service Data for Pandemic Planning and Research.", className="footer-text")
    ], className="footer")
], className="container")



# Callback for dropdowns updating other dropdowns
@app.callback(
    [Output('category-dropdown', 'options'), Output('category-dropdown', 'value')],
    Input('categoryType-dropdown', 'value')
)
def update_category_options(selected_categoryType):
    filtered_df = vaccination_data[vaccination_data['CategoryType'] == selected_categoryType]
    categories = filtered_df['Category'].unique()
    
    # Use len() to check if categories has elements
    return [{'label': subcat, 'value': subcat} for subcat in categories], categories[0] if len(categories) > 0 else None

@app.callback(
    [Output('bar-subcategory-dropdown', 'options'), Output('bar-subcategory-dropdown', 'value')],
    Input('category-dropdown', 'value')
)
def update_subcategory_options(selected_category):
    filtered_df = vaccination_data[vaccination_data['Category'] == selected_category]
    subcategories = filtered_df['SubCategory'].unique() if 'SubCategory' in filtered_df.columns else []
    
    # Use len() to check if subcategories has elements
    return [{'label': subcat, 'value': subcat} for subcat in subcategories], subcategories[0] if len(subcategories) > 0 else None


@app.callback(
    [Output('linechart-subcategory-dropdown', 'options'), Output('linechart-subcategory-dropdown', 'value')],
    Input('linechart-categoryType-dropdown', 'value')
)
def update_linechart_subcategory_options(selected_rate_categoryType):
    filtered_df = vaccination_data[vaccination_data['CategoryType'] == selected_rate_categoryType]
    subcategories = filtered_df['SubCategory'].unique() if 'SubCategory' in filtered_df.columns else []
    
    # Check if the array is empty by using the `len()` function, which works well with lists and arrays
    return [{'label': subcat, 'value': subcat} for subcat in subcategories], subcategories[0] if len(subcategories) > 0 else None


# Callback for vaccination trends graph
@app.callback(
    Output('vaccination-trends', 'figure'),
    [Input('dose-dropdown', 'value'), Input('categoryType-dropdown', 'value'), Input('category-dropdown', 'value'),
     Input('bar-subcategory-dropdown', 'value'), Input('month-checklist', 'value')]
)
def update_graph(selected_dose, selected_categoryType, selected_category, selected_subcategory, selected_months):
    selected_months_dt = pd.to_datetime(selected_months, format='%B %Y')
    filtered_data = vaccination_data[
        (vaccination_data['Dose'] == selected_dose) &
        (vaccination_data['CategoryType'] == selected_categoryType) &
        (vaccination_data['Category'] == selected_category) &
        (vaccination_data['SubCategory'] == selected_subcategory) &
        (vaccination_data['Month'].isin(selected_months_dt))
    ].copy()
    
    if filtered_data.empty:
        return px.bar(title="No data available for the selected filters")
    
    filtered_data['Month'] = filtered_data['Month'].dt.strftime('%B %Y')
    fig_vacc_trends = px.bar(
        filtered_data, 
        x='Population', 
        y='Vaccinated', 
        color='Month',
        title=f'{selected_dose} Dose Vaccinations for {selected_category} ({selected_categoryType}) in {selected_subcategory}',
        labels={'Vaccinated': 'Number of Vaccinated', 'Population': 'Population'},
        barmode='group'
    )
    fig_vacc_trends.update_layout(template="plotly_white")
    return fig_vacc_trends

# Callback for vaccination rate trends graph
@app.callback(
    Output('vaccination-rate-trends', 'figure'),
    [Input('linechart-dose-dropdown', 'value'), Input('linechart-categoryType-dropdown', 'value'),
     Input('linechart-subcategory-dropdown', 'value'), Input('chart-type-radio', 'value')]
)
def update_rate_graph(selected_dose, selected_rate_categoryType, selected_subcategory, chart_type):
    filtered_rate_data = vaccination_data[
        (vaccination_data['Dose'] == selected_dose) &
        (vaccination_data['CategoryType'] == selected_rate_categoryType) &
        (vaccination_data['SubCategory'] == selected_subcategory)
    ].copy()
    
    if filtered_rate_data.empty:
        return px.line(title="No data available for the selected filters") if chart_type == 'line' else px.bar(title="No data available for the selected filters")

    fig_rate_trends = (px.line if chart_type == 'line' else px.bar)(
        filtered_rate_data, 
        x='Month', 
        y='Vaccination rate (%)', 
        color='Category',
        labels={'Month': 'Month', 'Vaccination rate (%)': 'Vaccination rate (%)'}
    )
    fig_rate_trends.update_layout(template="plotly_white", 
                                  title=f'Vaccination Rate for {selected_dose} Dose Vaccinations of {selected_rate_categoryType} in {selected_subcategory}')
    return fig_rate_trends

# Callback for pie charts
@app.callback(
    [Output('headline-frequency-pie', 'figure'), Output('first-dose-rate-pie', 'figure'),
     Output('second-dose-rate-pie', 'figure')],
    [Input('headline-subcategory-dropdown', 'value'), Input('first-dose-subcategory-dropdown', 'value'),
     Input('second-dose-subcategory-dropdown', 'value')]
)
def update_pie_charts(selected_headline_subcategory, selected_first_dose_subcategory, selected_second_dose_subcategory):
    headline_pie = px.pie(
        df_headline_frequency[df_headline_frequency['SubCategory'] == selected_headline_subcategory],
        names='Month',
        values='Vaccine Headlines',
        title='Headline Frequency',
        color_discrete_map=custom_colors,
        hover_data=['Total Headlines']
    )
    
    first_dose_rate_pie = px.pie(
        df_first_dose_rate[df_first_dose_rate['SubCategory'] == selected_first_dose_subcategory],
        names='Month',
        values='Vaccination rate (%)',
        title='First Dose Vaccine Rate',
        color='Month',
        color_discrete_map=custom_colors
    )

    second_dose_rate_pie = px.pie(
        df_second_dose_rate[df_second_dose_rate['SubCategory'] == selected_second_dose_subcategory],
        names='Month',
        values='Vaccination rate (%)',
        title='Second Dose Vaccine Rate',
        color='Month',
        color_discrete_map=custom_colors
    )

    return headline_pie, first_dose_rate_pie, second_dose_rate_pie



# Callback for Daily Mail sentiment trend chart
@app.callback(
    Output('sentiment-trend-daily-mail', 'figure'),
    [Input('sentiment-trend-daily-mail', 'id')]
)
def update_graph_daily_mail(_):
    filtered_df = df_headlines[df_headlines['Source'] == 'Daily Mail']
    return generate_sentiment_figure(filtered_df, 'Daily Mail')

# Callback for Evening Standard sentiment trend chart
@app.callback(
    Output('sentiment-trend-evening-standard', 'figure'),
    [Input('sentiment-trend-evening-standard', 'id')]
)
def update_graph_evening_standard(_):
    filtered_df = df_headlines[df_headlines['Source'] == 'Evening Standard']
    return generate_sentiment_figure(filtered_df, 'Evening Standard')

# Callback for The Guardian sentiment trend chart
@app.callback(
    Output('sentiment-trend-the-guardian', 'figure'),
    [Input('sentiment-trend-the-guardian', 'id')]
)
def update_graph_the_guardian(_):
    filtered_df = df_headlines[df_headlines['Source'] == 'The Guardian']
    return generate_sentiment_figure(filtered_df, 'The Guardian')

# Function to generate the sentiment figure
def generate_sentiment_figure(filtered_df, source_name):
    # Group by date and sentiment
    sentiment_counts = filtered_df.groupby(['Date', 'Sentiment']).size().reset_index(name='Count')

    # Calculate total number of headlines per day
    total_counts = sentiment_counts.groupby('Date')['Count'].sum().reset_index(name='Total_Count')

    # Merge total counts back into sentiment_counts to calculate normalized counts
    sentiment_counts = sentiment_counts.merge(total_counts, on='Date')

    # Normalize the sentiment counts by dividing by the total number of headlines per day
    sentiment_counts['Normalized_Count'] = sentiment_counts['Count'] / sentiment_counts['Total_Count']

    # Create the sentiment trend line chart using normalized counts
    sentiment_trend_figure = px.line(sentiment_counts, x='Date', y='Normalized_Count', color='Sentiment',
                                     title=f'Sentiment Analysis of Headlines Over Time ({source_name}) ',
                                     labels={'Normalized_Count': 'Proportion of Headlines', 'Date': 'Date'})
    sentiment_trend_figure.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', font=dict(color='black')
    )
    
    return sentiment_trend_figure



# Callback for London sentiment pie chart
@app.callback(
    [Output('pie-london', 'figure'), Output('pie-london-info', 'children')],
    Input('month-dropdown-london', 'value')
)
def update_london_pie(selected_month):
    fig, sentiments_count = generate_sentiment_pie_chart(df_headlines, 'London', selected_month)
    info_text = generate_info_text(sentiments_count)
    return fig, info_text

# Callback for National Right sentiment pie chart
@app.callback(
    [Output('pie-national-right', 'figure'), Output('pie-national-right-info', 'children')],
    Input('month-dropdown-national-right', 'value')
)
def update_national_right_pie(selected_month):
    fig, sentiments_count = generate_sentiment_pie_chart(df_headlines, 'National-Right', selected_month)
    info_text = generate_info_text(sentiments_count)
    return fig, info_text
# Callback for National Left sentiment pie chart
@app.callback(
    [Output('pie-national-left', 'figure'), Output('pie-national-left-info', 'children')],
    Input('month-dropdown-national-left', 'value')
)
def update_national_left_pie(selected_month):
    fig, sentiments_count = generate_sentiment_pie_chart(df_headlines, 'National-Left', selected_month)
    info_text = generate_info_text(sentiments_count)
    return fig, info_text


# Utility function to generate info text
def generate_info_text(sentiments_count):
    return (f"Positive: {sentiments_count.get('Positive', 0)}, "
            f"Negative: {sentiments_count.get('Negative', 0)}, "
            f"Neutral: {sentiments_count.get('Neutral', 0)}")
def generate_sentiment_pie_chart(df, subcategory, selected_month):
    # Filter by subcategory and selected month
    if selected_month == 'All':
        df_filtered = df[df['SubCategory'] == subcategory]
    else:
        df_filtered = df[(df['SubCategory'] == subcategory) & (df['Month'] == selected_month)]
    
    # If no data is found for the selected month, create an empty pie chart
    if df_filtered.empty:
        fig = px.pie(names=['No Data'], values=[1], title=f'No data available for {subcategory} in {selected_month}')
        sentiments_count = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    else:
        # Generate pie chart with available sentiment data
        fig = px.pie(df_filtered, names='Sentiment', title=f'Sentiments for {subcategory} in {selected_month}')
        sentiments_count = df_filtered['Sentiment'].value_counts().to_dict()

    return fig, sentiments_count


@app.callback(
    Output('stacked-bar-chart', 'figure'),
    [Input('source-dropdown', 'value')]
)
def update_chart(selected_source):
    # Filter data based on the selected source
    filtered_df = df_top_keywords[df_top_keywords['Source'] == selected_source]

    # Create a stacked bar chart
    fig = px.bar(
        filtered_df, 
        x='Month', 
        y='Frequency', 
        color='Sentiment',
        text='Top_Keywords',
        title=f"Top Keywords for {selected_source} by Month and Sentiment",
        labels={'Frequency': 'Keyword Frequency'},
        barmode='stack'
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Frequency',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        hovermode='x',
        height=600
    )

    return fig

@app.callback(
    Output('keyword-frequency-bar-chart', 'figure'),
    [Input('month-dropdown', 'value')]
)
def update_keyword_frequency_chart(selected_month):
    filtered_df = df_top_keywords[df_top_keywords['Month'] == selected_month]

    if filtered_df.empty:
        return go.Figure().add_annotation(
            text="No data available for the selected filters",
            showarrow=False
        )

    fig = px.bar(
        filtered_df,
        x='Source',
        y='Frequency',
        color='Sentiment',
        text='Top_Keywords',
        title=f"Keyword Frequency in {selected_month} by Source",
        labels={'Frequency': 'Keyword Frequency'},
        barmode='group'
    )

    fig.update_layout(
        xaxis_title='Source',
        yaxis_title='Frequency',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        hovermode='x',
        height=600
    )

    return fig

# Callback to update the sentiment time series graph
@app.callback(
    Output('sentiment-time-series', 'figure'),
    [Input('source-dropdown-timeseries', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_time_series(selected_source, start_date, end_date):
    # Filter the data by source and date range
    filtered_df = df_covid_headlines[(df_covid_headlines['Source'] == selected_source) &
                                     (df_covid_headlines['Date'] >= start_date) &
                                     (df_covid_headlines['Date'] <= end_date)].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Group by Date and Sentiment, normalize by total count for each day
    time_series_df = filtered_df.groupby(['Date', 'Sentiment']).size().reset_index(name='Count')
    total_count_per_day = time_series_df.groupby('Date')['Count'].transform('sum')
    time_series_df['Normalized_Count'] = time_series_df['Count'] / total_count_per_day * 100

    # Plot the normalized time series
    fig = px.line(time_series_df, x='Date', y='Normalized_Count', color='Sentiment',
                  title=f'Normalized Sentiment Over Time ({selected_source})')

    fig.update_layout(xaxis_title='Date', yaxis_title='Percentage of Headlines', plot_bgcolor='white')
    return fig

# Callback to update the sentiment distribution graph across all sources
@app.callback(
    Output('sentiment-distribution', 'figure'),
    [Input('sentiment-dropdown-distribution', 'value')]
)
def update_distribution(selected_sentiment):
    # Filter the data by selected sentiment
    filtered_df = df_covid_headlines[df_covid_headlines['Sentiment'] == selected_sentiment].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Count sentiment distribution by source
    sentiment_dist = filtered_df.groupby('Source').size().reset_index(name='Count')

    # Calculate total headlines for each source
    total_headlines = df_covid_headlines.groupby('Source').size().reset_index(name='Total')

    # Merge the two dataframes to get counts and totals
    sentiment_dist = sentiment_dist.merge(total_headlines, on='Source')

    # Normalize by dividing by the total number of headlines for that source
    sentiment_dist['Percentage'] = (sentiment_dist['Count'] / sentiment_dist['Total']) * 100

    # Plot sentiment distribution as a percentage
    fig = px.bar(sentiment_dist, x='Source', y='Percentage',
                 title=f'Normalized {selected_sentiment} Sentiment Distribution Across All Sources',
                 color='Source')

    fig.update_layout(xaxis_title='Source', yaxis_title='Percentage of Headlines', plot_bgcolor='white')
    return fig

# Callback to update the top keywords by sentiment
@app.callback(
    Output('top-keywords', 'figure'),
    [Input('source-dropdown-keywords', 'value')]
)
def update_top_keywords(selected_source):
    filtered_df = df_covid_headlines[df_covid_headlines['Source'] == selected_source].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Explode the tokens to calculate top keywords
    filtered_df['Tokens'] = filtered_df['Tokens'].apply(lambda x: ast.literal_eval(x))
    exploded_df = filtered_df.explode('Tokens')

    # Group by Sentiment and Tokens to find top keywords
    top_keywords_df = exploded_df.groupby(['Sentiment', 'Tokens']).size().reset_index(name='Frequency')
    top_keywords_df = top_keywords_df.sort_values(by='Frequency', ascending=False).groupby('Sentiment').head(10)

    # Plot top keywords
    fig = px.bar(top_keywords_df, x='Tokens', y='Frequency', color='Sentiment',
                 title=f'Top Keywords by Sentiment ({selected_source})', barmode='group')

    fig.update_layout(xaxis_title='Keyword', yaxis_title='Frequency', plot_bgcolor='white')
    return fig

@app.callback(
    Output('vaccine-sentiment-trend', 'figure'),
    [Input('dose-type-dropdown', 'value'),
     Input('sentiment-type-dropdown', 'value'),
     Input('subcategory-dropdown', 'value')]
)
def update_vaccine_sentiment_trend(selected_dose, selected_sentiment, selected_subcategory):
    # Select the appropriate vaccine rate data based on dose type
    if selected_dose == 'First Dose':
        vaccine_data = df_first_dose_rate
    else:
        vaccine_data = df_second_dose_rate

    # Filter data by the selected SubCategory
    vaccine_data = vaccine_data[vaccine_data['SubCategory'] == selected_subcategory]
    sentiment_data = df_covid_headlines_grouped[
        (df_covid_headlines_grouped['Sentiment'] == selected_sentiment) &
        (df_covid_headlines_grouped['SubCategory'] == selected_subcategory)
    ]

    # Merge vaccine and sentiment data on the 'Month' column
    merged_data = pd.merge(vaccine_data, sentiment_data, on='Month', how='inner')

    if merged_data.empty:
        return go.Figure().add_annotation(
            text="No data available for the selected filters",
            showarrow=False
        )

    # Create a line chart with dual y-axes
    fig = go.Figure()

    # Add vaccine rate data
    fig.add_trace(go.Scatter(
        x=merged_data['Month'],
        y=merged_data['Vaccination rate (%)'],
        mode='lines+markers',
        name=f'{selected_dose} Vaccination Rate',
        yaxis='y1'
    ))

    # Add normalized sentiment frequency data
    fig.add_trace(go.Scatter(
        x=merged_data['Month'],
        y=merged_data['Normalized_Frequency'],
        mode='lines+markers',
        name=f'{selected_sentiment} Sentiment Frequency (Normalized)',
        yaxis='y2'
    ))

    # Update layout for dual y-axes
    fig.update_layout(
        title=f'Relationship between {selected_dose} Vaccination Rate and {selected_sentiment} Sentiment in {selected_subcategory}',
        xaxis_title='Month',
        yaxis=dict(
            title='Vaccination Rate (%)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
        ),
        yaxis2=dict(
            title='Normalized Sentiment Frequency',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
        height=600,
        hovermode='x'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
