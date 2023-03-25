import pytest
from tomlkit.toml_file import TOMLFile

from app.cryptact import CryptactInfo

# Test code for one case
# Assert and test the following code
# Test data: column data of table to be retrieved by CryptactInfo class
# Expected value: column data retrieved from toml file
"""
def cryptact_test_1case(token,expect_token):
    config = TOMLFile("./app/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")

    action = config_cryptact_info["action"]
    price = config_cryptact_info["price"]
    counter = config_cryptact_info["counter"]
    fee = config_cryptact_info["fee"]
    feeccy = config_cryptact_info["feeccy"]
    source_token = f"source_{expect_token.lower()}"
    base_token = f"base_{expect_token.lower()}"
    source = config_cryptact_info[source_token]
    base = config_cryptact_info[base_token]

    ci = CryptactInfo(config_cryptact_info, token)

    assert ci.cryptact_info == (action, source, base, price, counter, fee, feeccy)
"""


# method to get data from toml file and create expected value
def cryptact_expect_val(token):
    config = TOMLFile("./app/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")

    action = config_cryptact_info["action"]
    price = config_cryptact_info["price"]
    counter = config_cryptact_info["counter"]
    fee = config_cryptact_info["fee"]
    feeccy = config_cryptact_info["feeccy"]
    source_token = f"source_{token.lower()}"
    base_token = f"base_{token.lower()}"
    source = config_cryptact_info[source_token]
    base = config_cryptact_info[base_token]

    return (action, source, base, price, counter, fee, feeccy)


# When multiple test cases are executed (normal system)
def cryptact_culumn_data_test(token):
    config = TOMLFile("./app/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")
    ci = CryptactInfo(config_cryptact_info, token)
    return ci.cryptact_info


# TestCase1
@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("DOT", cryptact_expect_val("DOT")),
        ("KSM", cryptact_expect_val("KSM")),
        ("ASTR", cryptact_expect_val("ASTR")),
    ],
)
def test1(token, expected):
    assert cryptact_culumn_data_test(token) == expected


# When multiple test cases are executed (anomaly system)
def cryptact_culumn_data_test_ng(token):
    config = TOMLFile("./app/config.toml")
    toml_config = config.read()
    config_cryptact_info = toml_config.get("cryptact_info")
    ci = CryptactInfo(config_cryptact_info, token)
    return ci.cryptact_info


# TestCase2
@pytest.mark.parametrize(
    ("token", "expected"),
    [
        ("DOT", cryptact_expect_val("KSM")),
        ("DOT", cryptact_expect_val("ASTR")),
        ("KSM", cryptact_expect_val("DOT")),
        ("KSM", cryptact_expect_val("ASTR")),
        ("ASTR", cryptact_expect_val("DOT")),
        ("ASTR", cryptact_expect_val("KSM")),
    ],
)
def test2(token, expected):
    assert cryptact_culumn_data_test_ng(token) != expected


# To test one case at a time
"""
def test():
    cryptact_test_1case("DOT","DOT")
    cryptact_test_1case("KSM","DOT")
    cryptact_test_1case("ASTR","ASTR")
"""
