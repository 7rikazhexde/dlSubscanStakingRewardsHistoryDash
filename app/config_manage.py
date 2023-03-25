from tomlkit.toml_file import TOMLFile


class ConfigManage:
    def __init__(self):
        self.__toml_config = TOMLFile("./config.toml")
        self.__config = self.__toml_config.read()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_doc = self.__config_subscan_api_info[
            "subscan_api_doc"
        ]
        self.__config_ui_info = self.__config["ui_info"]
        self.__config_cryptact_info = self.__config["cryptact_info"]

    # Getter for Subscan API information
    def get_subscan_api_info(self):
        return self.__config_subscan_api_info

    subscan_api_info = property(get_subscan_api_info)

    # Getter for Subscan API Reference URL
    def get_subscan_api_doc(self):
        return self.__config_subscan_api_doc

    subscan_api_doc = property(get_subscan_api_doc)

    # Method to obtain Subscan API Acount
    def get_subscan_api_info_address(self, token):
        address_token = f"address_{(token).lower()}"
        address_token_value = self.__config_subscan_api_info[address_token]
        return address_token_value

    # Getter for Subscan API Acount Address
    def get_cryptact_info(self):
        return self.__config_cryptact_info

    cryptact_info = property(get_cryptact_info)

    # Getter for obtain UI infomation
    def get_ui_info(self):
        return self.__config_ui_info

    ui_info = property(get_ui_info)
