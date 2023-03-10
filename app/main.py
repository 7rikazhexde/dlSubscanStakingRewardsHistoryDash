import webbrowser
import pandas as pd
from dash import Dash, html, Input, Output, dash_table, dcc, State
from subscan import SubscanStakingRewardDataProcess
from subscan import SubscanStakingRewardsDataProcessForCryptact
from df_manage import DfManage
from config_manage import ConfigManage
from dcc_manage import DccManage
from dash.exceptions import PreventUpdate
from dash.dash import no_update

# Number of rows per page linking Data_table and DataFrame
ROW_PER_PAGE = 20

# Create the actual state (instance) of the application
app = Dash(__name__,suppress_callback_exceptions = True)

# Create an instance of a class that references config.ini
config_manage = ConfigManage()

# Create an instance of a class that references the [subscan_api_info] section
dcc_manage = DccManage(config_manage.subscan_api_info,config_manage.ui_info)
# Get key/value information for each section
token_data_list = dcc_manage.token_data_list
history_type_list = dcc_manage.history_type_list
sort_list = dcc_manage.sort_list

# DataFrame object to be displayed in the data_table component at startup
data_list = [['data1',1],['data2',2]] 
df_base = pd.DataFrame(data_list,columns=['culumn1','culumn2'])

# Create an instance of a class that processes DataFrame Object
df_manage = DfManage()

# Layout definition
# Title(H3)
title_div = html.H3('Download Subscan Staking&Rewards / Cryptact Custom')

# Usage(Button)
about_project_info = html.Div(
    [
        html.Button('Usage', id='submit_usage', n_clicks=0),
        html.Div(id='about_project_info', style={'display':'none'}),
    ],
    style={'display':'inline-flex'}
)

# History type(RadioItems)
history_type_div = html.Div(
    [
    html.Div(
        [
            html.Div('Type:',style={'font-weight': 'bold'}),
            dcc.RadioItems(id='radio_history_type',options=history_type_list, value=history_type_list[0], inline=True),
        ],
        style={'display':'inline-flex','margin-bottom': '10px'}
    ),
    html.Div(''),
    ]
)

# Token & Sort(RadioItems)
token_sort_div = html.Div(
    [
    html.Div(
        [
            html.Div('Token:',style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='drop_down_div',
                options=[dict(label=x,value=x) for x in token_data_list],
                value=token_data_list[0],
                clearable=False,
                style={'margin-left': '5px','width': '105px'}
            ),
            html.Div('Sort:',style={'font-weight': 'bold','margin-left': '15px'}),
            dcc.RadioItems(id='radio_sort',options=sort_list, value=sort_list[0], inline=True),
        ],
        style={'display':'inline-flex','align-items': 'center','height':'30px','margin-bottom': '10px'}
    ),
    html.Div(''),
    ]
)

# Acount Address(Input & Button)
address_input_div = html.Div(
    [
        html.Div('Acount Address:',style={'font-weight': 'bold'}),
        dcc.Input(id='input_address',type='text',placeholder="",value=config_manage.get_subscan_api_info_address(token_data_list[0]),size='58',style={'margin-left': '5px','height':'25px'}),
        html.Div('Input:',style={'font-weight': 'bold','margin-left': '5px'}),
        dcc.Input(id='input_num',type='number',value=50 ,min=1, max=5000, step=1,style={'margin-left': '5px','height':'25px'}),
        html.Button('Submit', id='submit', n_clicks=0,style={'margin-left': '5px','height':'30px'}),
    ],
    style={'display':'inline-flex','align-items': 'center','margin-bottom': '10px'}
)

# Select Table(Div)
select_table_div = html.Div(
    [
        html.Div('Select Table Data: ',style={'font-weight': 'bold'}),
        html.Div(id='select_table_info',children='No Data Selection',style={'margin-left': '5px'})
    ],
    style={'display':'inline-flex'}
)

# Active cell info(Div)
active_cell_info_div = html.Div([select_table_div],id='active_cell_info',style={'margin-bottom': '10px'})

# Response data(Div)
result_responsedata_info = html.Div(
    [
    html.Div(
        [
            html.Div('Response Data Info:',style={'font-weight': 'bold'}),
            html.Div(id='response_data_info',children='No Response Data',style={'margin-left': '5px'})
        ],
        style={'display':'inline-flex','margin-bottom': '10px'}
    ),
    html.Div(''),
    ]
)

# Response data(Div)
result_responsedata_info_div = html.Div(
    [
        result_responsedata_info
    ],
    id='result_responsedata_info_div',style={'display':'inline'}
)

# Table(dash_table.DataTable)
dash_data_table = dash_table.DataTable(
    id='data_table',
    columns=[dict(name=str(i),id=str(i))  for i in df_base.columns],
    data=df_base.to_dict('records'),
    fixed_rows=dict(headers=True,data=0),
    style_cell=dict(
        textAlign='left',
        minWidth='50px',
        width='100px',
        maxWidth='200px',
        overflow='hidden',
        textOverflow='ellipsis',
    ),
    style_header=dict(backgroundColor='paleturquoise',textAlign='center'),
    style_data=dict(backgroundColor='lavender'),
    sort_action='none',
    export_format='csv',
    page_size = 10,
    style_table=dict(height='280px',overflowY='auto')
)

# Export(Button)
# Change the style of the export button
# https://community.plotly.com/t/styling-the-export-button-in-datatable/38798/9
export_button = html.Button(
    'CSV Dwonload', 
    id='export_table',
    style={'backgroundColor': 'paleturquoise','margin-top': '10px'}, 
    **{'data-text': ''}
)

# Table & Export(Div & Button)
table_div = html.Div(
    [
    dash_data_table,
    export_button
    ],
    id='table_div',style={'display':'none'}
)

# Error Dialog(ConfirmDialog)
confirm_dialog = html.Div(
    [
        dcc.ConfirmDialog(id='confirm_error_dialog',message=''),
        html.Div(id='confirm_dialog_div', style={'display':'none'}),
    ]
)

# Application Layout Definition
app.layout = html.Div([
    title_div,
    about_project_info,
    history_type_div,
    token_sort_div,
    address_input_div,
    result_responsedata_info_div,
    active_cell_info_div,
    table_div,
    confirm_dialog
])

# Callbacks Definition
# Summary:
#  - Callback function to Div / children triggered by ConfirmDialog / submit_n_clicks
#  - When an error occurs, a dialog is displayed, and when the OK button is pressed in the dialog, 
#    the browser is redirected to the Subscan API Reference.
@app.callback(
    Output('confirm_dialog_div', 'children'),
    Input('confirm_error_dialog', 'submit_n_clicks')
)
def check_confirm_dialog(submit_n_clicks):
    if submit_n_clicks:
        # Open the Subscan API Document
        webbrowser.open('https://support.subscan.io/#http-status-codes')
        return no_update
    raise PreventUpdate

# Callback function to Usage Div / children triggered by Usage Button / n_clicks
# Summary: 
#  - Pressing the Usage button takes you to EADME.md on GitHub
@app.callback(
    Output('about_project_info', 'children'), 
    Input('submit_usage', 'n_clicks')
)
def open_url(n_clicks):
    if n_clicks:
        # Open the GitHub README.md
        webbrowser.open('https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash#readme')
        return no_update
    raise PreventUpdate

# Callback function to Active Cell Div / children triggered by data_table / active_cell and page_current
# Summary:
#  - When active_cell is pressed, the response data (DataFrame object) corresponding to the cell is displayed in 'component_property:children'.
#  - When the page is switched, 'No Data Selection' is displayed. (because the cell is deselected)
@app.callback(
    Output('select_table_info', 'children'), 
    Input('data_table', 'active_cell'),
    Input('data_table', 'page_current'),
    Input('confirm_error_dialog', 'submit_n_clicks'),
    Input('confirm_error_dialog', 'cancel_n_clicks')
)
def update_active_cell_info(active_cell,page_current,submit_n_clicks,cancel_n_clicks):
    
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
        text = 'No Data Selection'
        df_manage.error_flag = False
        return text

    # Ccell selection judgment
    if active_cell:
        # With cell selection
        page_num = df_manage.df_page_num
        row = active_cell['row'] + page_num * ROW_PER_PAGE
        column = active_cell['column']
        column_id = active_cell['column_id']
        cell_data = df.iloc[row][active_cell['column_id']]
        text = f'\'{cell_data}\' from table page: {show_page_num} row: {row} culumn: {column} column_id: {column_id}'
    else:
        # Without cell selection
        text = 'No Data Selection'
    return text

# Specify custom data attributes as component_property
# https://community.plotly.com/t/moving-datatable-export-button-and-changing-text/39115/2
app.clientside_callback(
    '''
    function(n_clicks) {
        if (n_clicks > 0)
            document.querySelector('#data_table button.export').click()
        return ''
    }
    ''',
    Output('export_table', 'data-text'),
    Input('export_table', 'n_clicks')
)

# Callback function to Input Address Div / value triggered by Radioitems / value
# Summary:
#  - When a token is selected in the radio item, 
#    the address corresponding to the token defined in config.ini is displayed in the "component_property:value" of the input tag.
@app.callback(
    Output('input_address', 'value'),
    Input('drop_down_div', 'value'),
)
def update_selecter(token):
    # Get Subscan API Info
    address = config_manage.get_subscan_api_info_address(token)
    return address

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
    Output('confirm_error_dialog', 'displayed'),
    Output('confirm_error_dialog', 'message'),
    Output('data_table', 'data'),
    Output('data_table', 'columns'),
    Output('data_table', 'page_size'),
    Output('data_table', 'page_current'),
    Output('data_table', 'selected_cells'),
    Output('data_table', 'active_cell'),
    Output('response_data_info', 'children'),
    Output('table_div', 'style'),
    Input('submit','n_clicks'),
    State('input_address','value'),
    State('radio_history_type', 'value'),
    State('drop_down_div', 'value'),
    State('input_num', 'value'),
    State('radio_sort', 'value'),
    prevent_initial_call=True
)
def get_subscan_stkrwd(n_clicks,address,history_type,token,num,sort_type):
    # variable initialization
    is_error = False
    text = None
    confirm_dialog_flag = False
    list_num = 0
    response_data_info = ''
    supplement = ''

    # HTTP POST Request
    if history_type == 'Reward&Slash':
        stkrwd = SubscanStakingRewardDataProcess(num,config_manage.subscan_api_info,token,address,sort_type)
        response_code, api_endpoint, response_status_code, header_list ,response_data_list, df, list_num = stkrwd.get_subscan_stakerewards()
    elif history_type == 'CryptactCustom':
        cyrptactcustom = SubscanStakingRewardsDataProcessForCryptact(num,config_manage.subscan_api_info,config_manage.cryptact_info,token,address,sort_type)
        response_code, api_endpoint, response_status_code, header_list ,response_data_list, df, list_num = cyrptactcustom.create_stakerewards_cryptact_cutom_df()

    # Check Error
    is_error, text = is_error_check(response_code,response_status_code,list_num)
    
    # Recieve data processing
    if is_error == True or list_num == 0:
        # Error handling
        df_manage.error_flag = True
        # Response data reception failure
        confirm_dialog_flag = True
        message = text
        response_data_info = 'Error'
        return confirm_dialog_flag, message,no_update, no_update, no_update, no_update, no_update, no_update, response_data_info,{'display':'none'}
    else:
        # Response data received successfully
        # Set received data (DataFrame)
        df_manage.df_data = df

        # Round to the maximum number if the acquisition limit is exceeded
        if int(num) > int(len(df)):
            supplement = '(*Retrieved up to the upper limit of the history.)'

        text1 = f'API Endpoint: {api_endpoint}'
        text2 = f'HTTP Status Codes: {response_status_code}'
        text3 = f'Data Num: {len(df)}{supplement}'

        output_string = html.Div([
            html.Div(children=text1),
            html.Div(children=text2),
            html.Div(children=text3)
            ],
        )
        
        if n_clicks:
            # submit
            data = df.to_dict('records')
            columns = [{'name': str(i), 'id': str(i),'deletable': False,'renamable': False} for i in df.columns]
            page_size = ROW_PER_PAGE
            page_current = 0
            selected_cells = []
            active_cell = None
            response_data_info = output_string
            return confirm_dialog_flag, no_update,data, columns, page_size, page_current, selected_cells, active_cell, response_data_info, {'display':'inline'}
    raise PreventUpdate

# error-determining function
def is_error_check(response_code,response_status_code,list_num):
    result = False
    text = ''
    # Response data error judgment processing
    # code error (other than success)
    if response_code != 0:
        text = f'HTTP Status Codes: {response_code}\n'\
                'Error Details: Invalid Account Address.\n'\
                'Please Check Account Address.\n\n'\
                'Click OK button to go to the Subscan API Documents page.\n'\
                'Open URL?({config_manage.subscan_api_doc})\n'
        result = True
    # HTTP Status Codes Error
    elif response_status_code != 200:
        text = f'HTTP Status Codes: {response_status_code}\n'\
                'Please Check Subscan API Documents.\n\n'\
                'Click OK button to go to the Subscan API Documents page.\n'\
                'Open URL?({config_manage.subscan_api_doc})\n'
        result = True
    # Error when no data received
    elif list_num == 0:
        text = f'Response data could not be retrieved.\n'\
                'Please Check Subscan API Documents or Response data.\n\n'\
                'Click OK button to go to the Subscan API Documents page.\n'\
                'Open URL?({config_manage.subscan_api_doc})\n'
        result = True
    return result, text

if __name__ == '__main__':
    # To allow access from other computers on the local network
    # app.run(debug=True,host='0.0.0.0')
    # To allow access only from your own computer
    app.run(debug=True)