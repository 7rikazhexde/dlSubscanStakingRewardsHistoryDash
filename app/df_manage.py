import pandas as pd


class DfManage:
    def __init__(self):
        data_list = [["data1", 1], ["data2", 2]]
        self.__df_data = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])
        self.__df_page_num = 0
        self.__error_flag = False

    # Setter/Getter for the DataFrame object
    def get_df(self):
        return self.__df_data

    def set_df(self, df_data):
        self.__df_data = df_data

    df_data = property(get_df, set_df)

    # Setter/Getter for the number of rows in a DataFrame object
    def get_df_page_num(self):
        return self.__df_page_num

    def set_df_page_num(self, df_page_num):
        self.__df_page_num = df_page_num

    df_page_num = property(get_df_page_num, set_df_page_num)

    # Setter/Getter for error flag data
    def get_error_flag(self):
        return self.__error_flag

    def set_error_flag(self, error_flag):
        self.__error_flag = error_flag

    error_flag = property(get_error_flag, set_error_flag)
