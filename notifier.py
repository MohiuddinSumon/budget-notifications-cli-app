from db_manager import DatabaseManager
from validator import DataValidator
from common import colors, get_month_dates


class Notifier:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.expense_threshold_checker = DataValidator()

    def notify_for_all_budget_data(self) -> None:
        """
        Execute Budget Notification Process for All Data
        :return: None
        """
        shop_data_list = self.db_manager.get_all_online_shops_details_data()

        for shop_data in shop_data_list:
            shop_month = str(shop_data['a_month'])
            _, first_day, last_day = get_month_dates(shop_month)
            self.expense_threshold_checker.validate_expense_threshold(
                shop_data=shop_data,
                first_day=first_day,
                last_day=last_day
            )

    def notify_for_current_month_budget_data(self, first_day, last_day) -> None:
        """
        Execute Budget Notification Process Based on Given Date
        :param first_day: First day of a month
        :param last_day: Last day of a month
        :return: None
        """
        shop_data_list = self.db_manager.get_all_online_shops_data_for_given_date(
            first_day=first_day,
            last_day=last_day
        )

        if shop_data_list:
            for shop_data in shop_data_list:
                self.expense_threshold_checker.validate_expense_threshold(
                    shop_data=shop_data,
                    first_day=first_day,
                    last_day=last_day
                )
        else:
            print(f"{colors[6]}{colors[5]}No Shop's Budget Details Found for Given Date's Month. Please Try Again With Another Date.{colors[0]}")
