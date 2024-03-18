import math
from db_handler import execute_query
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_kwargs


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        dif_x = point.x - self.x
        dif_y = point.y - self.y
        return math.sqrt(dif_x ** 2 + dif_y ** 2) <= self.radius


app = Flask(__name__)


@app.route('/stats_by_city')
@use_kwargs(
    {
        "genre": fields.Str(
            load_default=None
        ),
    },
    location="query"
)
def stats_by_city(genre):
    if genre:
        query = f'''SELECT MAX(invoices.BillingCity)
                    FROM genres
                    JOIN tracks ON tracks.GenreId = genres.GenreId
                    JOIN invoice_items ON invoice_items.TrackId = tracks.TrackId
                    JOIN invoices ON invoices.InvoiceId = invoice_items.InvoiceId
                    WHERE genres.Name= "{genre}"'''
        result = execute_query(query=query)
        return result
    else:
        return "genre - required parameter"


if __name__ == '__main__':
    app.run(debug=True)
