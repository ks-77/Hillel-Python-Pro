import string
from flask import Flask
import random
import pandas as pd


app = Flask(__name__)


@app.route("/generate-password")
def generate_password():
    length = random.randint(10, 20)
    required_symbols = []
    for _ in range(length // 4):
        required_symbols.append(random.choice(string.ascii_uppercase))
        required_symbols.append(random.choice(string.ascii_lowercase))
        required_symbols.append(random.choice(string.digits))
        required_symbols.append(random.choice(string.punctuation))
    if len(required_symbols) != length:
        for _ in range(length - len(required_symbols)):
            required_symbols.append(random.choice(string.ascii_letters))
    random.shuffle(required_symbols)
    password = ''.join(required_symbols)
    return password


@app.route('/calculate-average')
def calculate_average():
    file = pd.read_csv("hw.csv")
    average_height = file[" Height(Inches)"].mean()
    average_weight = file[" Weight(Pounds)"].mean()
    return f"Average height (Inches): {average_height}\nAverage weight (Pounds): {average_weight}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)