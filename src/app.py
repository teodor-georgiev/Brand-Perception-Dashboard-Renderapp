import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from PIL import Image
from Functions import *
# dash_bootstrap_components.themes

# Tab 1
# Read the data
df_brands = pd.read_csv("data/df_brands_aggregated.csv",delimiter=";")

# Set the options for the dropdown
renamed_columns = {"Social Perception Score Eco-Friendliness": "SPS Eco", "Survey Score Eco-Friendliness": "Survey Eco", 
               "Social Perception Score Luxury": "SPS Luxury", "Survey Score Luxury": "Survey Luxury", 
               "Social Perception Score Nutrition": "SPS Nutrition", "Survey Score Nutrition": "Survey Nutrition"}
df_brands.rename(columns=renamed_columns, inplace=True)
dropdown_options = df_brands.columns[1:-3].tolist()
dropdown_options_tab1_xaxis = dropdown_options
dropdown_options_tab1_yaxis = dropdown_options

# Rename the columns to make them more readable
df_brands["Sector"].replace({"apparel":"Apparel", "car":"Car", "food":"Food & Beverage", "personal_care":"Personal Care"}, inplace=True)
sectors_list = df_brands["Sector"].unique()
color_discrete_map = {"Apparel":"#636EFA", "Car":"#EF553B", "Food and Beverage":"#00CC96", "Personal Care":"#038764 "}

# Load the Brand Logos
brand_logos = {}
for i, row in df_brands.iterrows():
    brand = row["Brand Name"]
    brand_logos[brand] = Image.open(f"Brand Logos/{brand}.png")

# knowledge_graph_data = json.load(open('Google Searches/BMW.json', 'r'))["knowledge_graph"]
# knowledge_graph_img = brand_logos["BMW"]
 
# Tab 2
# Read the data
df_stocks_days = pd.read_csv("data/tab2/aggregated_stocks_values_days.csv")
df_stocks_weeks = pd.read_csv("data/tab2/aggregated_stocks_values_weeks.csv")
brands_list = df_stocks_days["Brand Name"].unique()
# remove AirBnb and Pepsi from numpy array
brands_list = brands_list[np.where((brands_list != "Airbnb") & (brands_list != "Pepsi"))]
# df_tweets_no_content = pd.read_csv("data/tab2/preprocessed_tweets_no_content.csv")

df_sentiment_overall = pd.read_csv("data/tab2/twitter_sentiment_overall.csv")
# df_tweets_sentiment_monthly = pd.read_csv("data/tab2/twitter_sentiment_monthly_percent.csv")
df_tweets_sentiment_daily = pd.read_csv("data/tab2/twitter_sentiment_daily_percent.csv")
df_tweets_sentiment_weekly = pd.read_csv("data/tab2/twitter_sentiment_weekly_percent.csv")
# df_tweets_languages_count = pd.read_csv("data/tab2/twitter_languages_count.csv")

df_tweets_count_daily = pd.read_csv("data/tab2/twitter_count_daily.csv")
df_tweets_count_weekly = pd.read_csv("data/tab2/twitter_count_weekly.csv")
# df_tweets_count_monthly = pd.read_csv("data/tab2/twitter_count_monthly.csv")

df_stocktwits_daily = pd.read_csv("data/tab2/stocktwits_daily.csv")
df_stocktwits_weekly = pd.read_csv("data/tab2/stocktwits_weekly.csv")
df_stocktwits_overall = pd.read_csv("data/tab2/stocktwits_overall.csv")

df_stocktwits_count_daily = pd.read_csv("data/tab2/stocktwits_daily_count.csv")
df_stocktwits_count_weekly = pd.read_csv("data/tab2/stocktwits_weekly_count.csv")

df_yougov_daily = pd.read_csv("data/tab2/yougov_daily.csv")
df_yougov_weekly = pd.read_csv("data/tab2/yougov_weekly.csv")
df_yougov_overall = pd.read_csv("data/tab2/yougov_overall.csv")

yougov_brand_presence = ["Awareness","Attention","WOM Exposure","Ad Awareness","Buzz"]
yougov_brand_image = ["Impression","Quality","Value","Recommend","Satisfaction","Reputation"]
yougov_brand_relationship = ["Consideration", "Purchase Intent", "Current Customer ", "Former Customer"]

apple_wordcloud_img = Image.open("data/tab2/wordclouds/Apple_positive_wordcloud_square.png")
# range_slider = dict(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=3,
#                      label="3m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=6,
#                      label="6m",
#                      step="month",
#                      stepmode="backward"),
#                 # dict(count=1,
#                 #      label="YTD",
#                 #      step="year",
#                 #      stepmode="todate"),
#                 dict(count=1,
#                      label="1y",
#                      step="year",
#                      stepmode="backward"),
#                 dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=False
#         ),
#         type="date"
#     ) 


charts = {"Stock Price":"Close","Stock Price % Change" :"pct_change","Stock Volume":"Volume","Twitter Polarity":"polarity","Tweets Count" : "tweets_count",
          "Stocktwits Sentiment":"trend","Stocktwits Count":"stocktwits_count"}
yougov_charts = { col: col for col in df_yougov_daily.columns[1:-1]}
charts.update(yougov_charts)
charts_axis_names = {"Stock Price":"Stock Price","Stock Price % Change" :"Stock Price % Change","Stock Volume":"Stock Volume","Twitter Polarity":"Twitter Polarity",
                     "Tweets Count" : "Tweets Count","Stocktwits Sentiment":"Stocktwits Sentiment","Stocktwits Count":"Stocktwits Count"}
charts_axis_names.update(yougov_charts)
# stock_charts_names = {"Line Chart":"line","Candlestick Chart":"candlestick","Area Chart(Cumulative)":"area","Bar Chart(Cumulative)":"bar","Area Chart(t-1)":"area","Bar Chart(t-1)":"bar"}

dropdown_options_tab2_1 = list(charts.keys())
dropdown_options_tab2_2 = list(charts.keys())            
# Define the styles of the elements
SIDEBAR_STYLE = {
    # 'position': 'fixed',
    # "float":"left",
    "position":"absolute",
    'top': "1rem",
    'margin-left': "0.5rem",
    'bottom': "1rem",
    'width': '16%',
    # "height":"565px",
    "height":"628px",
    'padding': '0px 10px',
    'background-color': '#ffffff',
    "border":"1px solid #e0e0e0",
    "border-radius": "10px",
}

TEXT_STYLE = {
    'textAlign': 'center',
}

TEXT_STYLE_DASHBOARD_NAME = {
    'textAlign': 'center',
    # "border":"1px solid #e0e0e0",
    'background-color': "#ffffff",
    "width":"45%",
    "float":"left",
    "height":"66px",
    "margin-top" : "-9px",
    "border-radius": "10px 0px 0px 10px",
    "borderBottom": "1px solid #e0e0e0",
    "borderLeft": "1px solid #e0e0e0",
    "borderTop": "1px solid #e0e0e0",
}

CONTENT_STYLE = {
    'margin-left': '17.5%',
    'margin-right': '0%',
    'padding': '11px 10px',
}

TAB_STYLE = {
    "width":"54%",
    "float":"left",
    "border":"1px solid #e0e0e0",
    'background-color': "#ffffff",
    "margin-top" : "-9px",
    "border-radius": "0px 10px 10px 0px",
}

GRAPH_STYLE = {
    "height" : "600px",
}

SWITCH_NAME_STYLE = {
    "float":"left",
    "width":"80%"  
}

SWITCH_STYLE = { 
    "float":"left", 
    "width":"19%"
}

KNOLEDGE_GRAPH_STYLE = {
    "border":"1px solid #e0e0e0",
    "float":"left",
    "margin-top" : "10px",
    "margin-left" : "10px",
    "width":"18.3%",
    "height":"550px",
    "border-radius": "10px",
    "background-color": "#ffffff"
}

# Define the layout of the App
# tabs = html.Div([
#         dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
#         dcc.Tab(label='Tab One', value='tab-1-example-graph',style = {'borderBottom': '0px solid #d6d6d6',"borderLeft": "0px solid #e0e0e0","background-color": "#ffffff"},
#                 selected_style = {"borderLeft": "0px solid #e0e0e0"},children=[content]),
#         dcc.Tab(label='Tab Two', value='tab-2-example-graph',style = {'borderBottom': '0px solid #d6d6d6',"background-color": "#ffffff"}),
#         dcc.Tab(label='Tab Three', value='tab-3-example-graph',style = {'borderBottom': '0px solid #d6d6d6',"background-color": "#ffffff"}),
#         # dcc.Tab(label='Tab Four', value='tab-4-example-graph'),
#         ])
#         # html.Div(id='tabs-content-example-graph')
# ], style=TAB_STYLE)

# Define the Main Bar
dashboard_name = html.Div(
    html.H3('Brand Perception Dashboard',
            style={"textAlign": "left", "width":"550px","padding-left" : "25px"}),
    style=TEXT_STYLE_DASHBOARD_NAME
)

tabs = html.Div(
                [
                dcc.Tabs(id="tabs", 
                        value='tab_2', 
                        children=[
                    dcc.Tab(label='Mining Brand Perceptions from Twitter', 
                            value='tab_1',
                            style = {'borderBottom': '0px solid #d6d6d6',"borderLeft": "0px solid #e0e0e0","background-color": "#ffffff","borderTop": "0px solid #e0e0e0"},
                            selected_style = {"borderLeft": "0px solid #e0e0e0"}),
                    dcc.Tab(label="Brand Perceptions' effect on Stock Price",
                            value='tab_2',
                            style = {'borderBottom': '0px solid #d6d6d6',"background-color": "#ffffff","borderTop": "0px solid #e0e0e0","borderRight": "0px solid #d6d6d6",
                                     "border-radius": "0px 10px 10px 0px"},
                            selected_style = {"borderRight": "0px solid #e0e0e0","border-radius": "0px 10px 10px 0px"}),
                    # dcc.Tab(label='Tab Three', 
                    #         value='tab_3',
                    #         style = {'borderBottom': '0px solid #d6d6d6',"borderRight": "0px solid #d6d6d6","background-color": "#ffffff",
                    #                 "border-radius": "0px 10px 10px 0px","borderTop": "0px solid #e0e0e0"})
                    ])
                ],
                style=TAB_STYLE
)

# Define the layout of the sidebar
sidebar_panel = html.Div(id = "sidebar_panel",
                         children = [],
                         style = SIDEBAR_STYLE)

# Begin content of sidebar in Tab 1
switch_1 =  html.Div(
            [
            html.P("Show Brand Names",style = SWITCH_NAME_STYLE),
            daq.BooleanSwitch(id='brand-names-switch',
                              on=True,
                              style = SWITCH_STYLE)
            ],
            style = {"height":"40px"}
)

switch_2 =  html.Div(
            [
            html.P("Show Trendline",style = SWITCH_NAME_STYLE),
            daq.BooleanSwitch(id='trendline-switch',on=True,style = SWITCH_STYLE)
            ]
            ,style ={"height":"40px"}
)

switch_3 =  html.Div(
            [
            html.P("Show Brand Logos",style = SWITCH_NAME_STYLE),
            daq.BooleanSwitch(id='logo-switch',on=False,style = SWITCH_STYLE)
            ]
            ,style ={"height":"40px"}
)


sidebar_1 = [
        html.H3("Filters", style={"textAlign": "center",}),
        html.Img(src="assets/filter_icon.png", style={"width":"100%","height":"75px","object-fit":"contain"}),
        dbc.Nav
        (
            [
                html.Label('Select X-Axis'),
                dcc.Dropdown(dropdown_options_tab1_xaxis, 'Survey Eco', id='xaxis-column',clearable=False),
                html.Br(),
                
                html.Label('Select Y-Axis'),
                dcc.Dropdown(dropdown_options_tab1_yaxis,'SPS Eco',id='yaxis-column',clearable=False),
                html.Br(),
                
                html.Label('Select Sector(s)'),
                dcc.Dropdown(sectors_list,['Car'],multi=True, id="sector-dropdown",placeholder="Select Sector(s)",style={"height":"75px"}),
                html.Br(),
                switch_1,
                switch_2,
                switch_3,
                
            ],
            vertical=True,
            pills=True,
        ),
    ]
# End of content of sidebar in Tab 1

# Begin Content of sidebar in Tab 2
switch_1_tab_2 =  html.Div(
            [
            html.P("Toggle Day/Week",style = SWITCH_NAME_STYLE),
            daq.BooleanSwitch(id='day-week-switch',on=False,style = SWITCH_STYLE)
            ]
            ,style ={"height":"40px"}
)

sidebar_2 = [
        html.H3("Filters", style={"textAlign": "center",}),
        # html.Hr(),
        # html.P("A simple sidebar layout with filters", className="lead"),
        html.Img(src="assets/filter_icon.png", style={"width":"100%","height":"75px","object-fit":"contain"}),
        
        dbc.Nav
        (
            [
                html.Label('Select Brand'),
                dcc.Dropdown(brands_list, 'Apple', id='brand-dropdown',clearable=False),
                html.Br(),
                
                html.Label('Select Y-Axis'),
                dcc.Dropdown(dropdown_options_tab2_1,"Stock Price",id='chart-dropdown',clearable=False),
                html.Br(),
                
                html.Label('Select Additional Y-Axis'),
                dcc.Dropdown(dropdown_options_tab2_2,None,id='chart-dropdown-2',clearable=True),
                html.Br(),
                switch_1_tab_2
                
            ],
            vertical=True,
            pills=True,
        ),
    ]
# End of content of sidebar in Tab 2

# Define the layout of the main content
content = html.Div(id="content", children=
    [
        # content_first_row,
        # content_second_row,
    ],
    style=CONTENT_STYLE
)

# Begin content of main content in Tab 1
# knowledge_graph = html.Div([
#                 html.H6("Knowledge Graph", style={"border":"1px solid #e0e0e0","margin-top" : "5px","margin-left" : "10px", "width":"92%",'textAlign': 'center'}),
#                 html.Img(src=knowledge_graph_img, style={"width":"100%","height":"150px","object-fit":"contain"}),
#                 html.P(knowledge_graph_data["title"], style={"margin-left" : "10px", "width":"92%","textAlign": 'center',"font-weight":"bold","border":"1px solid #e0e0e0"}),
#                 html.P(knowledge_graph_data["description"], style={"margin-left" : "10px", "width":"92%","border":"1px solid #e0e0e0","font-family":"Arial","font-size":"80%"}),
# ],style=KNOLEDGE_GRAPH_STYLE)


content_first_row = html.Div( 
                            [
                            dcc.Graph(
                                id='brand_perception_culotta',
                                style={"border":"1px solid #e0e0e0","width": "80%","float":"left","margin-top" : "10px","border-radius": "10px",
                                'background-color':'white'},config={"scrollZoom":True,'displayModeBar': False}),
                            # knowledge_graph
                            ]
                             )

content_second_row = html.Div([
                            dcc.Graph(id='brand_perception_culotta_boxplot_x',style={"border":"1px solid #e0e0e0","width": "49%","float":"left","margin-top" : "10px",
                                                                                     "border-radius": "10px",'background-color':'white'},config={'displayModeBar': False}), 

                            dcc.Graph(id='brand_perception_culotta_boxplot_y',style={"border":"1px solid #e0e0e0","width": "49%","float":"left","margin-top" : "10px","margin-left" : "10px",
                                                                                     "border-radius": "10px",'background-color':'white'},config={'displayModeBar': False})
                            ]
                             )
# End of content of main content in Tab 1


SMALL_TABS_STYLE = {'padding': '10px',"display":"flex","align-items": "center","justify-content": "center",'margin': '0 3px',"border":"0px solid #e0e0e0","background-color":"#eeeeee"
                    ,"font-weight" : "bold","border-radius": "5px","width":"25px","height":"15px"}
SMALL_TABS_STYLE_SELECTED = {**SMALL_TABS_STYLE, 'background-color':'#d4d4d4'}

SMALL_TABS_STYLE_CLOUD = {**SMALL_TABS_STYLE, 'width':'50px'}

SMALL_TABS_STYLE_CLOUD_SELECTED = {**SMALL_TABS_STYLE_CLOUD, 'background-color':'#d4d4d4'}

# SMALL_TABS_STYLE_SELECTED = SMALL_TABS_STYLE.update({'background-color':'#e0e0e0'})
# Begin content of main content in Tab 2
content_first_row_2 = html.Div(
                                [ 
                                dcc.Graph(id='brand_stocks_chart',
                                          style={"border":"1px solid #e0e0e0","width": "1191px","float":"left","margin-top" : "10px","border-radius": "10px",'background-color':'white'},
                                          config={"scrollZoom":True,'displayModeBar': False}),
                                # html.Div([
                                # dcc.Graph(id="brand_sentiment_time_chart",style={"border":"1px solid #e0e0e0","width": "100%",
                                #                                                  'background-color':'white',"border-radius": "10px"},config = {'displayModeBar': False}),
                                # dcc.Tabs(id="tabs_sentiment", value='D', children=[dcc.Tab(label='D', value='D',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED),
                                #                                                        dcc.Tab(label='W', value='W',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED),
                                #                                                        dcc.Tab(label='M', value='M',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED)],
                                #          style = {"position":"absolute","top":"5px","left":"400px","font-size": "11px"}),
                                # ],style={"position":"relative","width": "34%","float":"left","margin-top" : "10px","margin-left" : "10px",}),
                                # html.Div(
                                # [
                                # dcc.Graph(id="brand_twitter_count",style={"border":"1px solid #e0e0e0","width": "100%",
                                #                                                  'background-color':'white',"border-radius": "10px"},config = {'displayModeBar': False}),
                                # dcc.Tabs(id="tabs_count", value='D', children=[dcc.Tab(label='D', value='D',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED),
                                #                                                        dcc.Tab(label='W', value='W',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED),
                                #                                                        dcc.Tab(label='M', value='M',style=SMALL_TABS_STYLE,selected_style=SMALL_TABS_STYLE_SELECTED)],
                                #          style = {"position":"absolute","top":"5px","left":"400px","font-size": "11px"}),
                                # ],style={"position":"relative","width": "34%","float":"left","margin-top" : "10px","margin-left" : "10px",})
                                dcc.Graph(id="brand_overall_sentiment",style={"border":"1px solid #e0e0e0","width": "331px","float":"left","margin-top" : "10px","border-radius": "10px",
                                                                            'background-color':'white',"margin-left" : "10px"},config = {'displayModeBar': False}),
                                ]
)

content_second_row_2 = html.Div(
                                [
                                   
                                    
                                    
                                    dcc.Graph(id="brand_overall_pressence",style={"border":"1px solid #e0e0e0","width": "389px","float":"left","margin-top" : "10px","border-radius": "10px",
                                                                                'background-color':'white',"margin-left" : "0px"},config = {'displayModeBar': False}),
                                    dcc.Graph(id="brand_overall_image",style={"border":"1px solid #e0e0e0","width": "389px","float":"left","margin-top" : "10px","border-radius": "10px",
                                                                            'background-color':'white',"margin-left" : "10px"},config = {'displayModeBar': False}),
                                    dcc.Graph(id="brand_overall_relationship",style={"border":"1px solid #e0e0e0","width": "389px","float":"left","margin-top" : "10px","border-radius": "10px",
                                                                            'background-color':'white',"margin-left" : "10px"},config = {'displayModeBar': False}),
                                    html.Div(
                                    [   html.P("Twitter Word Cloud",style={"border":"0px solid #e0e0e0","margin-top" : "0px","margin-left" : "55px", "width":"92%",'textAlign': 'left',
                                                                           "font-size": "18px","fontFamily": "Helvetica"}),
                                        html.Img(id = "wordcloud",
                                                src= apple_wordcloud_img,
                                                style = {"object-fit": "contain","width": "99%","height": "88%","margin-top" : "0px","margin-left" : "5px","margin-right" : "5px"}),
                                        dcc.Tabs(id="tabs_wordcloud",
                                                 value='positive',
                                                 children=  [
                                                                dcc.Tab(label='Positive', value='positive',style=SMALL_TABS_STYLE_CLOUD,selected_style=SMALL_TABS_STYLE_CLOUD_SELECTED),
                                                                dcc.Tab(label='Negative', value='negative',style=SMALL_TABS_STYLE_CLOUD,selected_style=SMALL_TABS_STYLE_CLOUD_SELECTED)
                                                            ],
                                         style = {"position":"absolute","top":"5px","left":"215px","font-size": "11px"})
                                    ],style={"width": "331px","float":"left","height": "380px","margin-top" : "10px","margin-left" : "10px",
                                             "border":"1px solid #e0e0e0","border-radius": "10px","background-color":"white","position":"relative"})
                                    
                                ], 
                                # style = {"margin-left" : "-337px"}
)
dashboard_main = html.Div(
    [
        dashboard_name,
        tabs,
    ],
    style=CONTENT_STYLE
)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__,external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

# Create server variable with Flask server object for use with gunicorn
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = df_brands


# Create app layout
# app.layout = html.Div(children=[content,sidebar])
app.layout = html.Div(children=[dashboard_main,sidebar_panel,content])

@app.callback(Output("content", "children"),
              Output("content", "style"), 
              Input("tabs", "value"))
def render_content(tab):
    if tab == "tab_1":
        return [content_first_row, content_second_row] , CONTENT_STYLE
    elif tab == "tab_2":
        CONTENT_STYLE_2 = CONTENT_STYLE.copy()
        # CONTENT_STYLE_2.update({"margin-left":"13px"})
        return [content_first_row_2, content_second_row_2], CONTENT_STYLE_2
    
@app.callback(Output("sidebar_panel", "children"),
              Output("sidebar_panel", "style"),
              Input("tabs", "value"))
def render_sidebar(tab):
    if tab == "tab_1":
        return sidebar_1 , SIDEBAR_STYLE
    elif tab == "tab_2":
        SIDEBAR_STYLE_2 = SIDEBAR_STYLE.copy()
        SIDEBAR_STYLE_2.update({"height":"528px"})
        return sidebar_2 , SIDEBAR_STYLE_2

# Remove selected value from dropdown options
@app.callback(Output("xaxis-column","options"),
              Output("yaxis-column","options"),
              Input("xaxis-column","value"),
              Input("yaxis-column","value")
              )
def remove_options_tab(xaxis_column_value,yaxis_column_value):
    options_xaxis = [x for x in dropdown_options_tab1_xaxis if x != yaxis_column_value]
    options_yaxis = [x for x in dropdown_options_tab1_yaxis if x != xaxis_column_value]
    return options_xaxis, options_yaxis


@app.callback(
    Output('brand_perception_culotta', 'figure'),
    Output('brand_perception_culotta_boxplot_x', 'figure'),
    Output('brand_perception_culotta_boxplot_y', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('sector-dropdown', 'value'),
    Input('brand-names-switch', 'on'),
    Input('trendline-switch', 'on'),
    Input('logo-switch', 'on'),
    )

def update_graphs_1(xaxis_column_name, yaxis_column_name,sector_dropdown_name, brand_names, trendline_switch,logo_switch):
    df_filtered = df_brands[df_brands["Sector"].isin(sector_dropdown_name)]
    # dots_size = df_filtered[yaxis_column_name].fillna(0) + df_filtered[xaxis_column_name].fillna(0)
    df_filtered["dots_size"] = 1
    # Create the Scatter Plot
    fig = px.scatter(
                        df_filtered, x=xaxis_column_name, y=yaxis_column_name, color="Sector",hover_name="Brand Name", size = "dots_size", size_max=15,
                        height=550, color_discrete_map=color_discrete_map, hover_data={"dots_size":False,xaxis_column_name :":.2f", yaxis_column_name :":.3f"},
                        trendline="ols" if trendline_switch else None,
                        template = "simple_white"
                    )
    title = "Scatterplot of " + xaxis_column_name + " vs " + yaxis_column_name
    annotations = create_annotations(df_filtered, xaxis_column_name, yaxis_column_name)
    fig.update_layout(  
                        margin={'l': 40, 'b': 40, 't': 30, 'r': 180}, hovermode='closest',
                        hoverlabel=dict(bgcolor="white"),
                        uirevision="Don't change",
                        # Make the background transparent
                        paper_bgcolor='rgba(0,0,0,0)',
                        # scene=dict(annotations=annotations)
                        # legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.99)
                        # legend=dict(
                        #         orientation="h",
                        #         yanchor="bottom",
                        #         y=0.95,
                        #         xanchor="right",
                        #         x=0.99
                        #         ),
                    
                        # transition_duration=250   
                        title={
                        'text': title,
                        'y':0.97,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'} 
                    )

    # fig.update_traces(hovertemplate = xaxis_column_name + " %{x}" + "<br>%{y:.2f}")
    fig.update_xaxes(title = xaxis_column_name)
    fig.update_yaxes(title = yaxis_column_name)
    
    # fig.update_traces(textposition='top center',textfont_size=12)
    # fig.update_traces(marker={'size': 15})
    
    fig.update_layout(annotations=annotations if brand_names else [])
    
    # Create the Boxplots
    boxplot_x = create_boxplot(df_filtered, xaxis_column_name, xaxis_column_name, color_discrete_map)
    boxplot_y = create_boxplot(df_filtered, yaxis_column_name, yaxis_column_name, color_discrete_map)
    

    # fig.update_traces(marker_color="rgba(0,0,0,0)")
    if logo_switch:
        fig.update_traces(marker={'size': 1})
        xaxis_max = df_filtered[xaxis_column_name].max()
        yaxis_max = df_filtered[yaxis_column_name].max()
        x_size = xaxis_max*0.09
        y_size = yaxis_max*0.09
        if yaxis_column_name == "Survey Eco" and "Apparel" in sector_dropdown_name:
            x_size = xaxis_max*0.06
            y_size = yaxis_max*0.06
        
        for i, row in df_filtered.iterrows():
            brand = row["Brand Name"]
            fig.add_layout_image(
                dict(
                    source= brand_logos[brand],
                    xref= "x",
                    yref= "y",
                    xanchor="center",
                    yanchor="middle",
                    x=row[xaxis_column_name],
                    y=row[yaxis_column_name],
                    sizex= x_size,
                    sizey= y_size,
                    sizing="contain",
                    opacity=1,
                    layer="above"
                )
            )

    return fig, boxplot_x, boxplot_y


# Turn Brand Names Off when Brand Logos are turned ON
@app.callback(
    Output('brand-names-switch',"on"),
    Output('brand-names-switch',"disabled"), 
    Input('logo-switch', 'on'))
def update_brand_names(logo_switch):
    if logo_switch:
        return False, True
    else:
        return True, False
    
# Callbacks for Tab 2
@app.callback(Output("brand_stocks_chart","figure"),
              Input("brand-dropdown","value"),
              Input("chart-dropdown","value"),
              Input("chart-dropdown-2","value"),
              Input("day-week-switch","on"),
              )
def update_brand_stocks_chart(brand_dropdown, chart_dropdown, chart_dropdown_2, day_week_switch):
    if day_week_switch:
        df_stocks_filtered = df_stocks_weeks[df_stocks_weeks["Brand Name"] == brand_dropdown]
        df_tweets_filtered = df_tweets_sentiment_weekly[df_tweets_sentiment_weekly["brand"] == brand_dropdown]
        df_tweets_count_filtered = df_tweets_count_weekly[df_tweets_count_weekly["brand"] == brand_dropdown]
        df_stocktwits_filtered = df_stocktwits_weekly[df_stocktwits_weekly["brand"] == brand_dropdown]
        df_stocktwits_count_filtered = df_stocktwits_count_weekly[df_stocktwits_count_weekly["brand"] == brand_dropdown]
        df_yougov_filtered = df_yougov_weekly[df_yougov_weekly["Brand"] == brand_dropdown]
        title_prefix = "Weekly "
    else:    
        df_stocks_filtered = df_stocks_days[df_stocks_days["Brand Name"] == brand_dropdown]
        df_tweets_filtered = df_tweets_sentiment_daily[df_tweets_sentiment_daily["brand"] == brand_dropdown]
        df_tweets_count_filtered = df_tweets_count_daily[df_tweets_count_daily["brand"] == brand_dropdown]
        df_stocktwits_filtered = df_stocktwits_daily[df_stocktwits_daily["brand"] == brand_dropdown]
        df_stocktwits_count_filtered = df_stocktwits_count_daily[df_stocktwits_count_daily["brand"] == brand_dropdown]
        df_yougov_filtered = df_yougov_daily[df_yougov_daily["Brand"] == brand_dropdown]
        title_prefix = "Daily "
    
    # Link dropdown values to corresponding dataframes
    charts_df = {"Stock Price": df_stocks_filtered, "Stock Price % Change": df_stocks_filtered, "Stock Volume": df_stocks_filtered, "Twitter Polarity": df_tweets_filtered,
                 "Tweets Count": df_tweets_count_filtered, "Stocktwits Sentiment": df_stocktwits_filtered, "Stocktwits Count": df_stocktwits_count_filtered}
    yougov_charts_df = {key: df_yougov_filtered for key in yougov_charts.keys()}
    charts_df.update(yougov_charts_df)
    
    x_1 = charts_df[chart_dropdown]["Date"]
    y_1 = charts_df[chart_dropdown][charts[chart_dropdown]]
    x_2 = charts_df[chart_dropdown_2]["Date"] if chart_dropdown_2 != None else None
    y_2 = charts_df[chart_dropdown_2][charts[chart_dropdown_2]] if chart_dropdown_2 != None else None
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=x_1, y=y_1, name=charts_axis_names[chart_dropdown], line=dict(width=1.5),connectgaps = True)
                  ,secondary_y=False)
    title = title_prefix + brand_dropdown + " " + charts_axis_names[chart_dropdown]
    if chart_dropdown_2 != None:
        title += " vs. " + charts_axis_names[chart_dropdown_2]
        fig.add_trace(go.Scatter(x=x_2, y=y_2, name=charts_axis_names[chart_dropdown_2],line=dict(width=1.5),connectgaps = True,),
                      secondary_y=True)
    
    fig.update_layout(margin={'l': 30, 'b': 40, 't': 30, 'r': 40}, hovermode='x unified', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)',
                    template = "simple_white", showlegend=True,
                    title={
                    'text': title,
                    'y':0.97,
                    'x':0.46,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=0.95,
                                xanchor="right",
                                x=0.94
                                )
                    
                    
                    )
    # Round hoverdata to 2 decimal places
    # fig.update_traces(hovertemplate = "%{x}<br>%{y:.2f}")
    fig.update_traces(hovertemplate = "%{y:.2f}")
    fig.update_xaxes(title = "Date")
    fig.update_yaxes(title_text=charts_axis_names[chart_dropdown], secondary_y=False)
    
    # Add second y-axis if second dropdown is selected
    if chart_dropdown_2 != None:
        # Perform Pearson correlation
        r = pearson_correlation(charts_df[chart_dropdown], charts_df[chart_dropdown_2],charts[chart_dropdown], charts[chart_dropdown_2])
        r_str = str(round(r[0],2))
        p = r[1]
        p_str = " ***" if p < 0.001 else " **" if p < 0.01 else " *" if p < 0.05 else " ." if p < 0.1 else ""
        
        fig.update_yaxes(title_text=charts_axis_names[chart_dropdown_2], secondary_y=True)
        fig.add_annotation(dict(font=dict(size=14),
                                        x=0.46,
                                        y=0.96,
                                        showarrow=False,
                                        text="r = " + r_str + p_str,
                                        textangle=0,
                                        xanchor='center',
                                        yanchor='bottom',
                                        xref="paper",
                                        yref="paper"
                                        ))
        
    # fig.update_xaxes(rangeselector_x=0.85, rangeselector_y=1, rangeselector_font_size=11.5)
    # fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

# @app.callback(Output("brand_sentiment_time_chart","figure"),
#               Input("brand-dropdown","value"),
#               Input("tabs_sentiment","value"),
#               )
# def update_brand_sentiment_chart(brand_dropdown,tabs_sentiment):
#     brand = brand_dropdown
#     if tabs_sentiment == "D":
#         df_sentiment = df_tweets_sentiment_daily[df_tweets_sentiment_daily["brand"] == brand]
#     elif tabs_sentiment == "W":
#         df_sentiment = df_tweets_sentiment_weekly[df_tweets_sentiment_weekly["brand"] == brand]
#     else:
#         df_sentiment = df_tweets_sentiment_monthly[df_tweets_sentiment_monthly["brand"] == brand]
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df_sentiment["Date"], y=df_sentiment["sentiment_neg_perc"], mode='lines', name='Negative Sentiment', line=dict(color='rgb(248, 79, 49)', width=2), stackgroup='one'))
#     fig.add_trace(go.Scatter(x=df_sentiment["Date"], y=df_sentiment["sentiment_pos_perc"], mode='lines', name='Positive Sentiment', line=dict(color='rgb(35, 197, 82)', width=2), stackgroup='one'))
#     fig.update_layout(margin={'l': 20, 'b': 20, 't': 30, 'r': 20}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)', height=219,
#                     template="simple_white",showlegend=False,
#                     yaxis=dict(
#                     type='linear',
#                     range=[1, 100],
#                     ticksuffix='%'),
#                     # title ="Monthly Tweets Sentiment",
#                     title={
#                     'text': "Monthly Tweets Sentiment" if tabs_sentiment == "M" else "Weekly Tweets Sentiment" if tabs_sentiment == "W" else "Daily Tweets Sentiment",
#                     'y':0.97,
#                     'x':0.53,
#                     'xanchor': 'center',
#                     'yanchor': 'top'},
#                     )
    
#     # fig.update_xaxes(
#     #                 # dtick="M1",
#     #                 # tickformat="%b\n%Y",
#     #                 ticklabelmode="period")
#     return fig

# @app.callback(Output("brand_twitter_count","figure"),
#               Input("tabs_count","value"),
#               Input("brand-dropdown","value"),
#               )
# def update_brand_twitter_count(tabs_count,brand_dropdown):
#     brand = brand_dropdown
#     if tabs_count == "D":
#         df_count = df_tweets_count_daily[df_tweets_count_daily["brand"] == brand]
#     elif tabs_count == "W":
#         df_count = df_tweets_count_weekly[df_tweets_count_weekly["brand"] == brand]
#     else:
#         df_count = df_tweets_count_monthly[df_tweets_count_monthly["brand"] == brand]
    
#     # fig = px.area(df_count, x="date_axis", y="tweets_count", color_discrete_sequence=['#1f77b4'], height=225)
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df_count["Date"], y=df_count["tweets_count"], mode='lines', name='Tweets Count', line=dict(color='#1f77b4', width=2),stackgroup='one'))
#     fig.update_layout(margin={'l': 55, 'b': 20, 't': 30, 'r': 20}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)', height=219,
#                     template="simple_white",showlegend=False, 
#                     # hovertemplate= '<br>'.join(['Count: $%{y:.2f}','Date: %{x}']),
#                     title={
#                     'text': "Monthly Tweets Count" if tabs_count == "M" else "Weekly Tweets Count" if tabs_count == "W" else "Daily Tweets Count",
#                     'y':0.97,
#                     'x':0.53,
#                     'xanchor': 'center',
#                     'yanchor': 'top'},
#                     )
#     fig.update_xaxes(title = None)
#     fig.update_yaxes(title = None)
#     return fig

# Remove dropdown options from second dropdown if they are selected in the first dropdown
@app.callback(Output("chart-dropdown","options"),
              Output("chart-dropdown-2","options"),
              Input("chart-dropdown","value"),
              Input("chart-dropdown-2","value")
              )
def remove_options_tab2(chart_dropdown_value,chart_dropdown_2_value):
    options = [x for x in dropdown_options_tab2_1 if x != chart_dropdown_2_value]
    options_2 = [x for x in dropdown_options_tab2_2 if x != chart_dropdown_value]
    return options, options_2
  
@app.callback(Output("brand_overall_sentiment","figure"),
              Input("brand-dropdown","value"),
              )
def update_brand_overall_sentiment(brand_dropdown):
    df_sentiment = df_sentiment_overall[df_sentiment_overall["brand"] == brand_dropdown]
    labels = ['Positive', 'Negative']
    values = [df_sentiment["sentiment_pos_perc"].values[0], df_sentiment["sentiment_neg_perc"].values[0]]
    middle_text = str(round(df_sentiment["sentiment_pos_perc"].values[0],1)) + "%"
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5,   )])
    fig.update_traces(hoverinfo='label+percent',textinfo='none',
                      marker=dict(colors=['rgb(35, 197, 82)', 'rgb(248, 79, 49)']))
    fig.update_layout(margin={'l': 20, 'b': 20, 't': 30, 'r': 20}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)', height=219,
                    template="simple_white",showlegend=False,
                    title={
                    'text': "Overall Twitter Sentiment",
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    annotations=[dict(text=middle_text, x=0.5, y=0.5, font_size=18, showarrow=False)],
                    )
    return fig    

# Callback for the wordcloud
@app.callback(Output("wordcloud","src"),
              Input("brand-dropdown","value"),
              Input("tabs_wordcloud","value"),
              )  
def update_wordcloud(brand_dropdown,tabs_wordcloud):
    brand_name = brand_dropdown
    polarity = tabs_wordcloud
    source = Image.open(f"data/tab2/wordclouds/{brand_name}_{polarity}_wordcloud_square.png")
    return source

# Callback for the radar charts
@app.callback(Output("brand_overall_pressence", "figure"),
              Output("brand_overall_image", "figure"),
              Output("brand_overall_relationship", "figure"),
              Input("brand-dropdown","value"),
              )
def update_radar_charts(brand_dropdown):
    df_yougov = df_yougov_overall.loc[df_yougov_overall["Brand"] == brand_dropdown]
    df_yougov = df_yougov.drop(columns=["Brand"])
    
    # Presence
    df_yougov_pressence = df_yougov[yougov_brand_presence]
    r_pressence = df_yougov_pressence.values[0].tolist()
    theta_pressence = df_yougov_pressence.columns.tolist()
    fig_presence = px.line_polar(df_yougov_pressence, r=r_pressence, theta=theta_pressence, line_close=True,height=380)
    fig_presence.update_layout(margin={'l': 25, 'b': 20, 't': 50, 'r': 50}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    title={
                    'text': "Overall Brand Presence",
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    )
    fig_presence.update_traces(fill='toself',
                               mode="lines+markers",
                               hovertemplate = "%{theta} %{r:.2f}")
    # hovertemplate = "%{y:.2f}"
    # Image
    df_yougov_image = df_yougov[yougov_brand_image]
    r_image = df_yougov_image.values[0].tolist()
    theta_image = df_yougov_image.columns.tolist()
    fig_image = px.line_polar(df_yougov_image, r=r_image, theta=theta_image, line_close=True,height=380)
    fig_image.update_layout(margin={'l': 55, 'b': 20, 't': 50, 'r': 30}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    title={
                    'text': "Overall Brand Image",
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    polar=dict(radialaxis=dict(visible=True, range=[-20, 50])),
                    )
    fig_image.update_traces(fill='toself',
                            mode="lines+markers",
                            hovertemplate = "%{theta} %{r:.2f}")
    
    # Relationship
    df_yougov_relationship = df_yougov[yougov_brand_relationship]
    r_relationship = df_yougov_relationship.values[0].tolist()
    theta_relationship = yougov_brand_relationship
    fig_relationship = px.line_polar(df_yougov_relationship, r=r_relationship, theta=theta_relationship, line_close=True,height=380)
    fig_relationship.update_layout(margin={'l': 20, 'b': 20, 't': 50, 'r': 30}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    title={
                    'text': "Overall Brand Relationship",
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                    polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
                    
                    )
    fig_relationship.update_traces(fill='toself',
                                    mode="lines+markers",
                                    hovertemplate = "%{theta} %{r:.2f}")
    # Adding new line to the ticktext
    ticks_new_line = ["Consideration", "Purchase<br>Intent", "Current  <br>Customer", "Former  <br>Customer"]
    fig_relationship.update_polars(angularaxis_rotation=45,
                                    angularaxis_ticktext=ticks_new_line,
                                    angularaxis_tickvals=[0,1,2,3],
                                   )
    return fig_presence, fig_image, fig_relationship
  
# @app.callback(Output("brand_language_count","figure"),
#               Input("brand-dropdown","value"),
#               )
# def brand_languages_count(brand_dropdown):
#     df_language_count = df_tweets_languages_count[df_tweets_languages_count["brand"] == brand_dropdown]
#     fig = px.pie(df_language_count, values='count', names='language', hole=.5,height=225)
#     fig.update_layout(margin={'l': 20, 'b': 20, 't': 30, 'r': 20}, hovermode='closest', hoverlabel=dict(bgcolor="white"),paper_bgcolor='rgba(0,0,0,0)', template="simple_white",showlegend=True,
#                     title={
#                     'text': "Tweets Languages",
#                     'y':0.97,
#                     'x':0.53,
#                     'xanchor': 'center',
#                     'yanchor': 'top'},
#                     )
    
#     return fig
         
                   

if __name__ == "__main__":
	app.run_server(port='8080',debug=True)