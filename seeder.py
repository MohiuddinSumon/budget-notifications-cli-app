from mysql.connector import Error
from db_manager import DatabaseManager


class DataSeeder:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

    def execute_scripts_from_file(self, filename) -> None:
        """
        Read and execute sql commands from file
        :param filename: File name
        :return: None
        """
        fd = open(filename, 'r')
        sql_file = fd.read()
        fd.close()
        sql_commands = sql_file.split(';')

        for command in sql_commands:
            try:
                if command.strip() != '':
                    self.cursor.execute(command)
            except Error as e:
                print(f"Error Occurred: {e} - Command Skipped: {command}")

    def seed(self) -> bool:
        """
        Execute Initial Data Seeder
        :return: Bool
        """
        try:
            self.cursor.execute("DROP TABLE IF EXISTS t_shops")
            self.cursor.execute("DROP TABLE IF EXISTS t_budgets")

            self.execute_scripts_from_file('sql_files/db.sql')
            self.execute_scripts_from_file('sql_files/migration.sql')
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False

    def seed_current_month_data(self, initiate_date) -> bool:
        """
        Execute Initial Data Seeder
        :param initiate_date: Budget month initiate date
        :return: Bool
        """
        try:
            insert_query = """
                INSERT INTO t_budgets
                (a_shop_id, a_month, a_budget_amount, a_amount_spent)
                VALUES ( %s, %s, %s, %s )
            """
            records = [
                (1, initiate_date, 950.00, 725.67),
                (2, initiate_date, 1000.00, 886.63),
                (3, initiate_date, 650.00, 685.91),
                (4, initiate_date, 740.00, 746.92),
                (5, initiate_date, 630.00, 507.64),
                (6, initiate_date, 640.00, 946.32),
                (7, initiate_date, 980.00, 640.16),
                (8, initiate_date, 1500.00, 950.64),
            ]
            self.cursor.executemany(insert_query, records)
            self.conn.commit()
            return True
        except Error as e:
            print(e)
            return False
