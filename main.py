import argparse
from importlib import reload
from common import colors, get_month_dates
import db_config as config
from db_manager import DatabaseManager
from validator import DataValidator
from notifier import Notifier
from seeder import DataSeeder


class Main:
    @staticmethod
    def database_config(args) -> None:
        """
        Create database connection
        :param args: ARGS dict
        :return: None
        """
        db_host = args.database[0] if args.database[0] else config.DB_HOST
        db_user = args.database[1] if args.database[1] else config.DB_USER
        db_pass = args.database[2] if args.database[2] else config.DB_PASS
        db_name = args.database[3] if args.database[3] else config.DB_NAME
        db_port = args.database[4] if args.database[4] else config.DB_PORT

        with open("db_config.py", "w") as db_file:
            db_file.write(f'DB_HOST = "{db_host}"\n')
            db_file.write(f'DB_USER = "{db_user}"\n')
            db_file.write(f'DB_PASS = "{db_pass}"\n')
            db_file.write(f'DB_NAME = "{db_name}"\n')
            db_file.write(f'DB_PORT = {db_port}\n')

        reload(config)

        db_manager = DatabaseManager()
        conn = db_manager.create_connection()
        if conn and conn.is_connected():
            print(f"{colors[6]}{colors[4]}Database Connected Successfully{colors[0]}")
        else:
            print(f"{colors[6]}{colors[5]}Database Connection Failed. Please Check Your Provided Credentials{colors[0]}")

    @staticmethod
    def seed(args) -> None:
        """
        Seed initial data from db.sql
        :param args: ARGS dict
        :return: None
        """
        seed_flag = args.seed[0]
        if seed_flag.upper() == 'Y':
            seeder = DataSeeder()
            db_flag = seeder.seed()
            if db_flag:
                print(f"{colors[6]}{colors[4]}Data Seeded Successfully{colors[0]}")
            else:
                print(f"{colors[6]}{colors[5]}Data Seed Failed. Please Try Again{colors[0]}")

    @staticmethod
    def seed_current_data(args) -> None:
        """
        Seed given date data from seed_current_month_data function
        :param args: ARGS dict
        :return: None
        """
        seed_flag = args.seed_current_data[0]
        provided_date = args.seed_current_data[1]
        default_date, first_day, last_day = get_month_dates(any_date=provided_date)
        if seed_flag.upper() == 'Y':
            seeder = DataSeeder()
            db_flag = seeder.seed_current_month_data(first_day)
            if db_flag:
                print(f"{colors[6]}{colors[4]}Current Data Seeded Successfully{colors[0]}")
            else:
                print(f"{colors[6]}{colors[5]}Current Data Seed Failed. Please Try Again{colors[0]}")

    @staticmethod
    def generate_shop_data_string(data) -> str:
        """
        Show all shops details data including budget
        :param data: Shop details data
        :return: String
        """
        shop_id = data['a_id']
        shop_name = data['a_name']
        shop_stat = data['a_online']
        shop_month = data['a_month']
        shop_spent = data['a_amount_spent']
        shop_budget = data['a_budget_amount']
        shop_stat = 'Online' if shop_stat else 'Offline'
        shop_data = f'{colors[6]}{colors[1]}Shop ID: {shop_id} - Shop Name: {shop_name} - Shop Status: {shop_stat} - ' \
                    f'Shop Month: {shop_month} - Spent Amount: {shop_spent} - Budget Amount: {shop_budget}{colors[0]}'
        return shop_data

    @staticmethod
    def show_all_shops(args) -> None:
        """
        Show all shops details data including budget
        :param args: ARGS dict
        :return: None
        """
        db_manager = DatabaseManager()
        shop_all_flag = args.show_all_shops[0]
        if shop_all_flag.upper() == 'Y':
            all_shops_list = db_manager.get_all_shops_list()
            print(f'{colors[6]}{colors[7]}{colors[4]}All Shops Details{colors[0]}')
            print(f'{colors[6]}{colors[4]}Total Data Found: {len(all_shops_list)}\n{colors[0]}')
            for data in all_shops_list:
                shop_id = data['a_id']
                shop_name = data['a_name']
                shop_status = data['a_online']
                shop_status = 'Online' if shop_status else 'Offline'
                shop_data = f'{colors[6]}{colors[1]}Shop ID: {shop_id} - Shop Name: {shop_name} - ' \
                            f'Shop Status: {shop_status}{colors[0]}'
                print(shop_data)

    def show_all_shops_with_budget_details(self, args) -> None:
        """
        Show all shops details data including budget
        :param args: ARGS dict
        :return: None
        """
        db_manager = DatabaseManager()
        shop_all_flag = args.show_all_shops_details[0]
        if shop_all_flag.upper() == 'Y':
            all_shops_data = db_manager.get_all_shops_details_data()
            print(f'{colors[6]}{colors[7]}{colors[4]}All Available Shops Details With Budget{colors[0]}')
            print(f'{colors[6]}{colors[4]}Total Data Found: {len(all_shops_data)}\n{colors[0]}')
            for data in all_shops_data:
                shop_data = self.generate_shop_data_string(data=data)
                print(shop_data)

    def show_online_shops_with_budget_details(self, args):
        """
        Show all online shops details data including budget
        :param args: ARGS dict
        :return: None
        """
        db_manager = DatabaseManager()
        shop_online_flag = args.show_online_shops_details[0]
        if shop_online_flag.upper() == 'Y':
            online_shops_data = db_manager.get_all_online_shops_details_data()
            print(f'{colors[6]}{colors[7]}{colors[4]}Online Shops Details With Budget{colors[0]}')
            print(f'{colors[6]}{colors[4]}Total Data Found: {len(online_shops_data)}\n{colors[0]}')
            for data in online_shops_data:
                shop_data = self.generate_shop_data_string(data=data)
                print(shop_data)

    @staticmethod
    def notify_shops(args) -> None:
        """
        Notify shops those monthly expenditure reaches certain thresholds
        :param args: ARGS dict
        :return: None
        """
        notify_flag = args.notify_shops[0]
        data_volume = args.notify_shops[1]

        if notify_flag.upper() == 'Y':
            notifier = Notifier()
            if data_volume.upper() == 'ALL':
                notifier.notify_for_all_budget_data()
            elif data_volume.upper() == 'CURRENT':
                try:
                    budget_month = args.notify_shops[2]
                except IndexError as e:
                    budget_month = ""
                given_date, first_day, last_day = get_month_dates(budget_month)
                notifier.notify_for_current_month_budget_data(first_day=first_day, last_day=last_day)
            else:
                print(f'{colors[6]}{colors[5]}Invalid Keyword. Please Try Again{colors[0]}')

    @staticmethod
    def update_shop_budget(args) -> None:
        """
        Update shops monthly budget
        :param args: ARGS dict
        :return: None
        """
        db_manager = DatabaseManager()
        data_validator = DataValidator()
        shop_id = args.update_shop_budget[0]
        budget_amount = args.update_shop_budget[1]
        budget_month = args.update_shop_budget[2]
        given_date, first_day, last_day = get_month_dates(budget_month)
        shop_data = db_manager.get_shop_details_data_for_given_date(shop_id=shop_id, first_day=first_day, last_day=last_day)
        if shop_data:
            data_validator.validate_updated_shop_budget(shop_data=shop_data[0], shop_id=shop_id, budget_amount=budget_amount, first_day=first_day, last_day=last_day)
        else:
            print(f"{colors[6]}{colors[5]}No Shop Details Found for Given Date's Month. Please Try Again With Another Date.{colors[0]}")

    @staticmethod
    def reset_all_stored_data(args) -> None:
        """
        Restore all stored data
        :param args: ARGS dict
        :return: None
        """
        reset_flag = args.reset_data[0]
        if reset_flag.upper() == 'Y':
            seeder = DataSeeder()
            db_flag = seeder.seed()
            if db_flag:
                print(f"{colors[6]}{colors[4]}Data Restored Successfully{colors[0]}")
            else:
                print(f"{colors[6]}{colors[5]}Data Restore Failed. Please Try Again{colors[0]}")

    @staticmethod
    def close_db_connection(args):
        """
        Close database connection
        :param args: ARGS dict
        :return: None
        """
        close_flag = args.close[0]
        if close_flag.upper() == 'Y':
            db_manager = DatabaseManager()
            db_manager.cursor.close()
            db_manager.conn.close()

            if not db_manager.conn.is_connected():
                print(f"{colors[6]}{colors[4]}Database Disconnected Successfully{colors[0]}")
            else:
                print(f"{colors[6]}{colors[5]}Database Disconnection Failed. Please Try Again{colors[0]}")

    def main(self) -> None:
        """
        Driver function of notification CLI application
        :return: None
        """
        # create parser object
        app_title = 'A CLI Budget Notifier Application'
        parser = argparse.ArgumentParser(description=f"{colors[1]}{app_title}")

        # defining arguments for parser object
        parser.add_argument(
            "-db", "--database", type=str, nargs=5,
            metavar=('DB_HOST', 'DB_USER', 'DB_USER_PASSWORD', 'DB_NAME', 'DB_PORT'),
            default=None,
            help=f"Configure Database Connection"
        )

        parser.add_argument(
            "-si", "--seed", type=str, nargs=1,
            metavar='seed_initial_data', default=None,
            help="Seed Initial Data: Y/N"
        )

        parser.add_argument(
            "-sc", "--seed_current_data", type=str, nargs=2,
            metavar=('seed_current_data', 'preferred_date'), default=None,
            help=f"Seed Data for Given Month: Y/N Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's Date)"
        )

        parser.add_argument(
            "-shs", "--show_all_shops", type=str, nargs=1,
            metavar='show_all_shops_details', default=None,
            help=f"Show All Shops Details Data: Y/N"
        )

        parser.add_argument(
            "-sha", "--show_all_shops_details", type=str, nargs=1,
            metavar='show_all_shops_details_data', default=None,
            help=f"Show All Shops Details Data: Y/N"
        )

        parser.add_argument(
            "-sho", "--show_online_shops_details", type=str, nargs=1,
            metavar='show_online_shops_details_data', default=None,
            help=f"Show All Online Shops Details Data: Y/N"
        )

        parser.add_argument(
            "-nf", "--notify_shops", type=str, nargs='*',
            metavar='notify_shops, data_volume, budget_month', default=None,
            help=f"Notify Shop: Y/N ALL/CURRENT Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's Date)"
        )

        parser.add_argument(
            "-up", "--update_shop_budget", type=str, nargs=3,
            metavar=('shop_id', 'budget_amount', 'budget_month'), default=None,
            help=f"Update Shop Budget: 1-8 budget_amount Date(YYYY-MM-DD or empty string. Empty string will be replaced by today's date')"
        )

        parser.add_argument(
            "-re", "--reset_data", type=str, nargs=1,
            metavar='reset_all_db_data', default=None,
            help="Reset All Stored Data: Y/N"
        )

        parser.add_argument(
            "-cl", "--close", type=str, nargs=1,
            metavar='close_db_connection', default=None,
            help=f"Close Database Connection?: Y/N {colors[0]}"
        )

        # parse the arguments from standard input
        args = parser.parse_args()

        # calling functions depending on type of argument
        if args.database:
            self.database_config(args)
        elif args.seed:
            self.seed(args)
        elif args.seed_current_data:
            self.seed_current_data(args)
        elif args.show_all_shops:
            self.show_all_shops(args)
        elif args.show_all_shops_details:
            self.show_all_shops_with_budget_details(args)
        elif args.show_online_shops_details:
            self.show_online_shops_with_budget_details(args)
        elif args.notify_shops:
            self.notify_shops(args)
        elif args.update_shop_budget:
            self.update_shop_budget(args)
        elif args.reset_data:
            self.reset_all_stored_data(args)
        elif args.close:
            self.close_db_connection(args)


if __name__ == "__main__":
    main = Main()
    main.main()
