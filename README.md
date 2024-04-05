# dlSubscanStakingRewardsHistoryDash

Web app version of [dlSubscanStakingRewardsHistory](https://github.com/7rikazhexde/dlSubscanStakingRewardsHistory#dlsubscanstakingrewardshistory) created using Dash and Plotly

## Table of Contents

- [dlSubscanStakingRewardsHistoryDash](#dlsubscanstakingrewardshistorydash)
  - [Table of Contents](#table-of-contents)
  - [Summary](#summary)
    - [Supported tokens and Subscan API information](#supported-tokens-and-subscan-api-information)
    - [Notes](#notes)
  - [Demo](#demo)
    - [Obtain Staking\&Rewards History](#obtain-stakingrewards-history)
    - [Download Staking\&Rewards History(CSV)](#download-stakingrewards-historycsv)
    - [Notes](#notes-1)
  - [Usage](#usage)
    - [1. environment building](#1-environment-building)
    - [For Docker](#for-docker)
    - [For Local (Linux/Mac/Windows)](#for-local-linuxmacwindows)
      - [Note](#note)
    - [Development Environment](#development-environment)
    - [2. Subscan API Settings](#2-subscan-api-settings)
      - [Supplementation](#supplementation)
    - [3. Application Execution](#3-application-execution)
    - [4. Application Operations](#4-application-operations)
      - [Notes](#notes-2)
      - [1. Usage Button](#1-usage-button)
      - [2. Subscan Button](#2-subscan-button)
      - [3. Donate Button](#3-donate-button)
      - [4. History Type Selection](#4-history-type-selection)
      - [5. Token Type Selection](#5-token-type-selection)
      - [6. Staking Type Selection](#6-staking-type-selection)
      - [7. Sort Type Selection](#7-sort-type-selection)
      - [8. Account Address Input](#8-account-address-input)
      - [9. Input Number](#9-input-number)
      - [10. Submit Button](#10-submit-button)
      - [11. Response Data Info](#11-response-data-info)
      - [12. Table](#12-table)
      - [13. Error handling](#13-error-handling)
  - [Other Information](#other-information)
    - [Cryptact Custom File](#cryptact-custom-file)
    - [Donate](#donate)
      - [DOT](#dot)
      - [KSM](#ksm)
      - [ASTR](#astr)
      - [Manta](#manta)

## Summary

Save data in the following formats as csv files using Dash, Ploly, and Subscan API.

- Reward&Slash transaction history (Download all data)
- Cryptact custom files (Staking rewards)
- 2-dimensional graphical display of cumulative staking reward values and dates

### Supported tokens and Subscan API information

StakingRewards is obtained by specifying the following `Request URL` for each token according to the [API Endpoint](https://support.subscan.io/#api-endpoints) specification.

<div align="center">

| Token | API         | Request URL     | module_id    | event_id |
| ----- | ----------- | --------------- | ------------ | -------- |
| DOT   | V2 API      | reward-slash-v2 | Staking      | Reward   |
| KSM   | V2 API      | reward-slash-v2 | Staking      | Reward   |
| ASTR  | Staking API | reward-slash    | dappsstaking | Reward   |
| MANTA  | Staking API | reward-slash    | parachainstaking | Reward   |

</div>

### Notes

- While I have confirmed that I can verify incoming data for a particular account, I don't guarantee that you will necessarily get the expected data.
- Please note that I'm not responsible for any and all damages incurred by executing or referring to this code.
- The specifications of Subscan and the data format of Cryptact may change, so please check the latest information.
- When using the application, please set **SubscanAPI Key** information from the settings screen described below.
- Transaction history depends on the transaction status. Please be sure to confirm that the data acquired is the desired data and that there are no errors by referring to the transaction data.
- Only **Polkadot**, **Kusama**, **Astar** and **Manta** are supported Networks.\
  If other networks are specified, the data cannot be acquired correctly and an error will result.
  (reference:[API Endpoints](https://support.subscan.io/#api-endpoints))

## Demo

The Reward&Slash data displayed in the following demo uses [address](https://polkadot.subscan.io/reward?address=1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih&role=account) listed in Docs as of January 5, 2023.

### Obtain Staking&Rewards History

![dlSubscanStakingRewardsHistoryDash_demo1.gif](.demofile/dlSubscanStakingRewardsHistoryDash_demo1.gif)

### Download Staking&Rewards History(CSV)

![dlSubscanStakingRewardsHistoryDash_demo2.gif](.demofile/dlSubscanStakingRewardsHistoryDash_demo2.gif)

### Notes

- The assumption is that the response data is different from the Value displayed on Subscan Exploler.
- Not all accounts are applicable, but Value is displayed with the number of digits of the value adjusted.
- In this code, the data is adjusted to Reward&Slash's transaction history (Download all data) by setting the section information in "config.toml", so please compare the data with it when checking.

## Usage

### 1. environment building

### For Docker

> [!CAUTION]
> Currently, Unable to access web page after starting container with Docker([Detail](https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash/issues/5)).

A container based on the service specified in `docker-compose.yaml` (the `app` service) is built, started, and the application is executed.

1. Get project

    ```bash
    git clone https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash.git
    ```

2. Container construction and startup

    ```bash
    docker compose up -d --build

    # Affer build
    docker-compose stop
    docker-compose start
    ```

    or

    ```bash
    docker run --rm -p 8050:8050 dlsubscanstakingrewardshistorydash-app poetry run python app
    ```

### For Local (Linux/Mac/Windows)

#### Note

If you use a development environment that supports static analysis tools, see \[Optional\] Development environment.

1. Get project

    ```bash
    git clone https://github.com/7rikazhexde/dlSubscanStakingRewardsHistoryDash.git
    ```

1. Setup of virtual environment

    Run the poetry command.

    ```bash
    poetry install --no-dev
    ```

- If the package DL fails after installation, there may be a problem with the development environment.
- See [Switching between environments](https://python-poetry.org/docs/managing-environments/#switching-between-environments).
- Please run `poetry env info` to check your development environment.
- If your python version is not 3.10 or higher, please run `poetry env use python3.10` to recreate your development environment.

    Or create a virtual environment with venv, pyenv, etc. and run the following command.

    ```bash
    pip install -r requirements.txt
    ```

### Development Environment

The following static analysis tools are supported in the development environment

- [isort](https://pypi.org/project/isort/): Automatic organization of import statements
- [black](https://pypi.org/project/black/): Code formatter for Python (PEP8 compliant)
- [flake8](https://pypi.org/project/flake8/): Grammar checking
- [ruff](https://pypi.org/project/ruff/): An extremely fast Python linter and code formatter, written in Rust.
- [mypy](https://pypi.org/project/mypy/): Type checking with type annotations
- [pytest](https://pypi.org/project/pytest/): A framework for writing unit tests created for Python.

1. To create a development environment, do the following

   ```bash
   poetry install
   ```

1. How to use the static analysis tool (commands)

   ```bash
   poetry run task isort
   poetry run task black
   poetry run task flake8
   poetry run task mypy
   poetry run task ruffch
   poetry run task rufffix
   poetry run pytest -s -vv --cov=. --cov-branch --cov-report=html
   ```

### 2. Subscan API Settings

- Set the section marked "(User-defined required)" in `app/config.toml` before starting the application.
- Be sure to set the API key, address, decimal point adjustment value, and number of significant digits.
- Each setting value will be displayed in conjunction with the token information set on the page from which you first accessed the URL. (See below for "Application Operations").
- Please note that if the values are changed, the system will not operate normally.

#### Supplementation

- The API key is used in the HTTP Request Header information (`X-API-Key`), but the value can be obtained even if not specified.
- However, the Response data depends on [Rate Limiting](<(https://support.subscan.io/#global-conventions)>).
- Specifying a large value for the number of requests may result in `429 Too Many Requests` and may not work correctly.
- Please obtain an API key when using this service.

### 3. Application Execution

1. Execute the program in a virtual environment

    ```bash
    poetry run python app
    ```

1. Application Launch

    Please access the URL displayed.

    ```bash
    Dash is running on http://0.0.0.0:8050/

     * Serving Flask app 'main'
     * Debug mode: on
    ```

### 4. Application Operations

#### Notes

- The layout is composed of a tree of "components" such as html.Div and dcc.Input.
- See [official documentation](https://dash.plotly.com/) for details.
- The following Reward&Slash data uses the [address](https://polkadot.subscan.io/reward?address=1REAJ1k691g5Eqqg9gL7vvZCBG7FCCZ8zgQkZWd4va5ESih&role=account) listed in Docs.

#### 1. Usage Button

- Press the button to access this README.md.

#### 2. Subscan Button

- Press the button to access Suscan Explorer on your address.

#### 3. Donate Button

- Press the button to access this [Donate](#donate) Info.

#### 4. History Type Selection

- Select `Reward&Slash` or `CryptactCustom`.
- `Reward&Slash` is selected by default.

#### 5. Token Type Selection

- Select one of `DOT`, `KSM`, `ASTR`, `MANTA`.
- `DOT` is selected by default.

#### 6. Staking Type Selection

- Select `Nominator` or `NominationPool`.
- `Nominator` is selected by default.

> [!NOTE]
> **NominationPool supports only DOT and KSM.**  

#### 7. Sort Type Selection

- Select `Ascending` or `Descending`.
- `Ascending` is selected by default.

#### 8. Account Address Input

- Please enter your account.
- If it is not a legitimate account, a response error will result.
- The address is linked to Token (radio button).
- It is automatically entered by defining the `address_{tokken name}` key in the `[subscan_api_info]` selection in `config.toml`.

#### 9. Input Number

- Enter the number to retrieve.
- The default setting is in the range of `0` to `5000`.
- If the range is exceeded, no input is allowed.
- If you want to get more than `5000` entries, change the component_property(`max`) defined in the Input tag for `id='input_num'`.
- The default is `50` entered.

#### 10. Submit Button

- Clicking the `Submit` button will send a POST request based on the information entered in the Type, Token, Sort, and Account Address fields to retrieve the history.

#### 11. Response Data Info

- Response data (API Endpoint, HTTP Status Code, Data Num) is displayed when the `Submit` button is triggered.
- Data Num represents the number of cases retrieved, and if not met in Input, the maximum number of cases that can be retrieved is displayed.
- If there is a problem with the response data during response processing, an error dialog appears and Response Data Info displays Error.
- Default is "No Response Data" is displayed.

#### 12. Table

- Displays response data in table format (`dash_table.DataTable`).
- Select Table Data displays information about the selected cells. By default, "No Data Selection" is displayed.
- The table displays `20` response data per page.
- If the number of entries exceeds `20`, they will be displayed on multiple pages.
- Pressing the CSV Download button saves the response data in csv format.
- Changing pages deselects cells and changes "Response Data Info" and "Select Table Data" to default values.

#### 13. Error handling

- If there is a problem with the response data during response processing, an error dialog will appear; pressing the OK button will close the error dialog and access the Subscan API Documents page. If the Cancel button is pressed, the document page is not accessed and the error dialog is closed.
- When the error dialog is closed, "Response Data Info" will show Error and Select Table Data will change to the default value.

## Other Information

### Cryptact Custom File

Data is created according to the specifications in ["Custom File for any other trades"](https://support.cryptact.com/hc/en-us/articles/360002571312-Custom-File-for-any-other-trades).

- The data for the Cryptact custom file consists of a header and line data. The headers are stored in `[cryptact_info]` in "config.toml".
  `Cryptact_custom_header` value (list type) in "config.toml".
- Row data is created from a list of variable values (`block_timestamp`,`amount`,`event_index`) and `fixed values` (`[cryptact_info]`).
- `block_timestamp` is converted to local time with `fromtimestamp()` because it is UNIX time as it is.
- Date and time information is converted to string by specifying the format to match the Cryptact specification.
- Since `amount` does not match the actual reward amount as it is, adjust the decimal point adjustment value (`[subscan_api_info]` `display_digit_dot/ksw/astr`) set in `config.toml` using the number of significant digits (`[subscan_ api_info]`,`adjust_value_dot/ksw/astr`) using the number of significant digits (`[subscan_info]`).

### Donate

This project was created as a personal hobby, but if you find this project useful, I hope you will consider making a donation to the address below. Your donation will motivate the continued development of this project.

#### DOT

```text
14s8mQa7ZmFGqsaghB5DcgPtASH36vsM3aVEHCS6HAv5ExX5
```

#### KSM

```text
GSTHPevLLzj9zPcWEqGNUvjTQZdDJ8PRTbVWZihCt73oZi5
```

#### ASTR

```text
ZoS4NH8VDcudAc1DqULWBj1PrzWNr1wzHFtMcebbStWeVF8
```

#### Manta

```text
dfaR9auceLJjVSsM9dsfR9iG83XupnnG79M5S7zer8dL38ccM
```

Even a small contribution would be greatly appreciated. With heartfelt gratitude, I thank you.

> [!NOTE]
> Donations are not for profit but are intended to support the ongoing development and improvement of the project.
> There are no perks or services offered in exchange for donations.
