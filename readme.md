# Budget Notifications CLI Application
It's a Python CLI application to notify if any shops budget

# Schema Details
## Table Schema
We have database schema consists of two tables: Shops and budgets.

### Shops
The table `t_shops` holds master data about all the shops in our system.

* `a_id` and `a_name` should be self-explanatory.

* `a_online`: Specifies, whether a shop's products are currently being listed on the Stylight website. `1` means they are listed, `0` means they aren't.

### Budgets
The table `t_budgets` holds all shops' monthly budgets.

* `a_shop_id`: Signifies, which shop the budget is associated with.

* `a_budget_amount`: Signifies the monetary value a shop is willing to spend with Stylight in a given month.

* `a_amount_spent`: Represents how much money the shop has spent in that month.

* `a_month`: Signifies the month a budget is valid for. The _day_ component of the date is irrelevant and by convention always set to 1.

* `notification`: Signifies, 50% budget threshold notification is generated for shop.

The amounts spent for the current month are continuously updated until the month ends. Assume a part of the system is already doing that. You may assume all monetary values are in the same currency.

# Project Execution Guideline

## System Requirements
* `Python Version >= 3.8`
* `MySQL Version == 8.0.26 or Equivalent`

## Manual Virtualenv Setup Process
* **OS == LINUX**
  * `mkdir venvs`
  * `pip3 install virtualenv --user`
  * `virtualenv -p python3 venvs/venv`
  * `source venvs/venv/bin/activate`
* **OS == WINDOWS**
  * `mkdir \venvs`
  * `pip install virtualenv`
  * `virtualenv \venvs\venv`
  * `\venvs\venv\Scripts\activate`

## Project Setup
* `git clone https://github.com/tssovi/budget-notifications-cli-app.git`
* `cd budget-notifications-cli-app`
* `pip install -r requirements.txt`

## CLI Commands List
```text
usage: main.py [-h] [-db DB_HOST DB_USER DB_USER_PASSWORD DB_NAME DB_PORT] [-si seed_initial_data] [-sc seed_current_data preferred_date] [-shs show_all_shops_details] [-sha show_all_shops_details_data]
               [-sho show_online_shops_details_data] [-nf [notify_shops, data_volume, budget_month ...]] [-up shop_id budget_amount budget_month] [-re reset_all_db_data] [-cl close_db_connection]

A CLI Budget Notifier Application

optional arguments:
  -h, --help            show this help message and exit
  -db DB_HOST DB_USER DB_USER_PASSWORD DB_NAME DB_PORT, --database DB_HOST DB_USER DB_USER_PASSWORD DB_NAME DB_PORT
                        Configure Database Connection
  -si seed_initial_data, --seed seed_initial_data
                        Seed Initial Data: Y/N
  -sc seed_current_data preferred_date, --seed_current_data seed_current_data preferred_date
                        Seed Data for Given Month: Y/N Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's Date)
  -shs show_all_shops_details, --show_all_shops show_all_shops_details
                        Show All Shops Details Data: Y/N
  -sha show_all_shops_details_data, --show_all_shops_details show_all_shops_details_data
                        Show All Shops Details Data: Y/N
  -sho show_online_shops_details_data, --show_online_shops_details show_online_shops_details_data
                        Show All Online Shops Details Data: Y/N
  -nf [notify_shops, data_volume, budget_month ...], --notify_shops [notify_shops, data_volume, budget_month ...]
                        Notify Shop: Y/N ALL/CURRENT Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's Date)
  -up shop_id budget_amount budget_month, --update_shop_budget shop_id budget_amount budget_month
                        Update Shop Budget: 1-8 budget_amount Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's date')
  -re reset_all_db_data, --reset_data reset_all_db_data
                        Reset All Stored Data: Y/N
  -cl close_db_connection, --close close_db_connection
                        Close Database Connection?: Y/N
```

## Project Execution Commands
* **python main.py -h** **(_This will show all available CLI commands_)**
* **python main.py -db db_host db_user db_password db_name db_port** **(_This will create database connection_)**
* **python main.py -si y** **(_This will seed initial data from `db.sql` file and apply migration from `migration.sql` file_)**
* **python main.py -sc y YYYY-MM-DD** **(_This will seed some more budget data for given date months first date_)
* **python main.py -sha y** **(_This will show all available shops data including budget details_)**
* **python main.py -sho y** **(_This will show all online shops data including budget details_)**
* **python main.py -nf y all ""** **(_This notify shops those monthly expenditure reaches certain thresholds based on all budget month data_)**
* **python main.py -nf y current YYYY-MM-DD** **(_This notify shops those monthly expenditure reaches certain thresholds based on given dates month data_)**
* **python main.py -up shop_id budget_amount YYYY-MM-DD** **(_This will update shops monthly budget based on given date_)**
* **python main.py -re y** **(_This will restore all data from `db.sql` file_)**
* **python main.py -cl y** **(_This close database connection_)**

## Project Features
* Notify shops when they reach 50% or 100% of the month's budget
* Once that budget is exhausted, shops will go offline
* If shops monthly budget updated and overcome the 100% uses ration threshold point then will be online again and notify shop accordingly

## Q&A Section
### Does your solution avoid sending duplicate notifications?
Yes, it does. Implement a notification flag to trace if the shop already notified or not. If not notified then it will send notification.
### How does your solution handle a budget change after a notification has already been sent?
When processed a budget update request this application check if the updated budget is enough to maintain the expense and budget ratio or not.
It also notify shop accordingly with updated budget details.

> ###**Notes:**
> **You can replace YYYY-MM-DD with empty string like "". If you use empty string then it will use current date as input.**

## Sample CLI Commands and Outputs

```text
Terminal Command - python main.py -db localhost sabil password stylight_db 3306
Database Connected Successfully

Terminal Command - python main.py -si y
Data Seeded Successfully

Terminal Command - python main.py -shs y
All Shops Details
Total Data Found: 8

Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online

Terminal Command - python main.py -sha y
All Available Shops Details With Budget
Total Data Found: 16

Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 725.67 - Budget Amount: 930.00
Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 803.67 - Budget Amount: 960.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 886.63 - Budget Amount: 990.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 715.64 - Budget Amount: 670.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 685.91 - Budget Amount: 650.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 580.81 - Budget Amount: 890.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 746.92 - Budget Amount: 740.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 754.93 - Budget Amount: 590.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 507.64 - Budget Amount: 630.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 505.12 - Budget Amount: 870.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 946.32 - Budget Amount: 640.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 912.30 - Budget Amount: 700.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 640.16 - Budget Amount: 980.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 805.15 - Budget Amount: 990.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 965.64 - Budget Amount: 790.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 504.25 - Budget Amount: 720.00

Terminal Command - python main.py -sho y
Online Shops Details With Budget
Total Data Found: 10

Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 725.67 - Budget Amount: 930.00
Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 803.67 - Budget Amount: 960.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 685.91 - Budget Amount: 650.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 580.81 - Budget Amount: 890.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 507.64 - Budget Amount: 630.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 505.12 - Budget Amount: 870.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 640.16 - Budget Amount: 980.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 805.15 - Budget Amount: 990.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 965.64 - Budget Amount: 790.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 504.25 - Budget Amount: 720.00

Terminal Command - python main.py -nf y all ""
Expense Information:
Notify Date 2021-08-22:
Shop ID: 1
Shop Name: Steve McQueen
Shop Month: 2020-06-01
Spent Amount: 725.67
Budget Amount: 930.00
Expense Ration: 78.0
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 1
Shop Name: Steve McQueen
Shop Month: 2020-07-01
Spent Amount: 803.67
Budget Amount: 960.00
Expense Ration: 83.7
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 3
Shop Name: As Seen On Sale
Shop Month: 2020-06-01
Spent Amount: 685.91
Budget Amount: 650.00
Expense Ration: 105.5
Notification Message: Your monthly expense exceed 100% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 3
Shop Name: As Seen On Sale
Shop Month: 2020-07-01
Spent Amount: 580.81
Budget Amount: 890.00
Expense Ration: 65.3
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 5
Shop Name: Meow Meow
Shop Month: 2020-06-01
Spent Amount: 507.64
Budget Amount: 630.00
Expense Ration: 80.6
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 5
Shop Name: Meow Meow
Shop Month: 2020-07-01
Spent Amount: 505.12
Budget Amount: 870.00
Expense Ration: 58.1
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 7
Shop Name: George Manly
Shop Month: 2020-06-01
Spent Amount: 640.16
Budget Amount: 980.00
Expense Ration: 65.3
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 7
Shop Name: George Manly
Shop Month: 2020-07-01
Spent Amount: 805.15
Budget Amount: 990.00
Expense Ration: 81.3
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 8
Shop Name: Harrison Ford
Shop Month: 2020-06-01
Spent Amount: 965.64
Budget Amount: 790.00
Expense Ration: 122.2
Notification Message: Your monthly expense exceed 100% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 8
Shop Name: Harrison Ford
Shop Month: 2020-07-01
Spent Amount: 504.25
Budget Amount: 720.00
Expense Ration: 70.0
Notification Message: Your monthly expense exceed 50% thresholds limit.

Terminal Command - python main.py -sc y 2021-08-22
Current Data Seeded Successfully

Terminal Command - python main.py -nf y current 2021-08-22
Expense Information:
Notify Date 2021-08-22:
Shop ID: 1
Shop Name: Steve McQueen
Shop Month: 2021-08-01
Spent Amount: 725.67
Budget Amount: 950.00
Expense Ration: 76.4
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 5
Shop Name: Meow Meow
Shop Month: 2021-08-01
Spent Amount: 507.64
Budget Amount: 630.00
Expense Ration: 80.6
Notification Message: Your monthly expense exceed 50% thresholds limit.
Expense Information:
Notify Date 2021-08-22:
Shop ID: 7
Shop Name: George Manly
Shop Month: 2021-08-01
Spent Amount: 640.16
Budget Amount: 980.00
Expense Ration: 65.3
Notification Message: Your monthly expense exceed 50% thresholds limit.

Terminal Command - python main.py -nf y current ""
Notification Status: Shop ID: 1 - Shop Name: Steve McQueen - Already Notified.
Notification Status: Shop ID: 5 - Shop Name: Meow Meow - Already Notified.
Notification Status: Shop ID: 7 - Shop Name: George Manly - Already Notified.

Terminal Command - python main.py -up 8 2500.00 2021-08-22
Greetings! Your shop budget has been updated
Congratulations!! Your shop budget has been successfully updated.
Your updated shop budget is: 2500.00

Expense Information:
Notify Date 2021-08-22:
Shop ID: 8
Shop Name: Harrison Ford
Shop Month: 2021-08-01
Spent Amount: 950.64
Budget Amount: 2500.00
Expense Ration: 38.0
Notification Message: Your new monthly budget and expense ratio is 38.0%.

Terminal Command - python main.py -sha y
All Available Shops Details With Budget
Total Data Found: 24

Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 725.67 - Budget Amount: 930.00
Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 803.67 - Budget Amount: 960.00
Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2021-08-01 - Spent Amount: 725.67 - Budget Amount: 950.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 886.63 - Budget Amount: 990.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 715.64 - Budget Amount: 670.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2021-08-01 - Spent Amount: 886.63 - Budget Amount: 1000.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 685.91 - Budget Amount: 650.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 580.81 - Budget Amount: 890.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Offline - Shop Month: 2021-08-01 - Spent Amount: 685.91 - Budget Amount: 650.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 746.92 - Budget Amount: 740.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 754.93 - Budget Amount: 590.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2021-08-01 - Spent Amount: 746.92 - Budget Amount: 740.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 507.64 - Budget Amount: 630.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 505.12 - Budget Amount: 870.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2021-08-01 - Spent Amount: 507.64 - Budget Amount: 630.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 946.32 - Budget Amount: 640.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 912.30 - Budget Amount: 700.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2021-08-01 - Spent Amount: 946.32 - Budget Amount: 640.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 640.16 - Budget Amount: 980.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 805.15 - Budget Amount: 990.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2021-08-01 - Spent Amount: 640.16 - Budget Amount: 980.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 965.64 - Budget Amount: 790.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 504.25 - Budget Amount: 720.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2021-08-01 - Spent Amount: 950.64 - Budget Amount: 2500.00

Terminal Command - python main.py -re y
Data Restored Successfully

Terminal Command - python main.py -sha y
All Available Shops Details With Budget
Total Data Found: 16

Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 725.67 - Budget Amount: 930.00
Shop ID: 1 - Shop Name: Steve McQueen - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 803.67 - Budget Amount: 960.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 886.63 - Budget Amount: 990.00
Shop ID: 2 - Shop Name: Fashion Quasar - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 715.64 - Budget Amount: 670.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 685.91 - Budget Amount: 650.00
Shop ID: 3 - Shop Name: As Seen On Sale - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 580.81 - Budget Amount: 890.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 746.92 - Budget Amount: 740.00
Shop ID: 4 - Shop Name: H&R - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 754.93 - Budget Amount: 590.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 507.64 - Budget Amount: 630.00
Shop ID: 5 - Shop Name: Meow Meow - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 505.12 - Budget Amount: 870.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-06-01 - Spent Amount: 946.32 - Budget Amount: 640.00
Shop ID: 6 - Shop Name: Dole & Cabbage - Shop Status: Offline - Shop Month: 2020-07-01 - Spent Amount: 912.30 - Budget Amount: 700.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 640.16 - Budget Amount: 980.00
Shop ID: 7 - Shop Name: George Manly - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 805.15 - Budget Amount: 990.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-06-01 - Spent Amount: 965.64 - Budget Amount: 790.00
Shop ID: 8 - Shop Name: Harrison Ford - Shop Status: Online - Shop Month: 2020-07-01 - Spent Amount: 504.25 - Budget Amount: 720.00

Terminal Command - python main.py -cl y
Database Disconnected Successfully
```