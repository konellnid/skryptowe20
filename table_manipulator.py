import sqlite3
import exchange_rates_acquirer as rates_acquirer
import datetime

MIN_DATE = datetime.date(2012, 7, 1)
MAX_DATE = datetime.date(2016, 2, 29)

CREATE_TABLE_QUERY = "CREATE TABLE ExchangeRate (date text, rate real)"
INSERT_QUERY = "INSERT INTO ExchangeRate (date, rate) VALUES (?, ?)"
SELECT_QUERY = """SELECT ER.date, ER.rate, ROUND(orderSum, 2)
FROM ExchangeRate ER LEFT JOIN 
(
SELECT DATE(O.OrderDate) innerDate, SUM(OD.UnitPrice * OD.Quantity) orderSum
FROM OrderDetail OD JOIN `Order` O ON OD.OrderId = O.Id
GROUP BY DATE(O.OrderDate)
) ON ER.date = innerDate
ORDER BY
ER.date;"""


def get_rows_from_api(currency_code, start_date, end_date):
    api_rates = rates_acquirer.get_exchange_rates_from_api(currency_code, start_date, end_date)
    all_days_rates = rates_acquirer.expand_exchange_rates_to_range(api_rates, currency_code, start_date, end_date)

    return all_days_rates


if __name__ == "__main__":
    connection = sqlite3.connect("Northwind.sqlite")
    cursor = connection.cursor()

    cursor.execute(CREATE_TABLE_QUERY)

    rows = get_rows_from_api("usd", MIN_DATE, MAX_DATE)

    for row in rows:
        cursor.execute(INSERT_QUERY, row)

    connection.commit()

    cursor.close()
    connection.close()
