ALTER TABLE t_budgets
ADD COLUMN notification VARCHAR(50) DEFAULT "" AFTER a_amount_spent,
ADD COLUMN first_notified_date DATE DEFAULT NULL AFTER notification,
ADD COLUMN last_notified_date DATE DEFAULT NULL AFTER first_notified_date;
