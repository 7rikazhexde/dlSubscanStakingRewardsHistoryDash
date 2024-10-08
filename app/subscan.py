import json
import math
import time
import traceback
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import pandas as pd
import requests
from cryptact import CryptactInfo


class SubscanStakingRewardsDataFrame:
    def __init__(self, config_subscan_api_info, token, stk):
        # Selected Token
        self.__token_data = token
        self.__stk_data = stk

        # List for creating Reward&Slash tables
        # Reward&Slash / Download all data(csv) / header
        self.__reward_slash_data_header_config = (
            f"reward_slash_data_header_{stk.lower()}_{token.lower()}"
        )
        self.__reward_slash_data_header_token = config_subscan_api_info[
            self.__reward_slash_data_header_config
        ]
        # Create DataFrame object for Reward&Slash
        self.__df_stkrwd_header_data = pd.DataFrame(
            columns=self.__reward_slash_data_header_token
        )

        # List for Response data
        # Staking API / reward-slash-v2(DOT,KSM) / Response / data / list
        # V2 API / reward-slash(ASTR,MANTA) / Response / data / list
        reward_slash_data_config = f"reward_slash_data_{stk.lower()}_{token.lower()}"
        self.__reward_slash_data_token = config_subscan_api_info[
            reward_slash_data_config
        ]

    # Accessor for DataFrame for Reward&Slash
    @property
    def df_stkrwd_header_data(self):
        return self.__df_stkrwd_header_data

    @df_stkrwd_header_data.setter
    def df_stkrwd_header_data(self, df):
        self.__df_stkrwd_header_data = pd.concat([self.__df_stkrwd_header_data, df])

    # Accessor to list for Response data
    @property
    def reward_slash_data_token(self):
        return self.__reward_slash_data_token

    @reward_slash_data_token.setter
    def reward_slash_data_token(self, df):
        self.__reward_slash_data_token = pd.concat([self.__reward_slash_data_token, df])

    # Accessors for tokens
    @property
    def token_data(self):
        return self.__token_data

    # Accessors for tokens
    @property
    def stk_data(self):
        return self.__stk_data

    # Method to create a list of StakingRewards to be retrieved from the list element (item) of the received json data
    def get_reward_slash_data(self, item, response_json):
        stkrwd_data_list = []
        for column_index in self.__reward_slash_data_token:
            event_index_data = response_json["data"]["list"][item][column_index]
            stkrwd_data_list.append(event_index_data)
        # Returns data for one element of the received json data (list) and as a list of StakingRewards
        return stkrwd_data_list

    # Method to create values for DOT and KSM from the list of StakingRewards in list format
    def get_reward_slash_data_var_dot_ksm(
        self, one_line_headerdata_list, adjust_value, exp_val
    ):
        # List for one line of json data
        self.__one_line_data_list = []

        if self.stk_data == "Nominator":
            # variable value
            # 0 event_index
            # 1 era
            # 2 block_timestamp
            # 3 extrinsic_index
            # 4 amount
            # 5 module_id
            # 6 event_id
            # 7 stash
            # 8 account
            # 9 validator_stash
            self.__event_index = one_line_headerdata_list[0]
            self.__era = one_line_headerdata_list[1]
            self.__date = datetime.utcfromtimestamp(one_line_headerdata_list[2])
            # Block data is created from event_index
            self.__block = self.__event_index.split("-")[0]
            self.__extrinsic_index = one_line_headerdata_list[3]
            self.__value = Decimal(one_line_headerdata_list[4]) / Decimal("10") ** int(
                adjust_value
            )
            self.__value = self.__value.quantize(
                Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
            )
            # Action data is created from module_id and event_id
            self.__action = (
                one_line_headerdata_list[5] + f"({one_line_headerdata_list[6]})"
            )
            self.__stash = one_line_headerdata_list[7]
            self.__reward_account = one_line_headerdata_list[8]
        elif self.stk_data == "NominationPool":
            # variable value
            # 0 event_index
            # 1 block
            # 2 extrinsic_index
            # 3 pool_id
            # 4 amount
            # 5 event_id
            # 6 block_timestamp
            self.__event_index = one_line_headerdata_list[0]
            self.__block = one_line_headerdata_list[0].split("-")[0]
            self.__extrinsic_index = one_line_headerdata_list[1]
            self.__pool_id = one_line_headerdata_list[2]
            self.__amount = Decimal(one_line_headerdata_list[3]) / Decimal("10") ** int(
                adjust_value
            )
            self.__amount = self.__amount.quantize(
                Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
            )
            self.__action = f"nominationpools {one_line_headerdata_list[4]}"
            self.__block_timestamp = datetime.utcfromtimestamp(
                one_line_headerdata_list[5]
            )

        if self.token_data == "DOT" and self.stk_data == "Nominator":
            # Create Validator Stash for Dot as it exists.
            self.__validator_stash = one_line_headerdata_list[9]
            self.__one_line_data_list = [
                self.__event_index,
                self.__era,
                self.__date,
                self.__block,
                self.__extrinsic_index,
                self.__value,
                self.__action,
                self.__stash,
                self.__reward_account,
                self.__validator_stash,
            ]
        elif self.token_data == "KSM" and self.stk_data == "Nominator":
            self.__one_line_data_list = [
                self.__event_index,
                self.__era,
                self.__date,
                self.__block,
                self.__extrinsic_index,
                self.__value,
                self.__action,
                self.__stash,
                self.__reward_account,
            ]
        elif self.token_data == "DOT" and self.stk_data == "NominationPool":
            # Create Validator Stash for Dot as it exists.
            self.__one_line_data_list = [
                self.__event_index,
                self.__block,
                self.__extrinsic_index,
                self.__pool_id,
                self.__amount,
                self.__action,
                self.__block_timestamp,
            ]
        elif self.token_data == "KSM" and self.stk_data == "NominationPool":
            self.__one_line_data_list = [
                self.__event_index,
                self.__block,
                self.__extrinsic_index,
                self.__pool_id,
                self.__amount,
                self.__action,
                self.__block_timestamp,
            ]

        return self.__one_line_data_list

    # Method to create values for ASTR from a list of StakingRewards in list format
    def get_reward_slash_data_var_astr(
        self, one_line_headerdata_list, adjust_value, exp_val
    ):
        self.__one_line_data_list = []
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        # 6 event_id
        # Event ID data is created from event_index
        self.__event_id = one_line_headerdata_list[0]
        self.__date = datetime.utcfromtimestamp(one_line_headerdata_list[1])
        # Block data is created from event_index
        self.__block = self.__event_id.split("-")[0]
        self.__extrinsic_index = one_line_headerdata_list[3]
        self.__value = Decimal(one_line_headerdata_list[4]) / Decimal("10") ** int(
            adjust_value
        )
        self.__value = self.__value.quantize(
            Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
        )
        # Action data is created from module_id and event_id
        self.__action = one_line_headerdata_list[5] + f"({one_line_headerdata_list[6]})"

        self.__one_line_data_list = [
            self.__event_id,
            self.__date,
            self.__block,
            self.__extrinsic_index,
            self.__value,
            self.__action,
        ]
        return self.__one_line_data_list

    # Method to create values for MANTA from a list of StakingRewards in list format
    def get_reward_slash_data_var_manta(
        self, one_line_headerdata_list, adjust_value, exp_val
    ):
        self.__one_line_data_list = []
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        # 6 event_id
        # Event ID data is created from event_index
        self.__event_id = one_line_headerdata_list[0]
        self.__date = datetime.utcfromtimestamp(one_line_headerdata_list[1])
        # Block data is created from event_index
        self.__block = self.__event_id.split("-")[0]
        self.__extrinsic_index = one_line_headerdata_list[3]
        self.__value = Decimal(one_line_headerdata_list[4]) / Decimal("10") ** int(
            adjust_value
        )
        self.__value = self.__value.quantize(
            Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
        )
        # Action data is created from module_id and event_id
        self.__action = one_line_headerdata_list[5] + f"({one_line_headerdata_list[6]})"

        self.__one_line_data_list = [
            self.__event_id,
            self.__date,
            self.__block,
            self.__extrinsic_index,
            self.__value,
            self.__action,
        ]
        return self.__one_line_data_list

    # Method to add the specified list to the DataDrame by row specification
    def json_to_df(self, df, item, one_line_data_list):
        df.loc[item, :] = one_line_data_list
        return df


class SubscanStakingRewardsDataFrameForCryptact(SubscanStakingRewardsDataFrame):
    def __init__(self, config_subscan_api_info, config_cryptact_info, token, stk):
        super().__init__(config_subscan_api_info, token, stk)
        # Create DataFrame for Cryptact custom file
        self.__cryptact_heder_data = config_cryptact_info["cryptact_custom_header"]
        self.__df_cryptact_header_data = pd.DataFrame(
            columns=self.__cryptact_heder_data
        )

    # Accessors to DataFrame for Cryptact custom files
    @property
    def df_cryptact_header_data(self):
        return self.__df_cryptact_header_data

    @df_cryptact_header_data.setter
    def df_cryptact_header_data(self, df):
        self.__df_cryptact_header_data = pd.concat([self.__df_cryptact_header_data, df])

    def get_reward_slash_data_var_cryptact(
        self, one_line_headerdata_list, cryptact_info_data, adjust_value, exp_val
    ):
        self.__one_line_data_list = []
        # fixed value
        (
            action,
            source,
            base,
            price,
            counter,
            fee,
            feeccy,
        ) = cryptact_info_data.cryptact_info

        # variable value
        # 0 event_index
        # 1 era
        # 2 block_timestamp
        # 3 extrinsic_index
        # 4 amount
        # 5 module_id
        # 6 event_id
        # 7 stash
        # 8 account
        # 9 validator_stash
        if self.token_data == "DOT" or self.token_data == "KSM":
            self.__event_index = one_line_headerdata_list[0]
            if self.stk_data == "Nominator":
                self.__date = datetime.fromtimestamp(one_line_headerdata_list[2])
                self.__value = Decimal(one_line_headerdata_list[4]) / Decimal(
                    "10"
                ) ** int(adjust_value)
                self.__value = self.__value.quantize(
                    Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
                )
            elif self.stk_data == "NominationPool":
                self.__date = datetime.fromtimestamp(one_line_headerdata_list[5])
                self.__value = Decimal(one_line_headerdata_list[3]) / Decimal(
                    "10"
                ) ** int(adjust_value)
                self.__value = self.__value.quantize(
                    Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
                )
            self.__one_line_data_list = [
                self.__date,
                action,
                source,
                base,
                self.__value,
                price,
                counter,
                fee,
                feeccy,
                self.__event_index,
            ]
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        elif self.token_data == "ASTR":
            self.__event_id = one_line_headerdata_list[0]
            self.__date = datetime.fromtimestamp(one_line_headerdata_list[1])
            self.__value = Decimal(one_line_headerdata_list[4]) / Decimal("10") ** int(
                adjust_value
            )
            self.__value = self.__value.quantize(
                Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
            )
            self.__one_line_data_list = [
                self.__date,
                action,
                source,
                base,
                self.__value,
                price,
                counter,
                fee,
                feeccy,
                self.__event_id,
            ]
        # 0 event_index
        # 1 block_timestamp
        # 2 block_num
        # 3 extrinsic_hash
        # 4 amount
        # 5 module_id
        elif self.token_data == "MANTA":
            self.__event_id = one_line_headerdata_list[0]
            self.__date = datetime.fromtimestamp(one_line_headerdata_list[1])
            self.__value = Decimal(one_line_headerdata_list[4]) / Decimal("10") ** int(
                adjust_value
            )
            self.__value = self.__value.quantize(
                Decimal(f"{exp_val}"), rounding=ROUND_HALF_UP
            )
            self.__one_line_data_list = [
                self.__date,
                action,
                source,
                base,
                self.__value,
                price,
                counter,
                fee,
                feeccy,
                self.__event_id,
            ]
        return self.__one_line_data_list


class SubscanApiInfo:
    def __init__(self, config_subscan_api_info, token, stk, address):
        self.__api_key = str(config_subscan_api_info["api_key"])

        request_url_config = f"request_url_{stk.lower()}_{token.lower()}"
        api_host_config = f"api_host_{token.lower()}"
        # address_cnfig       = f'address_{token.lower()}'
        adjust_value_config = f"adjust_value_{stk.lower()}_{token.lower()}"

        self.__request_url = config_subscan_api_info[request_url_config]
        self.__api_host = config_subscan_api_info[api_host_config]
        self.__address = address  # config_subscan_api_info[address_cnfig]
        self.__adjust_value = float(config_subscan_api_info[adjust_value_config])

        self.__api_endpoint = self.__api_host + self.__request_url
        # POST request with the requests module using the Subscan API
        # header
        self.__headers_dict = {
            "Content-Type": "application/json",
            "X-API-Key": self.__api_key,
        }
        # data-raw
        # row is limited to 100
        self.__data_dict = {"row": 0, "page": 0, "address": self.__address}

    @property
    def subscan_api_info(self):
        return (
            self.__api_endpoint,
            self.__headers_dict,
            self.__data_dict,
            self.__adjust_value,
        )


class SubscanStakingRewardDataProcess:
    def __init__(self, input_num, config_subscan_api_info, token, address, stk, sort):
        # Instance Creation
        self.subscan_stkrwd_df = SubscanStakingRewardsDataFrame(
            config_subscan_api_info, token, stk
        )
        self.subscan_api_data = SubscanApiInfo(
            config_subscan_api_info, token, stk, address
        )

        # Dataframe initialization with get_stkrwd_header_df method
        self.df_header = self.subscan_stkrwd_df.df_stkrwd_header_data

        # Header creation with get_stkrwd_header_df
        self.header_list = self.subscan_stkrwd_df.df_stkrwd_header_data

        # API Information Settings
        (
            self.api_endpoint,
            self.headers_dict,
            self.data_dict,
            self.adjust_value,
        ) = self.subscan_api_data.subscan_api_info

        # Set the number of cases
        self.input_num = int(input_num)

        # Update row by number
        self.data_dict["row"] = self.input_num

        # Token Setting
        self.token = token

        # Staking Type Setting
        self.stk = stk

        # Sort Information Setting
        if sort == "Ascending":
            self.sort_type = True
        else:
            self.sort_type = False

        # initialization of data for reception
        self.response_data = []
        data_list = [["data1", 1], ["data2", 2]]
        self.sort_df_retrieve = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])

        # Config information acquisition
        self.exp_val = config_subscan_api_info[
            f"exponential_value_{stk.lower()}_{token.lower()}"
        ]

    def get_subscan_stakerewards(self):
        # Initialization of the number of list elements
        list_num = 0

        # Initialize total value of list element
        list_num_sum = 0

        # Sort list
        if self.stk == "Nominator":
            sort_val_pri1 = "Date"
            sort_val_pri2 = "Event Index"
            if self.token == "ASTR" or self.token == "MANTA":
                sort_val_pri2 = "Event ID"
            sort_val_list = [sort_val_pri1, sort_val_pri2]
        elif self.stk == "NominationPool":
            sort_val_pri1 = "Time"
            sort_val_pri2 = "Event ID"
            if self.token == "ASTR" or self.token == "MANTA":
                sort_val_pri1 = "Date"
                sort_val_pri2 = "Event ID"
            sort_val_list = [sort_val_pri1, sort_val_pri2]

        # If input_num is greater than 100, row has an upper limit of 100,
        # so the number of processing times is calculated from the number of cases, and every 100 cases is obtained.
        if self.input_num > 100:
            # Calculate the maximum number of pages to retrieve
            # ex)120->1.2->1,1+1 becomes 2
            page_renge = math.floor(self.input_num / 100) + 1
            # Update row (upper limit of row is 100, so 100 row/page is used)
            self.data_dict["row"] = 100

            for page in range(page_renge):
                # Sleep for 0.2 seconds considering API rate limit exceeded
                time.sleep(0.2)

                # Update page
                self.data_dict["page"] = page

                # Staking API / rewards-slash specification / row: 100 / page: Send by page
                response = requests.post(
                    self.api_endpoint,
                    headers=self.headers_dict,
                    data=json.dumps(self.data_dict),
                )

                # HTTP Status Codes
                response_status_code = response.status_code

                # Responsedata(JSON)
                response_json = response.json()

                # Check Error
                try:
                    response_code = response_json["code"]
                except Exception as e:
                    # ex)API rate limit exceeded
                    print(
                        f"Exception occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                    )
                    break

                try:
                    # Get the number of elements in the list if the address is not invalid.
                    if response_code != 400:
                        try:
                            list_num = len(response_json["data"]["list"])
                        except TypeError as e:
                            list_num = 0
                            print(
                                f"Changed list_num = {list_num} / TypeError occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                            )
                except TypeError:
                    count = response_json["data"]["count"]
                    print(
                        f"TypeError, but at this point, the data reading process has been executed up to the upper limit, so the iterative process is terminated. / count: {count}\n"
                    )
                    break

                # Add the number of list elements per page.
                list_num_sum += list_num

                # Create incoming data if there are no Response errors and the list exists
                if (
                    response_status_code == 200
                    and response_code == 0
                    and list_num_sum != 0
                ):
                    for item in range(list_num):
                        one_line_headerdata_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data(
                                item, response_json
                            )
                        )
                        if self.token == "DOT" or self.token == "KSM":
                            one_line_data_list = self.subscan_stkrwd_df.get_reward_slash_data_var_dot_ksm(
                                one_line_headerdata_list,
                                self.adjust_value,
                                self.exp_val,
                            )
                        elif self.token == "ASTR" or self.token == "MANTA":
                            one_line_data_list = (
                                self.subscan_stkrwd_df.get_reward_slash_data_var_astr(
                                    one_line_headerdata_list,
                                    self.adjust_value,
                                    self.exp_val,
                                )
                            )
                        df_page = self.subscan_stkrwd_df.json_to_df(
                            self.df_header, item, one_line_data_list
                        )
                    # Create DataFrame from list with setter (join)
                    self.subscan_stkrwd_df.df_stkrwd_header_data = df_page
                    # Get the DataFrame created (combined) with getter
                    concat_df = self.subscan_stkrwd_df.df_stkrwd_header_data
                    # delete duplicate rows
                    concat_df_duplicates = concat_df.drop_duplicates()
                    # Extract the number of cases from the data acquired for page_range
                    df_retrieve = concat_df_duplicates.iloc[: self.input_num, :]
                    # Sort
                    if self.token == "DOT" or self.token == "KSM":
                        self.sort_df_retrieve = df_retrieve.sort_values(
                            by=sort_val_list, ascending=self.sort_type
                        )
                    elif self.token == "ASTR" or self.token == "MANTA":
                        self.sort_df_retrieve = df_retrieve.sort_values(
                            by=sort_val_list, ascending=self.sort_type
                        )
                    self.sort_df_retrieve[sort_val_pri1] = pd.to_datetime(
                        self.sort_df_retrieve[sort_val_pri1]
                    )
                    self.sort_df_retrieve[sort_val_pri1] = self.sort_df_retrieve[
                        sort_val_pri1
                    ].dt.strftime("%Y-%m-%d %H:%M:%S")
                    # List extracted data
                    self.response_data = self.sort_df_retrieve.values.tolist()
                    # Override by the total value of the list element
                    list_num = list_num_sum
        else:
            # self.input_num <= 100
            # Staking API / specification
            response = requests.post(
                self.api_endpoint,
                headers=self.headers_dict,
                data=json.dumps(self.data_dict),
            )

            # HTTP Status Codes
            response_status_code = response.status_code

            # Response Data(JSON)
            response_json = response.json()
            response_code = response_json["code"]

            # Get the number of elements in the list if the address is not invalid.
            if response_code != 400:
                try:
                    list_num = len(response_json["data"]["list"])
                except TypeError as e:
                    list_num = 0
                    print(
                        f"Changed list_num = {list_num} / TypeError occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                    )

            # If there are no errors in Response and the list exists, incoming data is created.
            if response_status_code == 200 and response_code == 0 and list_num != 0:
                # Process the number of data received
                for item in range(list_num):
                    one_line_headerdata_list = (
                        self.subscan_stkrwd_df.get_reward_slash_data(
                            item, response_json
                        )
                    )
                    if self.token == "DOT" or self.token == "KSM":
                        one_line_data_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data_var_dot_ksm(
                                one_line_headerdata_list,
                                self.adjust_value,
                                self.exp_val,
                            )
                        )
                    elif self.token == "ASTR" or self.token == "MANTA":
                        one_line_data_list = (
                            self.subscan_stkrwd_df.get_reward_slash_data_var_astr(
                                one_line_headerdata_list,
                                self.adjust_value,
                                self.exp_val,
                            )
                        )
                    df_page = self.subscan_stkrwd_df.json_to_df(
                        self.df_header, item, one_line_data_list
                    )
                # Sort
                if self.token == "DOT" or self.token == "KSM":
                    self.sort_df_retrieve = df_page.sort_values(
                        by=sort_val_list, ascending=self.sort_type
                    )
                elif self.token == "ASTR" or self.token == "MANTA":
                    self.sort_df_retrieve = df_page.sort_values(
                        by=sort_val_list, ascending=self.sort_type
                    )
                self.sort_df_retrieve[sort_val_pri1] = pd.to_datetime(
                    self.sort_df_retrieve[sort_val_pri1]
                )
                self.sort_df_retrieve[sort_val_pri1] = self.sort_df_retrieve[
                    sort_val_pri1
                ].dt.strftime("%Y-%m-%d %H:%M:%S")
                # List extracted data
                self.response_data = self.sort_df_retrieve.values.tolist()
        return (
            response_code,
            self.api_endpoint,
            response_status_code,
            self.header_list,
            self.response_data,
            self.sort_df_retrieve,
            list_num,
        )

    # ascending-descending processing method
    """
    def sort_dataframe(self, df, sort_type):
        num = len(df)
        sort_Column = list(range(num))
        df_s1 = df.assign(SortColumn=sort_Column)
        df_s2 = df_s1.sort_values("SortColumn", ascending=sort_type)
        df_s3 = df_s2.drop("SortColumn", axis=1)
        return df_s3
    """


class SubscanStakingRewardsDataProcessForCryptact(SubscanStakingRewardDataProcess):
    def __init__(
        self,
        input_num,
        config_subscan_api_info,
        config_cryptact_info,
        token,
        address,
        stk,
        sort,
    ):
        # Create Instance
        self.subscan_stkrwd_df_for_cryptact = SubscanStakingRewardsDataFrameForCryptact(
            config_subscan_api_info, config_cryptact_info, token, stk
        )
        self.subscan_api_data = SubscanApiInfo(
            config_subscan_api_info, token, stk, address
        )
        self.cryptact_info_data = CryptactInfo(config_cryptact_info, token)

        # dataframe initialization with get_cryptact_header_df method
        self.df_header = self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data

        # Header creation with get_cryptact_header_df method
        self.header_list = self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data

        # API Information Settings
        (
            self.api_endpoint,
            self.headers_dict,
            self.data_dict,
            self.adjust_value,
        ) = self.subscan_api_data.subscan_api_info

        # Enter the number of cases
        self.input_num = int(input_num)

        # API information update (overwritten by number of items)
        self.data_dict["row"] = self.input_num

        # Sort Information Setting
        if sort == "Ascending":
            self.sort_type = True
        else:
            self.sort_type = False

        # initialization of data for reception
        self.response_data = []
        data_list = [["data1", 1], ["data2", 2]]
        self.sort_df_retrieve = pd.DataFrame(data_list, columns=["culumn1", "culumn2"])

        # Config information acquisition
        self.exp_val = config_subscan_api_info[
            f"exponential_value_{stk.lower()}_{token.lower()}"
        ]

    def create_stakerewards_cryptact_cutom_df(self):
        # Initialization of the number of list elements
        list_num = 0

        # Initialize total value of list element
        list_num_sum = 0

        # If input_num is greater than 100, row has an upper limit of 100,
        # so the number of processing times is calculated from the number of cases, and every 100 cases is obtained.
        if self.input_num > 100:
            # Calculate the maximum number of pages to retrieve
            # ex)120->1.2->1,1+1 becomes 2
            page_renge = math.floor(self.input_num / 100) + 1
            # Update row (upper limit of row is 100, so 100 row/page is used)
            self.data_dict["row"] = 100

            for page in range(page_renge):
                # Sleep for 0.2 seconds considering API rate limit exceeded
                time.sleep(0.2)

                # Update page
                self.data_dict["page"] = page

                # Staking API / rewards-slash specification / row: 100 / page: Send by page
                response = requests.post(
                    self.api_endpoint,
                    headers=self.headers_dict,
                    data=json.dumps(self.data_dict),
                )

                # HTTP Status Codes
                response_status_code = response.status_code

                # Responsedata(JSON)
                response_json = response.json()

                # Check Error
                try:
                    response_code = response_json["code"]
                except Exception as e:
                    # ex)API rate limit exceeded
                    print(
                        f"Exception occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                    )
                    break
                try:
                    # Get the number of elements in the list if the address is not invalid.
                    if response_code != 400:
                        try:
                            list_num = len(response_json["data"]["list"])
                        except TypeError as e:
                            list_num = 0
                            print(
                                f"Changed list_num = {list_num} / TypeError occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                            )
                except TypeError:
                    count = response_json["data"]["count"]
                    print(
                        f"TypeError, but at this point, the data reading process has been executed up to the upper limit, so the iterative process is terminated. / count: {count}\n"
                    )
                    break

                # Add the number of list elements per page.
                list_num_sum += list_num

                # Create incoming data if there are no Response errors and the list exists
                if (
                    response_status_code == 200
                    and response_code == 0
                    and list_num_sum != 0
                ):
                    for item in range(list_num):
                        one_line_headerdata_list = (
                            self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data(
                                item, response_json
                            )
                        )
                        one_line_data_list = self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data_var_cryptact(
                            one_line_headerdata_list,
                            self.cryptact_info_data,
                            self.adjust_value,
                            self.exp_val,
                        )
                        df_page = self.subscan_stkrwd_df_for_cryptact.json_to_df(
                            self.df_header, item, one_line_data_list
                        )
                    # Create DataFrame from list with setter (join)
                    self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data = (
                        df_page
                    )
                    # Get the DataFrame created (combined) with getter
                    concat_df = (
                        self.subscan_stkrwd_df_for_cryptact.df_cryptact_header_data
                    )
                    # delete duplicate rows
                    concat_df_duplicates = concat_df.drop_duplicates()
                    # Extract the number of cases from the data acquired for page_range
                    df_retrieve = concat_df_duplicates.iloc[: self.input_num, :]
                    # Sort
                    self.sort_df_retrieve = df_retrieve.sort_values(
                        by=["Timestamp", "Comment"], ascending=self.sort_type
                    )
                    self.sort_df_retrieve["Timestamp"] = pd.to_datetime(
                        self.sort_df_retrieve["Timestamp"]
                    )
                    self.sort_df_retrieve["Timestamp"] = self.sort_df_retrieve[
                        "Timestamp"
                    ].dt.strftime("'%Y/%m/%d %H:%M:%S")
                    # List extracted data
                    self.response_data = self.sort_df_retrieve.values.tolist()
                    # Override by the total value of the list element
                    list_num = list_num_sum

        else:
            # self.input_num <= 100
            # Staking API / rewards-slash specification
            response = requests.post(
                self.api_endpoint,
                headers=self.headers_dict,
                data=json.dumps(self.data_dict),
            )

            # HTTP Status Codes
            response_status_code = response.status_code

            # Response Data(JSON)
            response_json = response.json()
            response_code = response_json["code"]

            # listの要素数を取得
            if response_code != 400:
                try:
                    list_num = len(response_json["data"]["list"])
                except TypeError as e:
                    list_num = 0
                    print(
                        f"Changed list_num = {list_num} / TypeError occurred at {traceback.extract_tb(e.__traceback__)[-1].filename}:{traceback.extract_tb(e.__traceback__)[-1].lineno}"
                    )

            # Get the number of elements in the list if the address is not invalid.
            if response_status_code == 200 and response_code == 0 and list_num != 0:
                # Process the number of data received
                for item in range(list_num):
                    one_line_headerdata_list = (
                        self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data(
                            item, response_json
                        )
                    )
                    one_line_data_list = self.subscan_stkrwd_df_for_cryptact.get_reward_slash_data_var_cryptact(
                        one_line_headerdata_list,
                        self.cryptact_info_data,
                        self.adjust_value,
                        self.exp_val,
                    )
                    df_page = self.subscan_stkrwd_df_for_cryptact.json_to_df(
                        self.df_header, item, one_line_data_list
                    )
                # Sort
                self.sort_df_retrieve = df_page.sort_values(
                    by=["Timestamp", "Comment"], ascending=self.sort_type
                )
                self.sort_df_retrieve["Timestamp"] = pd.to_datetime(
                    self.sort_df_retrieve["Timestamp"]
                )
                self.sort_df_retrieve["Timestamp"] = self.sort_df_retrieve[
                    "Timestamp"
                ].dt.strftime("'%Y/%m/%d %H:%M:%S")
                # List extracted data
                self.response_data = self.sort_df_retrieve.values.tolist()
        return (
            response_code,
            self.api_endpoint,
            response_status_code,
            self.header_list,
            self.response_data,
            self.sort_df_retrieve,
            list_num,
        )
