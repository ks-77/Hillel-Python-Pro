import string
from webargs import fields, validate
from flask import Flask
import random
from webargs.flaskparser import use_kwargs
import pandas as pd


app = Flask(__name__)


@app.route("/generate-password")
@use_kwargs({"length": fields.Int(
    missing=10,
    validate=[validate.Range(min_inclusive=True, min=10, max_inclusive=True, max=20)]),
    },
    location='query'
)
def generate_password(length: int) -> object:
    return f"Your password: {''.join(random.choices(
        string.digits+string.ascii_lowercase+string.ascii_uppercase+string.punctuation,
        k=length
        ))}"


@app.route('/calculate-average')
def calculate_average():
    file = pd.read_csv("D:\Загрузки\hw.csv")
    average_height = file[" Height(Inches)"].mean()
    average_weight = file[" Weight(Pounds)"].mean()
    return f"Average height (Inches): {average_height}\nAverage weight (Pounds): {average_weight}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)