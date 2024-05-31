import folium
import pandas

data = pandas.read_csv("Volcanoes_USA.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])


def color_deter(elevation):
    if elevation < 1000:
        return 'beige'
    elif 1000 <= elevation < 3000:
        return "green"
    else:
        return "red"


v_map = folium.Map(location=[38.58, -99.96], zoom_start=6)

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(el) + "m",
                                     fill_color=color_deter(el), color='grey', fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")


with open('world.json', 'r', encoding='utf-8-sig') as f:
    geojson_data = f.read()


def style_function(feature):
    population = feature['properties'].get('POP2005', 0)
    if population < 10000000:
        return {'fillColor': 'green'}
    elif 10000000 <= population < 20000000:
        return {'fillColor': 'orange'}
    else:
        return {'fillColor': 'red'}


fgp.add_child(folium.GeoJson(
    data=geojson_data,
    style_function=style_function,
    check_first=True  # This ensures only valid geometries are rendered
))

v_map.add_child(fgv)
v_map.add_child(fgp)
v_map.add_child(folium.LayerControl())

v_map.save("Map1.html")
