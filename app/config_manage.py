from tomlkit.toml_file import TOMLFile


class ConfigManage:
    def __init__(self):
        self.__toml_config = TOMLFile("./app/config.toml")
        self.__config = self.__toml_config.read()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_doc = self.__config_subscan_api_info[
            "subscan_api_doc"
        ]
        self.__config_ui_info = self.__config["ui_info"]
        self.__config_cryptact_info = self.__config["cryptact_info"]
        self.__is_error = False

    # Getter for Subscan API information
    @property
    def subscan_api_info(self):
        return self.__config_subscan_api_info

    # Getter for Subscan API Reference URL
    @property
    def subscan_api_doc(self):
        return self.__config_subscan_api_doc

    # Method to obtain Subscan API Acount
    def get_subscan_api_info_address(self, token):
        address_token = f"address_{(token).lower()}"
        address_token_value = self.__config_subscan_api_info[address_token]
        return address_token_value

    # Getter for Subscan API Acount Address
    @property
    def cryptact_info(self):
        return self.__config_cryptact_info

    # Getter for obtain UI infomation
    @property
    def ui_info(self):
        return self.__config_ui_info

    # Setter/Getter for the Error occurrence
    @property
    def is_error(self):
        return self.__is_error

    @is_error.setter
    def is_error(self, is_error):
        self.__is_error = is_error
