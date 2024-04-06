import datetime
import os
import webbrowser
from typing import List

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from config_manage import ConfigManage
from dash import Dash, Input, Output, State, ctx, dash_table, dcc, html
from dash.dash import no_update
from dash.exceptions import PreventUpdate
from dcc_manage import DccManage
from df_manage import DfManage
from pandas.api.types import is_datetime64_dtype
from subscan import (
    SubscanStakingRewardDataProcess,
    SubscanStakingRewardsDataProcessForCryptact,
)

# Number of rows per page linking Data_table and DataFrame
ROW_PER_PAGE = 20

# Create the actual state (instance) of the application
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "dlSubscanStakingRewardsHistoryDash"

# Create an instance of a class that references config.ini
config_manage = ConfigManage()

# Create an instance of a class that references the [subscan_api_info] section
dcc_manage = DccManage(config_manage.subscan_api_info, config_manage.ui_info)
# Get key/value information for each section
token_data_list = dcc_manage.token_data_list
history_type_list = dcc_manage.history_type_list
sort_list = dcc_manage.sort_list
stk_type_list = dcc_manage.stk_type_list

# DataFrame object to be displayed in the data_table component at startup
data_list = [["data1", 1], ["data2", 2]]
df_base = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])

# Create an instance of a class that processes DataFrame Object
df_manage = DfManage()

# Layout definition
# Title(H3)
title_div = html.H3(
    "Download Subscan Staking&Rewards / Cryptact Custom",
    style={"margin-left": "5px", "margin-bottom": "10px", "margin-top": "5px"},
)

# Usage(Button)
info_div = html.Div(
    [
        # html.Button("Usage", id="submit_usage", n_clicks=0, style={"margin-right": "5px"}),
        # dbc.Button("Usage", id="submit_usage", n_clicks=0, color="primary", className="mr-2", size="sm",style={"margin-right": "5px"}),
        dbc.Button(
            "Usage",
            id="submit_usage",
            n_clicks=0,
            className="mr-2",
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
                "width": "100px",
            },
        ),
        html.Div(id="about_project_info", style={"display": "none"}),
        dbc.Button(
            "Subscan",
            id="submit_subscan_account_info",
            n_clicks=0,
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
                "width": "100px",
            },
        ),
        html.Div(id="subscan_account_info", style={"display": "none"}),
        # html.Button("Donate", id="submit_donate_info", n_clicks=0),
        dbc.Button(
            "Donate",
            id="submit_donate_info",
            n_clicks=0,
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
                "width": "100px",
            },
        ),
        html.Div(id="donate_info", style={"display": "none"}),
    ],
    style={"display": "inline-flex", "margin-bottom": "5px"},
)


# API key(Input & Button)
api_key_input_div = html.Div(
    [
        html.Div("API Key:", style={"font-weight": "bold", "margin-left": "5px"}),
        dcc.Input(
            id="input_api_key",
            type="password",
            placeholder="Enter your API key",
            value=config_manage.api_key_info,
            debounce=True,
            style={"margin-left": "5px", "width": "250px"},
        ),
        dbc.Button(
            "Set",
            id="submit_api_key",
            n_clicks=0,
            className="mr-2",
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
                "width": "60px",
            },
        ),
        html.Div(id="api_key_status", style={"margin-left": "5px"}),
    ],
    style={
        "display": "flex",
        "align-items": "center",
        "margin-bottom": "10px",
        "margin-top": "5px",
    },
)


# History type(RadioItems)
history_type_div = html.Div(
    [
        html.Div(
            [
                html.Div("Type:", style={"font-weight": "bold"}),
                dcc.RadioItems(
                    id="radio_history_type",
                    options=history_type_list,
                    value=history_type_list[0],
                    inline=True,
                    style={"margin-left": "5px"},
                    labelStyle={"margin-right": "2px"},
                ),
            ],
            style={
                "display": "inline-flex",
                "margin-bottom": "10px",
                "margin-left": "5px",
            },
        ),
        html.Div(""),
    ]
)

# Token & Sort(RadioItems)
token_sort_div = html.Div(
    [
        html.Div(
            [
                html.Div("Token:", style={"font-weight": "bold", "margin-left": "5px"}),
                dcc.Dropdown(
                    id="drop_down_div",
                    options=[dict(label=x, value=x) for x in token_data_list],
                    value=token_data_list[0],
                    clearable=False,
                    style={"margin-left": "5px", "width": "105px"},
                ),
                html.Div(
                    "StakingType:", style={"font-weight": "bold", "margin-left": "15px"}
                ),
                dcc.RadioItems(
                    id="stk_type",
                    options=stk_type_list,
                    value=stk_type_list[0],
                    inline=True,
                    style={"margin-left": "5px"},
                    labelStyle={"margin-right": "2px"},
                ),
                html.Div("Sort:", style={"font-weight": "bold", "margin-left": "15px"}),
                dcc.RadioItems(
                    id="radio_sort",
                    options=sort_list,
                    value=sort_list[0],
                    inline=True,
                    style={"margin-left": "5px"},
                    labelStyle={"margin-right": "2px"},
                ),
            ],
            style={
                "display": "inline-flex",
                "align-items": "center",
                "height": "30px",
                "margin-bottom": "10px",
            },
        ),
        html.Div(""),
    ]
)

# Acount Address(Input & Button)
address_input_div = html.Div(
    [
        html.Div(
            "Acount Address:", style={"font-weight": "bold", "margin-left": "5px"}
        ),
        dcc.Input(
            id="input_address",
            type="text",
            placeholder="Enter your acount address",
            value=config_manage.get_token_address_info(token_data_list[0]),
            size="58",
            style={"margin-left": "5px"},
        ),
        dbc.Button(
            "Set",
            id="set_account_address",
            n_clicks=0,
            className="mr-2",
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
                "width": "60px",
            },
        ),
        html.Div(id="account_address_status", style={"margin-left": "5px"}),
        html.Div("Input:", style={"font-weight": "bold", "margin-left": "5px"}),
        dcc.Input(
            id="input_num",
            type="number",
            value=50,
            min=1,
            max=5000,
            step=1,
            style={"margin-left": "5px"},
        ),
        # html.Button(
        #    "Submit",
        #    id="submit",
        #    n_clicks=0,
        #    style={"margin-left": "5px", "height": "30px", "background": "#cbe8fa"},
        # ),
        dbc.Button(
            "Submit",
            id="submit",
            n_clicks=0,
            className="mr-2",
            size="sm",
            style={
                "background": "#cbe8fa",
                "color": "rgb(50, 50, 50)",
                "margin-left": "5px",
            },
        ),
    ],
    style={"display": "inline-flex", "align-items": "center", "margin-bottom": "10px"},
)

# Select Table(Div)
select_table_div = html.Div(
    [
        html.Div(
            "Select Table Data: ", style={"font-weight": "bold", "margin-left": "5px"}
        ),
        html.Div(
            id="select_table_info",
            children="No Data Selection",
            style={"margin-left": "5px"},
        ),
    ],
    style={"display": "inline-flex"},
)

# Active cell info(Div)
active_cell_info_div = html.Div(
    [select_table_div], id="active_cell_info", style={"margin-bottom": "10px"}
)

# Response data(Div)
result_responsedata_info = html.Div(
    [
        html.Div(
            [
                html.Div(
                    "Response Data Info:",
                    style={"font-weight": "bold", "margin-left": "5px"},
                ),
                html.Div(
                    id="response_data_info",
                    children="No Response Data",
                    style={"margin-left": "5px"},
                ),
            ],
            style={"display": "inline-flex", "margin-bottom": "10px"},
        ),
        html.Div(""),
    ]
)

# Response data(Div)
result_responsedata_info_div = html.Div(
    [result_responsedata_info],
    id="result_responsedata_info_div",
    style={"display": "inline"},
)

# Table(dash_table.DataTable)
dash_data_table = html.Div(
    [
        html.Div(
            id="dash_table_title",
            children="",
            style={
                "color": "rgb(50, 50, 50)",
                "font-size": "115%",
                "margin-bottom": "10px",
                "margin-left": "5px",
            },
        ),
        dash_table.DataTable(
            id="data_table",
            columns=[dict(name=str(i), id=str(i)) for i in df_base.columns],
            data=df_base.to_dict("records"),
            fixed_rows=dict(headers=True, data=0),
            style_cell=dict(
                textAlign="left",
                minWidth="50px",
                width="130px",
                maxWidth="200px",
                overflow="hidden",
                textOverflow="ellipsis",
            ),
            style_header=dict(backgroundColor="paleturquoise", textAlign="center"),
            style_data=dict(backgroundColor="lavender"),
            sort_action="none",
            export_format="csv",
            page_size=10,
            style_table=dict(height="280px", overflowY="auto", marginLeft="5px"),
        ),
    ]
)

# Export(Button)
# Change the style of the export button
# https://community.plotly.com/t/styling-the-export-button-in-datatable/38798/9
# export_button = html.Button(
#    "Download CSV",
#    id="export_table",
#    style={
#        "backgroundColor": "paleturquoise",
#        "margin-top": "5px",
#    },
#    **{"data-text": ""},
# )

export_button = dbc.Button(
    "Download CSV",
    id="export_table",
    n_clicks=0,
    color="primary",
    className="mr-2",
    size="sm",
    style={
        "background": "#cbe8fa",
        "color": "rgb(50, 50, 50)",
        "margin-top": "5px",
        "margin-left": "5px",
        "width": "180px",
    },
)

show_graph_button = html.Button(
    "Show Graph",
    id="show_graph",
    style={"margin-top": "2px", "display": "none"},
    n_clicks=0,
)

# 2D-Graph(Div)
graph_div = html.Div(
    [
        dcc.Graph(id="date_cumsum_graph", style={"margin-left": "5px"}),
    ],
    id="graph_div",
    style={"display": "none"},
)

# Table & Export(Div & Button)
table_div = html.Div(
    [
        dash_data_table,
        export_button,
        graph_div,
        show_graph_button,
    ],
    id="table_div",
    style={"display": "none"},
)

# Error Dialog(ConfirmDialog)
confirm_dialog = html.Div(
    [
        dcc.ConfirmDialog(id="confirm_error_dialog", message=""),
        html.Div(id="confirm_dialog_div", style={"display": "none"}),
    ]
)

# Error Dialog for Subscan(ConfirmDialog)
confirm_dialog_subscan = html.Div(
    [
        dcc.ConfirmDialog(id="confirm_error_dialog_subscan", message=""),
        html.Div(id="confirm_dialog_subscan_div", style={"display": "none"}),
    ]
)

csv_div = html.Div(
    [
        dcc.Download(id="download_csv"),
        html.Div(id="csv_div", style={"display": "none"}),
    ]
)

usage_url_div = html.Div(
    id="usage_url_div",
    style={"display": "none", "margin-bottom": "10px"},
)

subscan_url_div = html.Div(
    id="subscan_url_div",
    style={"display": "none", "margin-bottom": "10px"},
)

donate_url_div = html.Div(
    id="donate_url_div",
    style={"display": "none", "margin-bottom": "10px"},
)

# Application Layout Definition
app.layout = html.Div(
    [
        title_div,
        info_div,
        usage_url_div,
        subscan_url_div,
        donate_url_div,
        api_key_input_div,
        history_type_div,
        token_sort_div,
        address_input_div,
        result_responsedata_info_div,
        active_cell_info_div,
        table_div,
        confirm_dialog,
        confirm_dialog_subscan,
        csv_div,
    ]
)


# Callbacks Definition
# Summary:
#  - Callback function to display API key status and update API key
#  - Update the value by pressing the Set button
#  - If the value is empty, it is updated with "".
@app.callback(
    Output("api_key_status", "children"),
    Output("input_api_key", "value"),
    Input("submit_api_key", "n_clicks"),
    State("input_api_key", "value"),
)
def update_api_key(n_clicks, api_key):
    if not ctx.triggered:
        # When loading application
        api_key = config_manage.api_key_info
        if api_key:
            # return "API key is set", api_key
            return "", api_key
        else:
            # return "API key is not set", ""
            return "", ""
    else:
        # When the Set button is clicked
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "submit_api_key" and n_clicks:
            config_manage.api_key_info = api_key
            if api_key:
                return "", api_key
            else:
                return "", ""
        else:
            raise PreventUpdate


# Callbacks Definition
# Summary:
#  - Callback function to Div / children triggered by ConfirmDialog / submit_n_clicks
#  - When an error occurs, a dialog is displayed, and when the OK button is pressed in the dialog,
#    the browser is redirected to the Subscan API Reference.
@app.callback(
    Output("confirm_dialog_div", "children"),
    Input("confirm_error_dialog", "submit_n_clicks"),
)
def check_confirm_dialog(submit_n_clicks):
    if submit_n_clicks and config_manage.is_error is False:
        # Open the Subscan API Document
        webbrowser.open("https://support.subscan.io/#http-status-codes")
        return no_update
    raise PreventUpdate


def is_docker():
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


# Callback function to Usage Div / children triggered by Usage Button / n_clicks
# Summary:
#  - Pressing the Usage button takes you to EADME.md on GitHub
#  - If it is in the Docker, use dcc.Link to display a clickable link.
@app.callback(
    Output("about_project_info", "children"),
    Output("usage_url_div", "children"),
    Output("usage_url_div", "style"),
    Input("submit_usage", "n_clicks"),
)
def open_url_about_project_info(n_clicks):
    if n_clicks:
        # Open the GitHub README.md
        url = "https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash#readme"
        if not is_docker():
            webbrowser.open(url)
            return no_update, no_update, {"display": "none"}
        else:
            usage_url_div_children = html.Div(
                [
                    html.Div(
                        "Please click the following Usage URL to open in your browser:",
                        style={"font-weight": "bold", "margin-left": "5px"},
                    ),
                    dcc.Link(
                        url, href=url, target="_blank", style={"margin-left": "5px"}
                    ),
                ]
            )
            usage_url_div_style = {"display": "block", "margin-bottom": "10px"}
            return no_update, usage_url_div_children, usage_url_div_style
    raise PreventUpdate


# Callback function to Doate Div / children triggered by Doate Button / n_clicks
# Summary:
#  - Pressing the Subscan button takes you to Staking&Rewards on Subscan.
#  - If it is in the Docker, use dcc.Link to display a clickable link.
@app.callback(
    Output("confirm_error_dialog_subscan", "displayed"),
    Output("confirm_error_dialog_subscan", "message"),
    Output("subscan_account_info", "children"),
    Output("subscan_url_div", "children"),
    Output("subscan_url_div", "style"),
    Input("submit_subscan_account_info", "n_clicks"),
    State("input_address", "value"),
    State("drop_down_div", "value"),
    State("stk_type", "value"),
)
def open_url_subscan_info(n_clicks, address, token, stk_type):
    # variable initialization
    is_error = False
    text = None
    confirm_dialog_flag = False
    subscan_url_div_style = {"display": "none"}

    # Push Subscan Button
    if n_clicks:
        token_fn = get_token_full_name(token)
        # Check StakingRewards Type Error
        is_error, text = is_stkrwd_type_support_check(token, stk_type)
        if is_error is True:
            confirm_dialog_flag = True
            message = text
            config_manage.is_error = True
            subscan_url_div_style = {"display": "none"}
            return (
                confirm_dialog_flag,
                message,
                no_update,
                no_update,
                subscan_url_div_style,
            )
        elif address == "":
            confirm_dialog_flag = True
            message = "Please input address"
            config_manage.is_error = True
            subscan_url_div_style = {"display": "none"}
            return (
                confirm_dialog_flag,
                message,
                no_update,
                no_update,
                subscan_url_div_style,
            )

        if stk_type == "Nominator":
            url = f"https://{token_fn}.subscan.io/reward?address={address}&role=account"
        elif stk_type == "NominationPool":
            url = f"https://{token_fn}.subscan.io/nomination_pool/paidout?address={address}"

        if not is_docker():
            webbrowser.open(url)
            return no_update, no_update, no_update, no_update, {"display": "none"}
        else:
            # Display the URL as a link in subscan_url_div
            subscan_url_div_children = html.Div(
                [
                    html.Div(
                        "Please click the following Subscan URL to open in your browser:",
                        style={"font-weight": "bold", "margin-left": "5px"},
                    ),
                    dcc.Link(
                        url, href=url, target="_blank", style={"margin-left": "5px"}
                    ),
                ]
            )
            subscan_url_div_style = {"display": "block", "margin-bottom": "10px"}
            return (
                no_update,
                no_update,
                no_update,
                subscan_url_div_children,
                subscan_url_div_style,
            )
    raise PreventUpdate


def get_token_full_name(token):
    match token:
        case "DOT":
            token_fn = "polkadot"
        case "KSM":
            token_fn = "kusama"
        case "ASTR":
            token_fn = "astar"
        case "MANTA":
            token_fn = "manta"
        case _:
            token_fn = ""
    return token_fn


# Callback function to Doate Div / children triggered by Doate Button / n_clicks
# Summary:
#  - Pressing the Usage button takes you to README.md on GitHub
@app.callback(
    Output("donate_info", "children"),
    Output("donate_url_div", "children"),
    Output("donate_url_div", "style"),
    Input("submit_donate_info", "n_clicks"),
)
def open_url_donate_info(n_clicks):
    if n_clicks:
        # Open the GitHub README.md
        url = "https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash?tab=readme-ov-file#donate"
        if not is_docker():
            webbrowser.open(url)
            return no_update, no_update, {"display": "none"}
        else:
            donate_url_div_children = html.Div(
                [
                    html.Div(
                        "Please click the following Donate URL to open in your browser:",
                        style={"font-weight": "bold", "margin-left": "5px"},
                    ),
                    dcc.Link(
                        url, href=url, target="_blank", style={"margin-left": "5px"}
                    ),
                ]
            )
            donate_url_div_style = {"display": "block", "margin-bottom": "10px"}
            return no_update, donate_url_div_children, donate_url_div_style
    raise PreventUpdate


# Callback function to Active Cell Div / children triggered by data_table / active_cell and page_current
# Summary:
#  - When active_cell is pressed, the response data (DataFrame object) corresponding to the cell is displayed in 'component_property:children'.
#  - When the page is switched, 'No Data Selection' is displayed. (because the cell is deselected)
@app.callback(
    Output("select_table_info", "children"),
    Input("data_table", "active_cell"),
    Input("data_table", "page_current"),
    Input("confirm_error_dialog", "submit_n_clicks"),
    Input("confirm_error_dialog", "cancel_n_clicks"),
)
def update_active_cell_info(
    active_cell, page_current, submit_n_clicks, cancel_n_clicks
):
    # Get df to reference in active cell
    df = df_manage.df_data

    # Set page information
    if page_current is None:
        page_num = 0
    else:
        page_num = page_current

    df_manage.df_page_num = page_num

    # Update page data for display
    show_page_num = page_num + 1

    # Error handling
    if df_manage.error_flag:
        text = "No Data Selection"
        df_manage.error_flag = False
        return text

    # Ccell selection judgment
    if active_cell:
        # With cell selection
        page_num = df_manage.df_page_num
        row = active_cell["row"] + page_num * ROW_PER_PAGE
        column = active_cell["column"]
        column_id = active_cell["column_id"]
        cell_data = df.iloc[row][active_cell["column_id"]]
        text = f"'{cell_data}' from table page: {show_page_num} row: {row} culumn: {column} column_id: {column_id}"
    else:
        # Without cell selection
        text = "No Data Selection"
    return text


# Specify custom data attributes as component_property
# https://community.plotly.com/t/moving-datatable-export-button-and-changing-text/39115/2
# app.clientside_callback(
#   """
#   function(n_clicks) {
#       if (n_clicks > 0)
#           document.querySelector('#data_table button.export').click()
#       return ''
#   }
#   """,
#   Output('csv_div', 'children'),
#   Input("export_table", "n_clicks"),
# )


@app.callback(
    Output("download_csv", "data"),
    Input("export_table", "n_clicks"),
    State("radio_history_type", "value"),
    State("drop_down_div", "value"),
    State("input_num", "value"),
    State("stk_type", "value"),
    prevent_initial_call=True,
)
def dl_csv(n_clicks, history_type, token, num, stk_type):
    if n_clicks > 0:
        df = df_manage.df_data
        df = df.astype(str)

        # pandas.DataFrame.to_csv method to output date in default format (YYYY-MM-DD HH:MM:SS)
        # "CryptactCustom" format converts the data format and adds single quotes
        if history_type == "CryptactCustom":
            df["Timestamp"] = "'" + pd.to_datetime(df["Timestamp"]).dt.strftime(
                "%Y/%m/%d %H:%M:%S"
            )

        d_today = datetime.date.today()

        return dcc.send_data_frame(
            df.to_csv,
            f"{token}_{history_type}_{stk_type}_N={num}_{d_today}.csv",
            index=False,
            header=True,
            encoding="utf-8-sig",
        )


# Callback function to Input Address Div / value triggered by Radioitems / value
# Summary:
#  - When a token is selected in the radio item,
#    the address corresponding to the token defined in config.ini is displayed in the "component_property:value" of the input tag.
@app.callback(
    Output("input_address", "value"),
    Input("drop_down_div", "value"),
)
def load_address(token):
    # Get Subscan API Info
    address = config_manage.get_token_address_info(token)
    return address


# Callback function to Input Address Div / value triggered by Radioitems / value
# Summary:
#  - Update the address for each token defined in app/config.toml
#  - Update the value by pressing the Set button
#  - If the value is empty, it is updated with "".
@app.callback(
    Output("account_address_status", "children"),
    Input("set_account_address", "n_clicks"),
    State("drop_down_div", "value"),
    State("input_address", "value"),
)
def update_address(n_clicks, token, input_address):
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "set_account_address" and n_clicks:
        config_manage.set_token_address_info(token, input_address)
        return no_update
    else:
        raise PreventUpdate


# Callback function to dash_table.DataTable and confirm_error_dialog  triggered by Submit Botton / n_clicks
# Summary:
#  - Response data received successfully
#    - Update and display component_property in dash_table.DataTable
#    - component_property: ConfirmDialog / data,columns,page_size,page_current,selected_cells,active_cell
#    - When the Submit button is pressed when a cell is selected, the data before execution remains, so it is updated with the specification to deselect the cell.
#    - page_current = 0,selected_cells = [],active_cell = None
#
#  - Response data reception failure
#    - Displays an error dialog and hides the table.
#    - component_property: ConfirmDialog / displayed,message , dash_table.DataTable / style
@app.callback(
    Output("confirm_error_dialog", "displayed"),
    Output("confirm_error_dialog", "message"),
    Output("dash_table_title", "children"),
    Output("data_table", "data"),
    Output("data_table", "columns"),
    Output("data_table", "page_size"),
    Output("data_table", "page_current"),
    Output("data_table", "selected_cells"),
    Output("data_table", "active_cell"),
    Output("response_data_info", "children"),
    Output("table_div", "style"),
    Output("graph_div", "style"),
    Input("submit", "n_clicks"),
    State("input_address", "value"),
    State("radio_history_type", "value"),
    State("drop_down_div", "value"),
    State("input_num", "value"),
    State("stk_type", "value"),
    State("radio_sort", "value"),
    prevent_initial_call=True,
)
def get_subscan_stkrwd(
    n_clicks, address, history_type, token, num, stk_type, sort_type
):
    # variable initialization
    is_error = False
    text = None
    confirm_dialog_flag = False
    list_num = 0
    response_data_info = ""
    supplement = ""

    # Check StakingRewards Type Error
    is_error, text = is_stkrwd_type_support_check(token, stk_type)

    if is_error is True:
        confirm_dialog_flag = True
        message = text
        response_data_info = ""
        config_manage.is_error = True
        return (
            confirm_dialog_flag,
            message,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            response_data_info,
            {"display": "none"},
            {"display": "none"},
        )

    # HTTP POST Request
    if history_type == "Reward&Slash":
        stkrwd = SubscanStakingRewardDataProcess(
            num, config_manage.subscan_api_info, token, address, stk_type, sort_type
        )
        (
            response_code,
            api_endpoint,
            response_status_code,
            _,
            _,
            df,
            list_num,
        ) = stkrwd.get_subscan_stakerewards()
    elif history_type == "CryptactCustom":
        cyrptactcustom = SubscanStakingRewardsDataProcessForCryptact(
            num,
            config_manage.subscan_api_info,
            config_manage.cryptact_info,
            token,
            address,
            stk_type,
            sort_type,
        )
        (
            response_code,
            api_endpoint,
            response_status_code,
            _,
            _,
            df,
            list_num,
        ) = cyrptactcustom.create_stakerewards_cryptact_cutom_df()

    # Check Response Data Error
    is_error, text = is_error_check(response_code, response_status_code, list_num)

    # Recieve data processing
    if is_error is True or list_num == 0:
        # Error handling
        df_manage.error_flag = True
        # Response data reception failure
        confirm_dialog_flag = True
        message = text
        response_data_info = "Error"
        return (
            confirm_dialog_flag,
            message,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            response_data_info,
            {"display": "none"},
            {"display": "none"},
        )
    else:
        # Response data received successfully
        # Set received data (DataFrame)
        df_manage.df_data = df

        # Round to the maximum number if the acquisition limit is exceeded
        if int(num) > int(len(df)):
            supplement = "(*Retrieved up to the upper limit of the history.)"

        text1 = f"API Endpoint: {api_endpoint}"
        text2 = f"HTTP Status Codes: {response_status_code}"
        text3 = f"Data Num: {len(df)}{supplement}"

        output_string = html.Div(
            [
                html.Div(children=text1),
                html.Div(children=text2),
                html.Div(
                    children=text3, style={"font-weight": "bold", "color": "#1e1eff"}
                ),
            ],
        )

        if n_clicks:
            # submit
            if history_type == "Reward&Slash":
                title = f"{history_type} / {token} dash_table(n={len(df)})"
            elif history_type == "CryptactCustom":
                title = f"{history_type} / {token} dash_table(n={len(df)})"
            dash_table_title_text = title
            # Numeric data displayed in DataTable is limited to 16 digits by default
            # Converting data (DataFrame) to string so that data with more than 16 digits can be displayed
            df = df.astype(str)
            data = df.to_dict("records")
            columns = [
                {"name": str(i), "id": str(i), "deletable": False, "renamable": False}
                for i in df.columns
            ]
            page_size = ROW_PER_PAGE
            page_current = 0
            selected_cells: List[str] = []
            active_cell = None
            response_data_info = output_string
            return (
                confirm_dialog_flag,
                no_update,
                dash_table_title_text,
                data,
                columns,
                page_size,
                page_current,
                selected_cells,
                active_cell,
                response_data_info,
                {"display": "inline"},
                {"display": "inline"},
            )
    raise PreventUpdate


# error-determining function
def is_stkrwd_type_support_check(token, stk_type):
    error_messages = {
        "ASTR": "ASTR does not support NominationPool.\nPlease submit the Nominator specification.\n",
        "MANTA": "MANTA does not support NominationPool.\nPlease submit the Nominator specification.\n",
    }

    result = token in error_messages and stk_type == "NominationPool"
    text = error_messages.get(token, "")

    return result, text


# error-determining function
def is_error_check(response_code, response_status_code, list_num):
    result = False
    text = ""
    open_url_text1 = ""
    open_url_text2 = ""
    if not is_docker():
        open_url_text1 = "Click OK button to go to the Subscan API Documents page.\n"
        open_url_text2 = f"Open URL?({config_manage.subscan_api_doc})\n"
    # Response data error judgment processing
    # code error (other than success)
    if response_code != 0:
        text = (
            f"HTTP Status Codes: {response_code}\n"
            "Error Details: Invalid Account Address.\n"
            "Please Check Account Address.\n\n"
            f"{open_url_text1}"
            f"{open_url_text2}"
        )
        result = True
    # HTTP Status Codes Error
    elif response_status_code != 200:
        text = (
            f"HTTP Status Codes: {response_status_code}\n"
            "Please Check Subscan API Documents.\n\n"
            f"{open_url_text1}"
            f"{open_url_text2}"
        )
        result = True
    # Error when no data received
    elif list_num == 0:
        text = (
            "Response data could not be retrieved.\n"
            "Please Check Account Address or Response data.\n\n"
            f"{open_url_text1}"
            f"{open_url_text2}"
        )
        result = True
    return result, text


# Callback function to display graph
# Summary:
#  - Callback function to date_cumsum_graph(Graph) children triggered by dash_table_title(Div) children.
#  - Stop callback when children attribute is empty.
#  - When the children attribute is updated, a two-dimensional graph of date/time and staking data is created and displayed from the DataFrame object obtained by the Subscan API.
@app.callback(
    Output("date_cumsum_graph", "figure"),
    # Input("show_graph", "n_clicks"),
    Input("dash_table_title", "children"),
    State("drop_down_div", "value"),
    State("radio_history_type", "value"),
    State("stk_type", "value"),
    State("radio_sort", "value"),
)
def display_graph(children, token, history_type, stk_type, sort_type):
    if children == "":
        raise PreventUpdate
    else:
        # Obtain data for graph display
        df = df_manage.df_data

        # Create graph sorting information
        if sort_type == "Ascending":
            graph_sort_type = True
        else:
            graph_sort_type = False

        # Create layout information for each historical information
        if history_type == "Reward&Slash":
            title = f"{history_type} / {token} / Cumulative Sum Value Date Graph(n={len(df)})"
            if stk_type == "Nominator":
                xaxis_data = "Date"
                yaxis_data = "Value"
            elif stk_type == "NominationPool":
                xaxis_data = "Time"
                yaxis_data = "Value"
        elif history_type == "CryptactCustom":
            title = f"{history_type} / {token} / Cumulative Sum Volume Timestamp Graph(n={len(df)})"
            xaxis_data = "Timestamp"
            yaxis_data = "Volume"

        # Create Layout
        ts_layout = go.Layout(
            title=dict(
                text=title,
                font=dict(size=19, color="rgb(50, 50, 50)"),
                x=0,
            ),
            # Display legend on graph
            showlegend=True,
            legend=dict(
                xanchor="left",
                yanchor="bottom",
                x=0.005,
                y=0.89,
                orientation="h",
            ),
            height=600,
            # Display Range Slider and Selector
            xaxis={
                "title": xaxis_data,
                "rangeslider": {"visible": True},
                "rangeselector": {
                    "buttons": [
                        {
                            "label": "7d",
                            "step": "day",
                            "count": 7,
                            "stepmode": "backward",
                        },
                        {
                            "label": "1m",
                            "step": "month",
                            "count": 1,
                            "stepmode": "backward",
                        },
                        {"step": "all"},
                    ]
                },
            },
            yaxis={
                "title": yaxis_data,
            },
        )

        # Create object of type datetime
        if not is_datetime64_dtype(df[xaxis_data]):
            df[xaxis_data] = pd.to_datetime(df[xaxis_data].str.replace("'", ""))

        # Sort Data
        num = len(df)
        sort_Column = list(range(num))
        df = df.assign(SortColumn=sort_Column)
        df = df.sort_values("SortColumn", ascending=graph_sort_type)
        df = df.drop("SortColumn", axis=1)
        df[yaxis_data] = df[yaxis_data].astype(float)
        df["cum_sum_data"] = df[yaxis_data].cumsum()
        df = df.reset_index()

        # Create Trace
        trace = go.Scatter(
            name=yaxis_data,
            x=df[xaxis_data],
            y=df["cum_sum_data"],
            mode="markers+lines",
            hovertemplate=f"{xaxis_data}:"
            + "%{x|%Y-%m-%d}<br>Cumsum:%{y:.1f}<br>%{customdata}<extra></extra>",
            customdata=[f"{yaxis_data}:{yd:.1f}" for yd in df[yaxis_data]],
            # Colorize from y=0 to data
            fill="tozeroy",
        )

        # Create graph with specified trace and layout
        fig = go.Figure(
            data=trace,
            layout=ts_layout,
        )

        # Update Scale
        fig.update_layout(
            xaxis=dict(range=[df[xaxis_data].min(), df[xaxis_data].max()]),
            yaxis=dict(range=[df["cum_sum_data"].min(), df["cum_sum_data"].max()]),
        )

        return fig


if __name__ == "__main__":
    # To allow access from other computers on the local network
    app.run(debug=False, host="0.0.0.0", port=8050)
    # To allow access only from your own computer
    # If you want to use the Dash Dev Tools, set dev_tools_ui=True.
    # app.run(debug=True, dev_tools_ui=False)
