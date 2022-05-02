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
# dashboard_layout = html.Div([
#     html.H1("이슈 통합 검색기"),
#     html.Div([
#         "검색 단어 : ",
#         dcc.Input(id='my-input', placeholder="단어를 입력 해주세요.", type='text', debounce=True)
#     ]),
#     html.Br(),
#     html.Div(id='my-output'),
# ])
# options = ["Redmine", "Portal", "Notion"]

# def generate_table(dataframe, max_rows=30):
#     df_drop_link = dataframe.drop(columns='url')

#     body_content  = []
#     for i in range(min(len(dataframe), max_rows)):
#         for col in df_drop_link.columns:
#             if col == '이슈번호':
#                 body_content.append(html.Td(html.A(href=dataframe.iloc[i]['url'], children=dataframe.iloc[i][col], target='_blank'),style={'width':'80px','border': '1px solid'}))
#             elif col == '상세설명':
#                 body_content.append(html.Td(dataframe.iloc[i][col],style={'width':'200em','border': '1px solid',"white-space":"break-spaces",'overflow': 'auto','word-break': 'normal','word-wrap': 'break-word'}))
#             # elif col == '제목':
#             #     body_content.append(html.Td(dataframe.iloc[i][col],style={'width':'30em','border': '1px solid'}))
#             else: 
#                 body_content.append(html.Td(dataframe.iloc[i][col],style={'width':'100px','border': '1px solid','backgroundColor': 'red','color': 'white'}))

#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in df_drop_link.columns]) ] +
#         # Body
#         [html.Tr(
#             body_content
#         )]
#     )
#     return dash_table.DataTable(
#     style_data={
#         'whiteSpace': 'normal',
#         'height': 'auto',
#         'lineHeight': '15px',
#         'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
#     },
#     data=dataframe.to_dict('records'),
#     columns=[{'id': c, 'name': c} for c in dataframe.columns],
#     style_cell={
#         'overflow': 'hidden',
#         'textOverflow': 'ellipsis',
#         # 'maxWidth': 0
#     },
#     style_data_conditional=[
#         {
#             'if': {
#                 'column_id': '이슈번호',
#             },
#             'width': '5%',
#         },
#         {
#             'if': {
#                 'column_id': '제목',
#             },
#             'width': '30%',
#         },
#         {
#             'if': {
#                 'column_id': '매치율',
#             },
#             'width': '10%',
#             'backgroundColor': '#85144b',
#             'color': 'white'
#         },{
#             'if': {
#                 'column_id': '상세설명',
#             },
#             'width': '50%',
#         }
#     ]
# )

def search(keyword=None):
    body =  {
        "query": {
            "multi_match": {
                "type": "best_fields",
                "fields": [
                    "subject", 
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
        "highlight" : {
            "type": "unified",
            "require_field_match": False,
            "number_of_fragments": 0,
            "fields" : {
                "*" : { "pre_tags" : ["<mark>"], "post_tags" : ["</mark>"] }
            }
        }
    }

    es = Elasticsearch("http://elasticsearch:9200")
    res = es.search(index='issues',body=body)
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