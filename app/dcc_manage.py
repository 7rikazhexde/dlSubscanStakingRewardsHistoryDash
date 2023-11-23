class DccManage:
    def __init__(self, config_subscan_api_info, config_ui_info):
        # token_list selection read
        self.__token_data_list = config_subscan_api_info["token_list"]
        self.__token_data = self.__token_data_list[0]

        # history_type_list selection read
        self.__history_type_list = config_ui_info["history_type_list"]
        self.__history_type = self.__history_type_list[0]

        # sort_list selection read
        self.__sort_list = config_ui_info["sort_list"]
        self.__sort_type = self.__sort_list[0]

    # Setter/Getter for token information
    @property
    def token_data_list(self):
        return self.__token_data_list

    @token_data_list.setter
    def token_data_list(self, token_list):
        self.__token_data_list = token_list

    # Setter/Getter for history type information
    @property
    def history_type_list(self):
        return self.__history_type_list

    @history_type_list.setter
    def history_type_list(self, history_type_data_list):
        self.__history_type_list = history_type_data_list

    # Setter/Getter for sort information
    @property
    def sort_list(self):
        return self.__sort_list

    @sort_list.setter
    def sort_list(self, sort_type_list):
        self.__sort_list = sort_type_list
