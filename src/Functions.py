import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
import pandas as pd

# Function to annotate the plot
def create_annotations(df: dict, xaxis: str, yaxis: str)->list:
    """
    Adds annotations to the plot

    Parameters
    ----------
    df : dict
        Dataframe with the data
    xaxis : str
        Name of the column to be used as x-axis
    yaxis : str
        Name of the column to be used as y-axis

    Returns
    -------
    annotations : List
        List with the annotations
    """    
    annotations = []
    first = True
    for index, row in df.iterrows():
        if first:
            col = "black"
            first = False
        else:
            col = "black"
                
        anno = dict(x=row[xaxis],
                    y=row[yaxis],
                    text=row["Brand Name"],
                    showarrow=False,
                    arrowhead=0,
                    font=dict(color=col),
                    yshift=25,
                    bgcolor="white",
                    opacity=0.85)

        annotations.append(anno)
    return annotations

def create_boxplot(df: dict, axis: str,axis_titles, color_map)->object:
    """
    Creates a boxplot

    Parameters
    ----------
    df : dict
        Dataframe with the data
    axis : str
        Axis to be used

    Returns
    -------
    object
        Object with the plot
    """    
    fig = px.box(df, x="Sector", y=axis, color="Sector",  color_discrete_map= color_map, height = 265,
                       template = "simple_white")
    fig.update_yaxes(title = axis_titles)
    fig.update_layout (  
                        margin={'l': 40, 'b': 40, 't': 30, 'r': 18},
                        boxgap=0.8 if df["Sector"].nunique() < 3 else 0.2,
                        # Make the plot background transparent
                        paper_bgcolor='rgba(0,0,0,0)',
                        title={
                        'text': "Boxplot of " + axis,
                        'y':0.97,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                        yaxis_tickformat=",.3f"
                    
                        )
    return fig

def create_figure(df: dict, type: str, height: int,template : str)->object:
    """
    Creates a figure of given type

    Parameters
    ----------
    df : dict
        Dataframe with the data
    type : str
        Figure type
    height : int
        Height of the figure
    template : str
        Template of the figure

    Returns
    -------
    object
        Object with the plot
    """
    if type == "Line Chart":
        fig = px.line(df, x="Date", y="Close", template = template,height=height)
        return fig
    elif type == "Bar Chart(t-1)":
        fig = px.bar(df, x="Date", y="pct_change", template = template,height=height)
        df["Color"] = np.where(df["pct_change"]<0, 'crimson', '#1f77b4')
        fig.update_traces(marker_color=df["Color"])
        return fig
    elif type == "Candlestick Chart":
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        # template = template,
                        # height=height
                        )], 
                        layout=go.Layout(
                        # title="Mt Bruno Elevation",
                        # width=500,
                        height = height,
                        template = template,
    ))
        return fig
    elif type == "Area Chart(t-1)":
        fig = px.area(df, x="Date", y="pct_change", template = template,height=height)
        df["Color"] = np.where(df["pct_change"]<0, 'crimson', '#1f77b4')
        fig.update_traces(marker_color=df["Color"])
        return fig
    elif type == "Bar Chart(Cumulative)":
        fig = px.bar(df, x="Date", y="cumulative_returns", template = template,height=height)
        df["Color"] = np.where(df["cumulative_returns"]<0, 'crimson', '#1f77b4')
        fig.update_traces(marker_color=df["Color"])
        return fig
    elif type == "Area Chart(Cumulative)":
        fig = px.area(df, x="Date", y="cumulative_returns", template = template,height=height)
        df["Color"] = np.where(df["cumulative_returns"]<0, 'crimson', '#1f77b4')
        fig.update_traces(marker_color=df["Color"])
        return fig
    
    
def pearson_correlation(df_1, df_2, column_name_1, column_name_2):
    df_1 = df_1[['Date', column_name_1]]
    df_2 = df_2[['Date', column_name_2]]
    df_correlate = pd.merge(df_1, df_2, on='Date', how='inner')
    df_correlate = df_correlate.dropna()
    if len(df_correlate) <= 2:
        return (0, 1)
    x = df_correlate[column_name_1]
    y = df_correlate[column_name_2]
    r = stats.pearsonr(x, y)
    return r