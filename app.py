import flask
import sqlite3
import datetime
from flask import abort, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)

app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

cache = Cache(app)


def get_string_date_from_date(date):
    try:
        selected_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        string_date = selected_date.strftime("%Y-%m-%d")
        return string_date
    except ValueError:
        return ""


def get_result_from_query(query, parameter):
    connection = sqlite3.connect("Northwind.sqlite")
    cursor = connection.cursor()

    cursor.execute(query, parameter)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def turn_exchange_rates_in_dictionary(rates):
    results = []
    for row in rates:
        results.append({'date': row[0], 'rate': row[1], 'is_interpolated': bool(row[2])})

    return results


def turn_sum_of_transaction_in_dictionary(transactions):
    results = []
    for row in transactions:
        results.append({'date': row[0], 'sum': row[1]})

    return results


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/request_maker')
def request_maker():
    return render_template('request_maker.html')


@app.route('/api/exchangerates/<date>', methods=['GET'])
@cache.memoize(timeout=300)
def api_single_exchange_rate(date):
    string_date = get_string_date_from_date(date)
    if "" == string_date:
        abort(400, "Wrong date format")

    select_single_exchange_rate_query = """SELECT ER.date, ER.rate, ER.is_interpolated FROM ExchangeRate ER 
        WHERE ER.date = ?;"""
    result = get_result_from_query(select_single_exchange_rate_query, (string_date,))

    return jsonify({'date': string_date, 'result': turn_exchange_rates_in_dictionary(result)})


@app.route('/api/exchangerates/<start_date>/<end_date>', methods=['GET'])
def api_exchange_rate_range(start_date, end_date):
    string_start_date = get_string_date_from_date(start_date)
    string_end_date = get_string_date_from_date(end_date)

    if string_start_date == "" or string_end_date == "" or string_end_date < string_start_date:
        abort(400, "Wrong dates provided")

    select_multiple_exchange_rates_query = """SELECT ER.date, ER.rate, ER.is_interpolated FROM ExchangeRate ER 
        WHERE ER.date >= ? AND ER.date <= ?;"""

    result = get_result_from_query(select_multiple_exchange_rates_query, (string_start_date, string_end_date))

    return jsonify({'start_date': string_start_date, 'end_date': string_end_date,
                    'result': turn_exchange_rates_in_dictionary(result)})


@app.route('/api/sum/<currency>/<date>', methods=['GET'])
@cache.memoize(timeout=300)
def api_single_sum_of_transaction(currency, date):
    string_date = get_string_date_from_date(date)

    if "" == string_date:
        abort(400, "Wrong date format")

    currency = currency.upper()

    select_single_sum_of_transaction_query = ""

    if currency == "PLN":
        select_single_sum_of_transaction_query = """SELECT ST.date, ST.pln_value FROM SumOfTransaction ST 
            WHERE ST.date = ?;"""
    elif currency == "USD":
        select_single_sum_of_transaction_query = """SELECT ST.date, ST.usd_value FROM SumOfTransaction ST 
            WHERE ST.date = ?;"""
    else:
        abort(400, "Wrong currency")

    result = get_result_from_query(select_single_sum_of_transaction_query, (string_date,))

    return jsonify({'date': string_date, 'currency': currency, 'result': turn_sum_of_transaction_in_dictionary(result)})


@app.route('/api/sum/<currency>/<start_date>/<end_date>', methods=['GET'])
def api_multiple_sum_of_transaction(currency, start_date, end_date):
    string_start_date = get_string_date_from_date(start_date)
    string_end_date = get_string_date_from_date(end_date)

    if string_start_date == "" or string_end_date == "" or string_end_date < string_start_date:
        abort(400, "Wrong dates provided")

    currency = currency.upper()

    select_single_sum_of_transaction_query = ""

    if currency == "PLN":
        select_single_sum_of_transaction_query = """SELECT ST.date, ST.pln_value FROM SumOfTransaction ST 
            WHERE ST.date >= ? AND ST.DATE <= ?;"""
    elif currency == "USD":
        select_single_sum_of_transaction_query = """SELECT ST.date, ST.usd_value FROM SumOfTransaction ST 
            WHERE ST.date >= ? AND ST.date <= ?;"""
    else:
        abort(400, "Wrong currency")

    result = get_result_from_query(select_single_sum_of_transaction_query, (string_start_date, string_end_date))

    return jsonify({'start_date': string_start_date, 'end_date': string_end_date, 'currency': currency,
                    'result': turn_sum_of_transaction_in_dictionary(result)})


if __name__ == "__main__":
    app.run()
