from apscheduler.schedulers.background import BackgroundScheduler
from pages.search_page.page import dashboard_layout as dashboard_layout1
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import os
## Worker Start
from app import app
from engine.jobids import *
from engine.worker import startWorker
from engine.jobq import pushJob

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/search/' or pathname == '/search':
        return dashboard_layout1
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.server.route("/search/collect")
def do_the_thing():
    jobElsCollect()
    return "OK", 200

sched = BackgroundScheduler()
@sched.scheduled_job('interval', hours=1, id='DashWork')
def jobElsCollect():
    pushJob(CreateRedmineIndex)
    # pushJob(CreatePortalIndex)
    # pushJob(CreateNotionIndex)
    # pushJob(IngestRedmineData)
    # pushJob(IngestPortalData)


APP_DEBUG = os.getenv("DEBUG")
APP_USE_RELOADER = os.getenv("USE_RELOADER")
if __name__ == '__main__':
    # Run worker thread
    startWorker()
    # Run Scheduler
    sched.start()
    # Run Web server
    app.run_server(debug=APP_DEBUG, use_reloader=APP_USE_RELOADER, host="0.0.0.0")