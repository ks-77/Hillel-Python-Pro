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
        query = f'''SELECT BillingCity
                    FROM (
                        SELECT invoices.BillingCity, DENSE_RANK() OVER (ORDER BY COUNT(invoice_items.Quantity) DESC) AS rank
                        FROM invoices
                        JOIN invoice_items ON invoice_items.InvoiceId = invoices.InvoiceId
                        JOIN tracks ON tracks.TrackId = invoice_items.TrackId
                        JOIN genres ON genres.GenreId = tracks.GenreId
                        WHERE genres.Name = '{genre}'
                        GROUP BY invoices.BillingCity
                    )
                    WHERE rank =1'''
        result = execute_query(query=query)
        return result
    else:
        return "genre - required parameter"


if __name__ == '__main__':
    app.run(debug=True)
