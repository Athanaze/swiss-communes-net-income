import csv
from operator import itemgetter
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim
TOP_N = 100
with open('file.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    data = []
    for row in reader:
        if row['VARIABLE'] == 'Revenu net par habitant/-e, en francs':
            data.append((row['GEO_NAME'], float(row['VALUE'])))
    data.sort(key=itemgetter(1), reverse=True)
    data = data[:TOP_N]
    communes = [row[0] for row in data]
    
    # Create the map
    map = folium.Map(location=[46.8182, 8.2275], zoom_start=8)

    geolocator = Nominatim(user_agent="swiss_communes_map")

    for commune in communes:
        location = geolocator.geocode(commune + ", Switzerland")
        folium.Marker([location.latitude, location.longitude], popup=commune).add_to(map)

    map.save('swiss_communes_map.html')
    
    values = [row[1] for row in data]
    plt.bar(communes, values)
    plt.xticks(rotation=90)
    plt.yticks(range(0, int(max(values)), 10000))
    plt.tight_layout()
    plt.show()