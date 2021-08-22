from datetime import datetime
from mysql import connector
from mysql.connector import Error
import db_config


class DatabaseManager:
    def __init__(self):
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

    @staticmethod
    def create_connection():
        """
        Create Database Connection
        :return: Database connection object
        """
        try:
            db_connection = connector.connect(
                host=db_config.DB_HOST,
                user=db_config.DB_USER,
                passwd=db_config.DB_PASS,
                database=db_config.DB_NAME,
                port=db_config.DB_PORT
            )
            return db_connection
        except Error as e:
            print(e)

    def close_connection(self) -> None:
        """
        Close Database Connection
        :return: None
        """
        self.cursor.close()
        self.conn.close()

    def get_all_shops_list(self) -> list:
        """
        Return all shops data
        :return: data list
        """
        try:
            query = f"""
                SELECT 
                    t_shops.a_id, t_shops.a_name, t_shops.a_online
                FROM 
                    t_shops
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(e)

    def get_all_shops_details_data(self) -> list:
        """
        Return all shops data
        :return: data list
        """
        try:
            query = f"""
                SELECT 
                    t_shops.a_id, t_shops.a_name, t_shops.a_online, t_budgets.a_month,
                    t_budgets.a_budget_amount, t_budgets.a_amount_spent, t_budgets.notification,
                    t_budgets.first_notified_date, t_budgets.last_notified_date
                FROM 
                    t_budgets
                INNER JOIN 
                    t_shops 
                ON
                    t_budgets.a_shop_id=t_shops.a_id
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(e)

    def get_all_online_shops_details_data(self) -> list:
        """
        Return all online shops data
        :return: data list
        """
        try:
            query = f"""
                SELECT 
                    t_shops.a_id, t_shops.a_name, t_shops.a_online, t_budgets.a_month,
                    t_budgets.a_budget_amount, t_budgets.a_amount_spent, t_budgets.notification,
                    t_budgets.first_notified_date, t_budgets.last_notified_date
                FROM 
                    t_budgets
                INNER JOIN 
                    t_shops 
                ON
                    t_budgets.a_shop_id=t_shops.a_id
                WHERE 
                    t_shops.a_online='1'
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(e)

    def get_all_online_shops_data_for_given_date(self, first_day, last_day) -> list:
        """
        Return all online shops data
        :param first_day: First day of a month
        :param last_day: Last day of a month
        :return: data list
        """

        try:
            query = f"""
                SELECT 
                    t_shops.a_id, t_shops.a_name, t_shops.a_online, t_budgets.a_month,
                    t_budgets.a_budget_amount, t_budgets.a_amount_spent, t_budgets.notification,
                    t_budgets.first_notified_date, t_budgets.last_notified_date
                FROM 
                    t_budgets
                INNER JOIN 
                    t_shops 
                ON
                    t_budgets.a_shop_id=t_shops.a_id
                WHERE 
                    t_shops.a_online='1' AND (t_budgets.a_month BETWEEN '{first_day}' AND '{last_day}')
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(e)

    def get_shop_details_data_for_given_date(self, shop_id, first_day, last_day) -> list:
        """
        Return shops details data
        :param shop_id: Shop ID
        :param first_day: First day of a month
        :param last_day: Last day of a month
        :return: data list
        """
        try:
            query = f"""
                SELECT 
                    t_shops.a_id, t_shops.a_name, t_shops.a_online, t_budgets.a_month,
                    t_budgets.a_budget_amount, t_budgets.a_amount_spent, t_budgets.notification,
                    t_budgets.first_notified_date, t_budgets.last_notified_date
                FROM 
                    t_budgets
                INNER JOIN 
                    t_shops 
                ON
                    t_budgets.a_shop_id=t_shops.a_id
                WHERE 
                    t_shops.a_id={shop_id} AND (t_budgets.a_month BETWEEN '{first_day}' AND '{last_day}')
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(e)

    def update_shop_status(self, shop_id, online_status) -> None:
        """
        Update shop active status
        :param shop_id: Id of shop to be updated
        :param online_status: Active status of the shop
        :return: None
        """

        try:
            query = "UPDATE t_shops SET a_online = %s WHERE a_id = %s"
            params = (online_status, shop_id)
            self.cursor.execute(query, params)
            self.conn.commit()

        except Error as e:
            print(e)

    def update_shop_budget_amount(self, shop_id, budget_amount, first_day, last_day) -> None:
        """
        Update shop monthly budget
        :param shop_id: Shop ID
        :param budget_amount: Shop new budget amount
        :param first_day: First day of a month
        :param last_day: Last day of a month
        :return: None
        """
        try:
            query = "UPDATE t_budgets SET a_budget_amount = %s WHERE a_shop_id = %s AND (a_month BETWEEN %s AND %s)"
            params = (budget_amount, shop_id, first_day, last_day)
            self.cursor.execute(query, params)
            self.conn.commit()

        except Error as e:
            print(e)

    def update_notification_status(self, shop_id, first_notified_date, notification, first_day, last_day) -> None:
        """
        Update shop budget notification status
        :param shop_id: Id of shop to be updated
        :param first_notified_date: First notification send date
        :param notification: notification status
        :param first_day: First day of a month
        :param last_day: Last day of a month
        :return: None
        """

        notified_date = datetime.now().date()
        try:
            if not first_notified_date:
                if first_day and last_day:
                    query = "UPDATE t_budgets " \
                            "SET notification = %s, first_notified_date = %s, last_notified_date = %s " \
                            "WHERE a_shop_id = %s AND (a_month BETWEEN %s AND %s)"
                    params = (notification, notified_date, notified_date, shop_id, first_day, last_day)
                else:
                    query = "UPDATE t_budgets " \
                            "SET notification = %s, first_notified_date = %s, last_notified_date = %s " \
                            "WHERE a_shop_id = %s"
                    params = (notification, notified_date, notified_date, shop_id)
            else:
                if first_day and last_day:
                    query = "UPDATE t_budgets " \
                            "SET notification = %s, last_notified_date = %s " \
                            "WHERE a_shop_id = %s AND (a_month BETWEEN %s AND %s)"
                    params = (notification, notified_date, shop_id, first_day, last_day)
                else:
                    query = "UPDATE t_budgets " \
                            "SET notification = %s, last_notified_date = %s " \
                            "WHERE a_shop_id = %s"
                    params = (notification, notified_date, shop_id)

            self.cursor.execute(query, params)
            self.conn.commit()

        except Error as e:
            print(e)
