######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Drinks!'
color1='#92A5E8'
color2='#FF82AB'
color3='#FFC300'
color4='#228B22'
color5='#33A1C9'
sourceurl = 'https://git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/blob/master/data/drinks.csv'
githublink = 'https://github.com/yibaiyilan/304-titanic-dropdown.git'


###### Import a dataframe #######
df = pd.read_csv('https://raw.git.generalassemb.ly/intuit-ds-15/05-cleaning-combining-data/master/data/drinks.csv?token=AAAK2LPHP3AY6NSYEPWPUFLC7NBC2',on_bad_lines='skip')
variables_list=['beer_servings','spirit_servings','wine_servings']

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('Choose a continent for summary statistics:'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'),
              [Input('dropdown', 'value')])
def display_value(continuous_var):
    grouped_mean=df.groupby(['continent',pd.cut(df["total_litres_of_pure_alcohol"], np.arange(0, 18, 3)).astype(str)]).mean()
    results=pd.DataFrame(grouped_mean).dropna()
    # Create a grouped bar chart
    mydata1 = go.Bar(
    x=results.loc['AF'].index,
    y=results.loc['AF'][continuous_var],
    name='Africa',
    marker=dict(color=color1)
    )
    mydata2 = go.Bar(
        x=results.loc['AS'].index,
        y=results.loc['AS'][continuous_var],
        name='Asia',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        x=results.loc['EU'].index,
        y=results.loc['EU'][continuous_var],
        name='Europe',
        marker=dict(color=color3)
    )
    mydata4 = go.Bar(
        x=results.loc['OC'].index,
        y=results.loc['OC'][continuous_var],
        name='Oceania',
        marker=dict(color=color4)
    )
    mydata5 = go.Bar(
        x=results.loc['SA'].index,
        y=results.loc['SA'][continuous_var],
        name='South America',
        marker=dict(color=color5)
    )

    mylayout = go.Layout(
        title='Grouped bar chart',
        xaxis = dict(title = 'Total Litres of Pure Alcohol'), # x-axis label
        yaxis = dict(title = str(continuous_var)), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3,mydata4,mydata5], layout=mylayout)
    return fig


######### Run the app, good luck#########
if __name__ == '__main__':
    app.run_server(debug=True)
