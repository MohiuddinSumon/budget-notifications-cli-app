import decimal
from datetime import datetime
from common import colors
from enums import NotificationStatus
from db_manager import DatabaseManager


class DataValidator:

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conn = self.db_manager.create_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

    @staticmethod
    def notify_shop_on_budget_update(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, exceed_limit) -> None:
        """
        Notify the Shop about monthly expenditure threshold
        :param shop_id: Shop ID
        :param shop_name: Shop Name
        :param shop_month: Budget initiate month
        :param shop_budget: Budget amount
        :param shop_spent: Expense amount
        :param expense_ration: Expense ratio
        :param exceed_limit: Expense exceed limit
        :return: None
        """
        date = datetime.now().date()

        budget_message = f'{colors[6]}{colors[1]}Congratulations!! Your shop budget has been successfully updated.\n' \
                         f'Your updated shop budget is: {shop_budget}{colors[0]}'
        notify_info = f'{colors[6]}{colors[1]}Notify Date {date}:\nShop ID: {shop_id}\nShop Name: {shop_name}\n' \
                      f'Shop Month: {shop_month}\nSpent Amount: {shop_spent}\nBudget Amount: {shop_budget}\n' \
                      f'Expense Ration: {expense_ration}{colors[0]}'
        if exceed_limit:
            notify_message = f'{colors[6]}{colors[2]}Your monthly expense exceed {exceed_limit} thresholds limit.{colors[0]}'
        else:
            notify_message = f'{colors[6]}{colors[1]}Your new monthly budget and expense ratio is {expense_ration}%.{colors[0]}'

        print(f'{colors[6]}{colors[3]}Greetings! Your shop budget has been updated\n{budget_message}\n{colors[0]}')

        print(f'{colors[6]}{colors[3]}Expense Information:\n{notify_info}\n{colors[6]}{colors[3]}Notification Message: {notify_message}{colors[0]}')

    @staticmethod
    def notify_shop(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, exceed_limit) -> None:
        """
        Notify the Shop about monthly expenditure threshold
        :param shop_id: Shop ID
        :param shop_name: Shop Name
        :param shop_month: Budget initiate month
        :param shop_budget: Budget amount
        :param shop_spent: Expense amount
        :param expense_ration: Expense ratio
        :param exceed_limit: Expense exceed limit
        :return: None
        """
        date = datetime.now().date()

        notify_info = f'{colors[6]}{colors[1]}Notify Date {date}:\nShop ID: {shop_id}\nShop Name: {shop_name}\n' \
                      f'Shop Month: {shop_month}\nSpent Amount: {shop_spent}\nBudget Amount: {shop_budget}\n' \
                      f'Expense Ration: {expense_ration}{colors[0]}'
        notify_message = f'{colors[6]}{colors[2]}Your monthly expense exceed {exceed_limit} thresholds limit.{colors[0]}'

        print(f'{colors[6]}{colors[3]}Expense Information:\n{notify_info}\n{colors[6]}{colors[3]}Notification Message: {notify_message}{colors[0]}')

    def validate_expense_threshold(self, shop_data, first_day, last_day) -> None:
        """
        Validate expenses of Shop
        :param shop_data: Shop details data
        :param first_day: First day of the month
        :param last_day: Last day of the month
        :return: None
        """

        shop_id = shop_data['a_id']
        shop_name = shop_data['a_name']
        shop_month = shop_data['a_month']
        shop_spent = shop_data['a_amount_spent']
        shop_budget = shop_data['a_budget_amount']
        first_notified_date = shop_data['first_notified_date']
        notification = shop_data['notification']
        expense_ration = round((shop_spent / shop_budget) * 100, 1)

        if 50 <= expense_ration >= 100 and NotificationStatus.REACH_100.value not in notification:
            notification += NotificationStatus.REACH_100.value
            self.db_manager.update_shop_status(shop_id, 0)
            self.db_manager.update_notification_status(shop_id, first_notified_date, notification, first_day, last_day)
            self.notify_shop(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, '100%')

        elif 50 <= expense_ration <= 100 and NotificationStatus.REACH_50.value not in notification:
            notification += NotificationStatus.REACH_50.value
            self.db_manager.update_notification_status(shop_id, first_notified_date, notification, first_day, last_day)
            self.notify_shop(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, '50%')

        elif NotificationStatus.REACH_50.value in notification or NotificationStatus.REACH_100.value in notification:
            already_notified = f'{colors[6]}{colors[2]}Shop ID: {shop_id} - Shop Name: {shop_name} - Already Notified.{colors[0]}'
            print(f'{colors[6]}{colors[3]}Notification Status: {already_notified}{colors[0]}')

    def validate_updated_shop_budget(self, shop_data, shop_id, budget_amount, first_day, last_day) -> None:
        """
        Validate budget of Shop
        :param shop_data: Shop details data
        :param shop_id: Shop ID
        :param budget_amount: Shop budget amount
        :param first_day: First day budget month
        :param last_day: Last day budget month
        :return: None
        """

        shop_name = shop_data['a_name']
        shop_month = shop_data['a_month']
        shop_spent = shop_data['a_amount_spent']
        shop_budget = decimal.Decimal(budget_amount)
        notification = shop_data['notification']
        first_notified_date = shop_data['first_notified_date']
        expense_ration = round((shop_spent / shop_budget) * 100, 1)

        if 50 <= expense_ration >= 100:
            notification = NotificationStatus.REACH_100.value
            self.db_manager.update_shop_status(shop_id, 0)
            self.db_manager.update_shop_budget_amount(shop_id, shop_budget, first_day, last_day)
            self.db_manager.update_notification_status(shop_id, first_notified_date, notification, first_day, last_day)
            self.notify_shop_on_budget_update(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, '100%')

        elif 50 <= expense_ration <= 100:
            notification = NotificationStatus.REACH_50.value
            self.db_manager.update_shop_status(shop_id, 1)
            self.db_manager.update_shop_budget_amount(shop_id, shop_budget, first_day, last_day)
            self.db_manager.update_notification_status(shop_id, first_notified_date, notification, first_day, last_day)
            self.notify_shop_on_budget_update(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, '50%')

        else:
            notification = ""
            self.db_manager.update_shop_status(shop_id, 1)
            self.db_manager.update_shop_budget_amount(shop_id, shop_budget, first_day, last_day)
            self.db_manager.update_notification_status(shop_id, first_notified_date, notification, first_day, last_day)
            self.notify_shop_on_budget_update(shop_id, shop_name, shop_month, shop_spent, shop_budget, expense_ration, '')
