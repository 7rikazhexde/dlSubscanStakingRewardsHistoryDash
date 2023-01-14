class DccManage:
    def __init__(self,config_subscan_api_info,config_ui_info):
        # token_list selection read
        self.__token_data_list = config_subscan_api_info['token_list'].split(',')
        self.__token_data = self.__token_data_list[0]

        # history_type_list selection read
        self.__history_type_list = config_ui_info['history_type_list'].split(',')
        self.__history_type = self.__history_type_list[0]

        # sort_list selection read
        self.__sort_list = config_ui_info['sort_list'].split(',')
        self.__sort_type = self.__sort_list[0]

    # Setter/Getter for token information
    def get_token_data_list(self):
        return self.__token_data_list

    def set_token_data_list(self, token_list):
        self.__token_data_list = token_list
    
    token_data_list = property(get_token_data_list, set_token_data_list)

    # Setter/Getter for history type information
    def get_history_type_list(self):
        return self.__history_type_list

    def set_history_type_list(self, history_type_data_list):
        self.__history_type_list = history_type_data_list
    
    history_type_list = property(get_history_type_list, set_history_type_list)

    # Setter/Getter for sort information
    def get_sort_list(self):
            return self.__sort_list

    def set_sort_list(self, sort_type_list):
        self.__sort_list  = sort_type_list
    
    sort_list = property(get_sort_list, set_sort_list)