# import libraries required for dash app
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

harvest=pd.read_excel("harvest.xlsx", sheet_name=2)

baseline=pd.read_excel("harvest.xlsx", sheet_name=0)

combined = harvest.merge(baseline, on="Land ID", suffixes=( "", "_B"))

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app=Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc_css])
server = app.server

load_figure_template("CERULEAN")


app.layout=dbc.Container([
    dcc.Tabs(className="dbc", children=[
        dbc.Tab(label="Respondents", children=[
            html.Br(),
            html.H4(id="map1_title", style={"textAlign": "center"}),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Markdown("**Select a District:**"),
                        dcc.Dropdown(
                            id='dropdown',
                            options=[{'label': i, 'value': i} for i in harvest.District.unique()],
                            value=[],
                            className="dbc"
                        ),

                        # dcc.Markdown("**Select Age Range:**"),
                        # dcc.RangeSlider(
                        #     id='slider',
                        #     min = harvest.Age.min(),
                        #     max = harvest.Age.max(),
                        #     value = [],
                        #     step=1,
                        #     marks={int(harvest.Age.min()): str(harvest.Age.min()),
                        #             20: "20",
                        #             25: "25",
                        #             30: "30",
                        #             35: "35",
                        #             40: "40",
                        #             45: "45",
                        #             50: "50",
                        #             int(harvest.Age.max()): str(harvest.Age.max())},
                        #     className="dbc"
                        # ),

                    ])
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='graph1')
                ], width=8)
            ]),
            
            
        ]), # End of Tab 1

        dbc.Tab(label="Baseline vs Current", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.Br(),
                        dcc.Markdown("**Select a District:**"),
                        dcc.Checklist(
                            id='checklist_district',
                            options=[{'label': i, 'value': i} for i in sorted(harvest.District.unique())],
                            value=[],
                            className="dbc"
                        ),

                        dcc.Markdown("**Select Type of Crops:**"),
                        dcc.Checklist(
                            id='checklist_crops',
                            options=[{'label': i, 'value': i} for i in harvest.Crops.unique()],
                            value=[],
                            className="dbc"
                        ),

                    ])
                ], width=4),
                dbc.Col([
                    html.Br(),
                    html.H4(id="map2_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph2', style={'height': '37.5vh'}), # To control the height of the graph
                    html.H4(id="map3_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph3', style={'height': '37.5vh'}) # To control the height of the graph
                ], width=8)
            ]),                       
        ]), # End of Tab 2

        dbc.Tab(label="Satisfaction & Impact Perception", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.Br(),
                        dcc.Markdown("**Select a District:**"),
                        dcc.Checklist(
                            id='checklist_district_satisfaction',
                            options=[{'label': i, 'value': i} for i in sorted(harvest.District.unique())],
                            value=[],
                            className="dbc"
                        ),

                        # dcc.Markdown("**Select Age Range:**"),
                        # dcc.RangeSlider(
                        #     id='slider_satisfaction',
                        #     min = harvest.Age.min(),
                        #     max = harvest.Age.max(),
                        #     value = [],
                        #     step=1,
                        #     marks={harvest.Age.min(): str(harvest.Age.min()),
                        #            20: "20",
                        #            25: "25",
                        #             30: "30",
                        #             35: "35",
                        #             40: "40",
                        #             45: "45",
                        #             50: "50",
                        #            harvest.Age.max(): str(harvest.Age.max())},
                        #     className="dbc"
                        # ),

                    ])
                ], width=4),
                dbc.Col([
                    html.Br(),
                    html.H4(id="map4_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph4', style={'height': '37.5vh'}), # To control the height of the graph
                    html.H4(id="map5_title", style={"textAlign": "center"}),
                    html.Br(),
                    dcc.Graph(id='graph5', style={'height': '37.5vh'}), # To control the height of the graph
                ], width=8)
            ]),            
        ]) # End of Tab 3
        
    ])
])
        

@app.callback(
        Output('map1_title', 'children'),
        Output('graph1', 'figure'),
        Input('dropdown', 'value'),
        # Input('slider', 'value')
)

def update_figure1(district): #removed age from the function
    
    if not district:
        title = "Gender Distribution of All Respondents"
        df = harvest

    else: # district and not age: # changed from elif to else
        title = f"Gender Distribution of Respondents in {district}"
        df = harvest.query('District in @district')
    
    # elif not district and age:
    #     title = f"Gender Distribution of Respondents between age {age[0]} and {age[1]}"
    #     df = harvest[harvest['Age'].between(age[0], age[1])]
    
    # else:
    #     title = f"Gender Distribution of Respondents in {district} between age {age[0]} and {age[1]}"
    #     df = harvest.query('District in @district').query('Age >= @age[0] and Age <= @age[1]')

    
    # Calculate the maximum count of respondents
    max_count = df.groupby(["Gender"]).size().max()

    # Calculate the step size based on the maximum count and the desired number of ticks
    step_size = max(1, max_count // 6)

    # Generate the tick values by starting from 0 and incrementing by the step size
    tickvals = list(range(0, max_count + 2, step_size))

    fig=px.bar(
        (df
         .groupby(["Gender"])
         .size()
         .reset_index(name = "count")
        ),
        x="Gender",
        y="count",
    ).update_traces(
        marker_color=['hotpink', 'cornflowerblue'], 
        width=0.5).update_xaxes(
        tickvals=[0, 1],
        ticktext = ["Female", "Male"]
    ).update_yaxes(
        title_text = "Number of Respondents", 
        tickformat='d',
        tickvals=tickvals  # Add this line 
              
    )
        
    return title, fig

@app.callback(
        Output('map2_title', 'children'),
        Output('graph2', 'figure'),
        Input('checklist_district', 'value'),
        Input('checklist_crops', 'value')
)

def update_figure2(district, crop): 
    
    if not district and not crop:
        title = "Total Baseline vs Current Yield in All Districts"
        df = combined

    elif district and not crop:
        title = f"Baseline vs Current Yield in Selected District/s"
        df = combined.query('District in @district')
    
    elif not district and crop:
        title = f"Baseline vs Current Yield in All Districts for Selected Crop/s"
        df = combined.query('Crops in @crop')
    
    else:
        title = f"Baseline vs Current Yield in Selected District/s for Selected Crop/s"
        df = combined.query('District in @district').query('Crops in @crop')



    fig=px.bar(
        df.groupby("District").agg({"Updated Yield": "sum", "Baseline Yield": "sum"}).reset_index().rename(columns={"Updated Yield": "Current Yield"}),
        x="District",
        y=["Baseline Yield", "Current Yield"],
        barmode="group",
        labels={"value": "Yield (kg)", "variable": "Yield Type"},
        color_discrete_sequence=["orange", "cornflowerblue"]
    ).update_yaxes(
        tickformat='d'
    )
        
    return title, fig


@app.callback(
        Output('map3_title', 'children'),
        Output('graph3', 'figure'),
        Input('checklist_district', 'value'),
        Input('checklist_crops', 'value')
)

def update_figure3(district, crop): 
    
    if not district and not crop:
        title = "Total Baseline vs Current Agricultural Income in All Districts"
        df = combined

    elif district and not crop:
        title = f"Baseline vs Current Agricultural Income in Selected District/s"
        df = combined.query('District in @district')
    
    elif not district and crop:
        title = f"Baseline vs Current Agricultural Income in All Districts for Selected Crop/s"
        df = combined.query('Crops in @crop')
    
    else:
        title = f"Baseline vs Current Agricultural Income in Selected District/s for Selected Crop/s"
        df = combined.query('District in @district').query('Crops in @crop')


    fig=px.bar(
        df.groupby("District").agg({"Updated Income from Agriculture": "sum", "Baseline Income from Agriculture": "sum"}).reset_index().rename(columns={"Updated Income from Agriculture": "Current Income",
                                                                                                                                                        "Baseline Income from Agriculture": "Baseline Income"}),
        x="District",
        y=["Baseline Income", "Current Income"],
        barmode="group",
        labels={"value": "Income (USD)", "variable": "Income Type"},
        color_discrete_sequence=["orange", "cornflowerblue"]
    ).update_yaxes(
        tickformat='d'
    )
        
    return title, fig


@app.callback(
        Output('map4_title', 'children'),
        Output('graph4', 'figure'),
        Input('checklist_district_satisfaction', 'value'),
        # Input('slider_satisfaction', 'value')
)


def update_figure4(district): #removed age from the function

    # Replace 'F' and 'M' with 'Female' and 'Male'
    harvest['Gender'] = harvest['Gender'].replace({'F': 'Female', 'M': 'Male'})
    
    if not district:
        title = "Overall Community Satisfaction Level by Gender"
        df = harvest

    else: # district and not age:
        title = f"Community Satisfaction Level in {district}"
        df = harvest.query('District in @district')
    
    # elif not district and age:
    #     title = f"Community Satisfaction Level of Respondents between age {age[0]} and {age[1]}"
    #     df = harvest[harvest['Age'].between(age[0], age[1])]
    
    # else:
    #     title = f"Community Satisfaction Level of Respondents in {district} between age {age[0]} and {age[1]}"
    #     df = harvest.query('District in @district').query('Age >= @age[0] and Age <= @age[1]')
   

    fig=px.bar(
        df.groupby(["District", "Gender"]).agg({"Satisfaction": "mean"}).reset_index(),
        x="District",
        y=["Satisfaction"],
        color="Gender",
        barmode="group",
        labels={"value": "Satisfaction Level", "variable": "Gender"},
        color_discrete_map={"Female": "hotpink", "Male": "cornflowerblue"},
        # hover_data={"Satisfaction": ":.2f"}  # Add this line
    ).update_yaxes(
        tickformat='.2f',
        range=[0, 5] # to make y ticks to 5
    ).update_layout(
    annotations=[
        dict(
            x=0,
            y=1.15,
            showarrow=False,
            text="<i>Measured on a Scale of 1 to 5<i>",
            xref="paper",
            yref="paper",
            font=dict(
                color="brown"  # Change the color to your desired color
            )
        )
    ]
)
        
    return title, fig


@app.callback(
        Output('map5_title', 'children'),
        Output('graph5', 'figure'),
        Input('checklist_district_satisfaction', 'value'),
        # Input('slider_satisfaction', 'value')
)


def update_figure5(district): #removed age from the function

    # Replace 'F' and 'M' with 'Female' and 'Male'
    harvest['Gender'] = harvest['Gender'].replace({'F': 'Female', 'M': 'Male'})
    
    if not district:
        title = "Overall Impact Perception Level by Gender"
        df = harvest

    else: # district and not age:
        title = f"Impact Perception Level in {district}"
        df = harvest.query('District in @district')
    
    # elif not district and age:
    #     title = f"Impact Perception Level of Respondents between age {age[0]} and {age[1]}"
    #     df = harvest[harvest['Age'].between(age[0], age[1])]
    
    # else:
    #     title = f"Impact Perception Level of Respondents in {district} between age {age[0]} and {age[1]}"
    #     df = harvest.query('District in @district').query('Age >= @age[0] and Age <= @age[1]')
   

    fig=px.bar(
        df.groupby(["District", "Gender"]).agg({"Perception": "mean"}).reset_index(),
        x="District",
        y=["Perception"],
        color="Gender",
        barmode="group",
        labels={"value": "Impact Perception Level", "variable": "Gender"},
        color_discrete_map={"Female": "hotpink", "Male": "cornflowerblue"},
        # hover_data={"Satisfaction": ":.2f"}  # Add this line
    ).update_yaxes(
        tickformat='.2f',
        range=[0, 5] # to make y ticks to 5
    ).update_layout(
    annotations=[
        dict(
            x=0,
            y=1.15,
            showarrow=False,
            text="<i>Measured on a Scale of 1 to 5<i>",
            xref="paper",
            yref="paper",
            font=dict(
                color="brown"  # Change the color to your desired color
            )
        )
    ]
)
        
    return title, fig

# if __name__ == '__main__':
#     app.run_server(debug=True)
