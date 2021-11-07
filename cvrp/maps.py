import folium
from branca.element import Figure

def html_template(m,bounding_PolyLine):
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water Color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)
    folium.LayerControl().add_to(m)

    m.add_child(bounding_PolyLine)

    fig = Figure(height="100%")

    fig.add_child(m)

    return m