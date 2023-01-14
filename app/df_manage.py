import pandas as pd

class DfManage:
    def __init__(self):
        self.__data = []
        self.__df_data = pd.DataFrame(self.__data)
        self.__df_page_num = 0

    # Setter/Getter for the DataFrame object
    def get_df(self):
        return self.__df_data
     
    def set_df(self,df_data):
        self.__df_data = df_data

    df_data = property(get_df, set_df)

    # Setter/Getter for the number of rows in a DataFrame object
    def get_df_page_num(self):
        return self.__df_page_num
     
    def set_df_page_num(self,df_page_num):
        self.__df_page_num = df_page_num

    df_page_num = property(get_df_page_num, set_df_page_num)