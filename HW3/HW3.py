import requests
from faker import Faker
from flask import Flask, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs
import json
from babel.numbers import get_currency_symbol


app = Flask(__name__)

faker_instance = Faker()


@app.route('/generate-students')
@use_kwargs(
    {
        "count": fields.Int(
            missing=10,
            validate=[validate.Range(min=1, max=1000)]
        ),
    },
    location="query"
)
def generate_students(count: int) -> object:
    students = []
    for _ in range(count):
        students.append(
            {
                "1.First name": faker_instance.first_name(),
                "2.Last name": faker_instance.last_name(),
                "3.Email": faker_instance.email(),
                "4.Password": faker_instance.password(),
                "5.Birthday": f"{faker_instance.date_of_birth(None, 18, 60)}",

            }
        )
    with open("students.json", "w") as jsonfile:
        json.dump(students, jsonfile, indent=4)
    return jsonify(students)


@app.route('/get_bitcoin_value')
@use_kwargs(
    {
        "convert": fields.Int(
            missing=1,
            validate=[validate.Range(min=1, max=1000)]
        ),
        "currency": fields.Str(
            load_default="USD",
            validate=[validate.OneOf(["UAH", "USD", "EUR"])]
        )
    },
    location="query"
)
def get_bitcoin_value(currency, convert):
    url = f'https://bitpay.com/api/rates/BTC/{currency.upper()}'
    result = requests.get(url)
    if result.status_code != 200:
        return Response("Error", status=result.status_code)
    data = result.json()
    value = data.get('rate')
    price_per_quantity = value * convert
    symbol = "₴" if currency.upper() == "UAH" else get_currency_symbol(currency.upper(), locale='en_US')
    data = {
        "1. Currency": currency,
        "2. Currency symbol": symbol,
        f"3. Price per 1 BTC": value,
        "4. Quantity": convert,
        "5. Price per quantity": price_per_quantity
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
