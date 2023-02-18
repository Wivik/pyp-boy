# Pyp-Boy

I've always dreamed about the Fallout pip-boy. This is a dirty try to make an application using Python and Flask to render it. Made for Pinephone.

## How to use

Install requirements :

```bash
pip install --user requirements.txt
```

Run flask

```bash
python -m flask run
```

Open your browser to http://localhost:5000

The left button will toggle fullscreen, the right will leave it.

The only working feature is the MAP, able to display the current location based on your current IP address and the SEARCH feature can display the requested location.

## Attribution

Unless other statement, this project is licensed under MIT.

Maps based on [OpenStreetMap](https://www.openstreetmap.org/), using [Leaflet](https://leafletjs.com) and [Stamenmaps](http://maps.stamen.com/#watercolor/12/37.7706/-122.3782) render.

Icons are from [Remix Icon](https://remixicon.com).
