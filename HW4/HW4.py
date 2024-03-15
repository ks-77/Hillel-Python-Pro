from db_handler import execute_query
from flask import Flask
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


@app.route('/all-track-info')
@use_kwargs(
    {
        "track_id": fields.Int(
            missing=1,
            validate=[validate.Range(1, 3503)]
        ),
    },
    location="query"
)
def get_all_info_about_track(track_id):
    query = f'''SELECT DISTINCT tracks.TrackId, tracks.Name, Composer, Milliseconds, UnitPrice, media_types.Name,
                genres.Name, albums.Title, artists.Name,playlists.Name,
                (SELECT SUM(tracks.Milliseconds) / 3600000 FROM tracks)
                FROM tracks
                JOIN media_types ON tracks.MediaTypeId = media_types.MediaTypeId
                JOIN genres ON tracks.GenreId = genres.GenreId
                JOIN albums ON tracks.AlbumId = albums.AlbumId
                JOIN artists ON albums.ArtistId = artists.ArtistId
                JOIN playlist_track ON tracks.TrackId = playlist_track.TrackId
                JOIN playlists ON playlist_track.PlaylistId = playlists.PlaylistId
                WHERE tracks.TrackId = {track_id}'''
    result = execute_query(query=query)
    return result


@app.route('/order_price')
@use_kwargs(
    {
        "country": fields.Str(
            load_default=None,
        ),
    },
    location="query"
)
def order_price(country):
    if country is not None:
        query = f'''SELECT SUM(Total), BillingCountry
                    FROM (invoices)
                    WHERE invoices.BillingCountry= '{country}' '''
    else:
        query = f'''SELECT SUM(Total), BillingCountry
                    FROM (invoices)
                    GROUP BY BillingCountry'''
    result = execute_query(query=query)
    return result


if __name__ == '__main__':
    app.run(debug=True)
