from tomlkit.toml_file import TOMLFile


class ConfigManage:
    def __init__(self):
        self.load_config()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_doc = self.__config_subscan_api_info[
            "subscan_api_doc"
        ]
        self.__config_ui_info = self.__config["ui_info"]
        self.__config_cryptact_info = self.__config["cryptact_info"]
        self.__is_error = False

    def load_config(self):
        self.__toml_config = TOMLFile("./app/config.toml")
        self.__config = self.__toml_config.read()

    # Getter for Subscan API information
    @property
    def subscan_api_info(self):
        return self.__config_subscan_api_info

    # Getter for Subscan API Reference URL
    @property
    def subscan_api_doc(self):
        return self.__config_subscan_api_doc

    # Getter for Subscan API Acount Address
    @property
    def cryptact_info(self):
        return self.__config_cryptact_info

    # Getter for obtain UI infomation
    @property
    def ui_info(self):
        return self.__config_ui_info

    # Setter/Getter for Subscan API Key
    @property
    def api_key_info(self):
        self.load_config()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        return self.__config_subscan_api_info["api_key"]

    @api_key_info.setter
    def api_key_info(self, api_key):
        self.load_config()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_info["api_key"] = api_key
        self.__toml_config.write(self.__config)

    # Setter/Getter for Token Address
    def get_token_address_info(self, token):
        self.load_config()
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        key = f"address_{token.lower()}"
        return self.__config_subscan_api_info[key]

    def set_token_address_info(self, token, address):
        self.load_config()
        key = f"address_{token.lower()}"
        self.__config_subscan_api_info = self.__config.get("subscan_api_info")
        self.__config_subscan_api_info[key] = address
        self.__toml_config.write(self.__config)

    # Setter/Getter for the Error occurrence
    @property
    def is_error(self):
        return self.__is_error

    @is_error.setter
    def is_error(self, is_error):
        self.__is_error = is_error
