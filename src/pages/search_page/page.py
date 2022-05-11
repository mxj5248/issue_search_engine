import dash 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app 
import requests
import json
import pandas as pd
from dash import Dash, dash_table
from IPython.display import HTML
from elasticsearch import Elasticsearch

######################
#                    #
#  dashboard_layout  #
#                    #
######################

def search(keyword=None):
    body =  {
        "size" : 50,
        "query": {
            "multi_match": {
                "type": "best_fields",
                "fields": [
                    "subject^2", 
                "description"
            ],
                "query": keyword,
            }
        },
    # }
        # "highlight": {
        #     "fragment_size": 150,
        #     "fields": {
        #         "subject": {},
        #         "description": {}
        #     }
        # },
        # "highlight" : {
        #     "type": "unified",
        #     "require_field_match": False,
        #     "number_of_fragments": 0,
        #     "fields" : {
        #         "*" : { "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
        #     }
        # }
    }

    es = Elasticsearch("http://elasticsearch:9200")
    # res = es.search(index=['idx_redmine','idx_portal','idx_notion'],body=body)
    res = es.search(index="idx_*",body=body)
    return res
    
dashboard_layout= html.Div([
    dbc.Navbar(
    dbc.Container(
            [
            html.Div(dbc.NavbarBrand("이슈 통합 검색기", href="#"),style={'width': '20%','text-align':'left'}),
            html.Div(dcc.Input(id='my-input', type="text", placeholder="Search here",debounce=True,style={'width': '100%'}),style={'width': '70%'}),
            html.Div(dbc.Button("검색", color="primary", className="me-1"))
            ],
        ),
    color="dark",
    dark=True,
    ),
    html.Br(),
    # html.Div(className='row',id='my-output',style={'display' : 'flex','margin-left': '10px','margin-right': '10px'})
    html.Div(id='my-output',style={'margin-left': '10px','margin-right': '10px'})

])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    r = search(input_value)
    rows = r['hits']['hits']
    results = []
    # input_address = 'http://elasticsearch:9200/issues/_search?q='+input_value
    # res = requests.get(input_address)
    # json_data = res.json()
    # rows = json_data['hits']['hits']
    # results = []
    for r in rows: 
        subresults=[]
        subresults.append(html.H5(className="card-title",children=[r['_source']['subject']]))
        subresults.append(html.H6(className="card-subtitle mb-2 text-muted",children= ["이슈 번호 : " + str(r['_source']['id'])]))
        if len(r['_source']['description']) > 300:
            subresults.append(html.P(className="card-text",children=[r['_source']['description'][:300]+'...']))
        else: subresults.append(html.P(className="card-text",children=[r['_source']['description']]))
        results.append(html.Div(className="card",children=html.Div(className="card-body",children=subresults),style = {"width" : "100rem"}))
    return results
        # data = {}
        # data["매치율"] = [str(r['_score'])]
        # df['url'] = df['이슈번호'].apply(lambda x: "https://redmine.netand.co.kr/issues/"+x)
        # results.append(generate_table(df))




# @app.callback(
#     Output("site-checklist", "value"),
#     Output("all-checklist", "value"),
#     Input("site-checklist", "value"),
#     Input("all-checklist", "value"),
# )
# def sync_checklists(sites_selected, all_selected):
#     ctx = dash.callback_context
#     input_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     if input_id == "site-checklist":
#         all_selected = ["All"] if set(sites_selected) == set(options) else []
#     else:
#         sites_selected = options if all_selected else []
#     return sites_selected, all_selected