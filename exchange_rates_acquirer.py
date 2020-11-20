import requests
import datetime

MIN_AVAILABLE_DATE = "2002-01-02"
MAX_DAYS = 93
DELTA_ONE_DAY = datetime.timedelta(days=1)


def format_datetime_to_string(date):
    return date.strftime("%Y-%m-%d")


def make_get_request_for_range(currency_code, start_date, end_date):
    start_date_string = format_datetime_to_string(start_date)
    end_date_string = format_datetime_to_string(end_date)
    response = requests.get(
        "http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/{}/?format=json".format(currency_code, start_date_string,
                                                                                   end_date_string))
    if response.status_code == 200:
        result = []
        rates = response.json()["rates"]
        for single_day_data in rates:
            result.append((single_day_data["effectiveDate"], single_day_data["mid"]))
        return result
    else:
        return []


def make_get_request_for_single_day(currency_code, day_date):
    day_date_string = format_datetime_to_string(day_date)

    response = requests.get(
        "http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/?format=json".format(currency_code, day_date_string))
    if response.status_code == 200:
        rates_for_one_day = response.json()["rates"][0]
        return rates_for_one_day["effectiveDate"], rates_for_one_day["mid"]
    else:
        return []


def get_previous_available_day_date(currency_code, day_data):
    day_data -= DELTA_ONE_DAY
    single_day_data = make_get_request_for_single_day(currency_code, day_data)

    while not single_day_data:
        day_data -= DELTA_ONE_DAY
        single_day_data = make_get_request_for_single_day(currency_code, day_data)

    return single_day_data


def split_dates_by_max_days(start_date, end_date):
    split_dates = []

    while (end_date - start_date).days > MAX_DAYS:
        split_dates.append((start_date, start_date + datetime.timedelta(days=MAX_DAYS)))
        start_date += datetime.timedelta(days=(MAX_DAYS + 1))

    split_dates.append((start_date, end_date))
    return split_dates


def get_exchange_rates_from_api(currency_code, start_date, end_date):
    if end_date < start_date:
        return []

    split_dates = split_dates_by_max_days(start_date, end_date)

    exchange_rates = []
    for single_date_range in split_dates:
        single_range_exchange = (make_get_request_for_range(currency_code, single_date_range[0], single_date_range[1]))
        exchange_rates.extend(single_range_exchange)

    return exchange_rates


def day_is_in_api(api_exchange_rates, date, api_rates_index):
    if api_rates_index < len(api_exchange_rates):
        if format_datetime_to_string(date) == api_exchange_rates[api_rates_index][0]:
            return True
        else:
            return False
    else:
        return False


def expand_exchange_rates_to_range(api_exchange_rates, currency_code, start_date, end_date):
    all_days_exchange_rates = []

    if api_exchange_rates[0][0] != format_datetime_to_string(start_date):
        previous_available_day_data = get_previous_available_day_date(currency_code, start_date)
        # marks start_date with the value from previous available day
        all_days_exchange_rates.append((format_datetime_to_string(start_date), previous_available_day_data[1]))
        start_date += DELTA_ONE_DAY

    api_rates_index = 0
    while start_date <= end_date:
        if day_is_in_api(api_exchange_rates, start_date, api_rates_index):
            all_days_exchange_rates.append(api_exchange_rates[api_rates_index])
            api_rates_index += 1
        else:
            all_days_exchange_rates.append(
                (format_datetime_to_string(start_date), exchange_rates_from_api[api_rates_index - 1][1]))

        start_date += DELTA_ONE_DAY

    return all_days_exchange_rates


if __name__ == "__main__":
    start = datetime.date(2020, 1, 1)
    end = datetime.date(2020, 10, 12)
    currency_usd = "usd"
    exchange_rates_from_api = get_exchange_rates_from_api(currency_usd, start, end)

    all_days_rates = expand_exchange_rates_to_range(exchange_rates_from_api, currency_usd, start, end)

    for rate in all_days_rates:
        print(rate)
