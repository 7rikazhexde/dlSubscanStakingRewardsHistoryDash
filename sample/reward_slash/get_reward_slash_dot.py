import json
from decimal import ROUND_HALF_UP, Decimal

import requests

# Code to retrieve staking reward data managed by reward_slash

# The data to be acquired can be viewed at the following Subscan Explorer URL
# https://polkadot.subscan.io/reward?address=[address]&role=account
url = "https://polkadot.api.subscan.io/api/v2/scan/account/reward_slash"

payload = json.dumps(
    {
        "address": "",
        "block_range": "",
        "category": "Reward",
        "is_stash": True,
        "page": 0,
        "row": 10,
        "timeout": 0,
    }
)
headers = {
    "User-Agent": "Apidog/1.0.0 (https://apidog.com)",
    "Content-Type": "application/json",
}

response = requests.request("POST", url, headers=headers, data=payload)

response_json = response.json()
list_num = len(response_json["data"]["list"])
list_num = 10

for i in range(list_num):
    amount = response_json["data"]["list"][i]["amount"]
    value = Decimal(amount) / Decimal("10") ** 10
    num = 10
    rounded_value = value.quantize(Decimal(f"1e-{num}"), rounding=ROUND_HALF_UP)
    print(rounded_value)
