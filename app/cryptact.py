class CryptactInfo:
    def __init__(self, config_cryptact_info, token):
        self.__action = config_cryptact_info["action"]
        self.__price = config_cryptact_info["price"]
        self.__counter = config_cryptact_info["counter"]
        self.__fee = config_cryptact_info["fee"]
        self.__feeccy = config_cryptact_info["feeccy"]

        __source_token = f"source_{token.lower()}"
        __base_token = f"base_{token.lower()}"

        self.__source = config_cryptact_info[__source_token]
        self.__base = config_cryptact_info[__base_token]

    # Getter for the Cryptact Header Infomation
    def get_cryptact_custom_header_data(self):
        return (
            self.__action,
            self.__source,
            self.__base,
            self.__price,
            self.__counter,
            self.__fee,
            self.__feeccy,
        )

    cryptact_info = property(get_cryptact_custom_header_data)
