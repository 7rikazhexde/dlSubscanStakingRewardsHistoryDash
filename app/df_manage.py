import pandas as pd


class DfManage:
    def __init__(self):
        data_list = [["data1", 1], ["data2", 2]]
        self.__df_data = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])
        self.__df_page_num = 0
        self.__error_flag = False

    # Setter/Getter for the DataFrame object
    @property
    def df_data(self):
        return self.__df_data

    @df_data.setter
    def df_data(self, df_data):
        self.__df_data = df_data

    # Setter/Getter for the number of rows in a DataFrame object
    @property
    def df_page_num(self):
        return self.__df_page_num

    @df_page_num.setter
    def df_page_num(self, df_page_num):
        self.__df_page_num = df_page_num

    # Setter/Getter for error flag data
    @property
    def error_flag(self):
        return self.__error_flag

    @error_flag.setter
    def error_flag(self, error_flag):
        self.__error_flag = error_flag
