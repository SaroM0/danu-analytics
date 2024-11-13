from django.shortcuts import render
import pandas as pd
import folium
import plotly.graph_objects as go
from django.http import JsonResponse

file_path = 'data/df_ventas_concat.csv'
data = pd.read_csv(file_path)

city_coordinates = {
    'HARDERSFIELD': [53.6458, -1.7780],
    'ASHBORNE': [53.0167, -1.7333],
    'HORNSEY': [51.5833, -0.1167],
    'EANVERNESS': [57.4778, -4.2247],
    'SUTTON': [51.3600, -0.1940],
    'BARNCOMBE': [50.7184, -3.5339],
    'TAMWORTH': [52.6333, -1.6833],
    'EASTHAVEN': [56.5000, -2.7500],
    'BALLYMENA': [54.8639, -6.2761],
    'PEMBROKE': [51.6740, -4.9158],
    'GOULCREST': [52.0000, -1.0000],
    'STANMORE': [51.6167, -0.3167],
    'ALNERWICK': [55.4000, -1.7000],
    'BLACKPOOL': [53.8175, -3.0357],
    'CARDEND': [56.5000, -3.0000],
    'LEESIDE': [51.7500, -0.0833],
    'TARMSWORTH': [53.0000, -2.0000],
    'BROMWICH': [52.5000, -2.0000],
    'WANBORNE': [53.5000, -1.0000],
    'LUNDY': [51.1800, -4.6667],
    'OLDHAM': [53.5409, -2.1114],
    'FURNESS': [54.2000, -3.2167],
    'WINTERVALE': [51.0000, -2.0000],
    'BREDWARDINE': [52.0000, -3.0000],
    'BALERNO': [55.8833, -3.3500],
    'SHARNWICK': [51.7000, -1.3000],
    'ARBINGTON': [52.0000, -1.5000],
    'PALPERROTH': [52.5000, -2.0000],
    'CAERSHIRE': [51.8333, -2.3500],
    "KNIFE'S EDGE": [50.0000, -5.0000],
    'MOUNTMEND': [51.3000, -2.5000],
    'LARNWICK': [53.0000, -1.5000],
    'AYLESBURY': [51.8168, -0.8141],
    'CULCHETH': [53.4500, -2.5000],
    'PITMERDEN': [57.3333, -2.3167],
    'HALIVAARA': [54.0000, -2.0000],
    'LEWES': [50.8753, 0.0172],
    'PAETHSMOUTH': [51.5000, -2.0000],
    'EASTHALLOW': [54.0000, -1.5000],
    'BULLMAR': [52.0000, -0.5000],
    'BLACK HOLLOW': [52.5000, -1.5000],
    'WOLFORD': [51.0000, -0.5000],
    'PORTHCRAWL': [51.5000, -3.7000],
    'VERITAS': [54.0000, -1.0000],
    "PELLA'S WISH": [51.0000, -1.0000],
    'NORFOLK': [52.6297, 1.2923],
    'GARIGILL': [54.8000, -2.3000],
    'ABERDEEN': [57.1497, -2.0943],
    'GRAYCOTT': [53.0000, -1.0000],
    'HILLFAR': [53.0000, -1.0000],
    'GUTHRAM': [52.0000, -0.5000],
    'DRY GULCH': [53.0000, -2.5000],
    "BEGGAR'S HOLE": [51.0000, -0.5000],
    'LANTEGLOS': [50.3400, -4.5800],
    'HARTLEPOOL': [54.6900, -1.2100],
    'CLAETHORPES': [53.5600, -0.0300],
    'IRRAGIN': [51.5000, -2.5000],
    'AETHELNEY': [51.0000, -2.0000],
    'KILMARNOCK': [55.6117, -4.4958],
    'SWORDBREAK': [52.5000, -1.5000],
    'CESTERFIELD': [53.2300, -1.4200],
    'LUTON': [51.8787, -0.4200],
    'SOLARIS': [51.5000, -2.5000],
    'KELD': [54.4000, -2.2000],
    'CLARCTON': [51.0000, -1.5000],
    'DONCASTER': [53.5228, -1.1285],
    'PAENTMARWY': [53.0000, -3.0000],
}

df_cities = pd.DataFrame([
    {'City': city, 'Latitude': coords[0], 'Longitude': coords[1]}
    for city, coords in city_coordinates.items()
])

def home(request):
    return render(request, 'analytics/home.html')

def chatbot(request):
    return render(request, 'analytics/chatbot.html')

def create_map():
    m = folium.Map(location=[53.0, -1.5], zoom_start=6)
    for idx, row in df_cities.iterrows():
        city_name = row['City']
        lat, lon = row['Latitude'], row['Longitude']
        
        folium.Marker(
            location=[lat, lon],
            popup=f'<b>{city_name}</b>',  # Aseguramos que el popup tenga solo el nombre
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    return m


def map(request):
    folium_map = create_map()
    map_html = folium_map._repr_html_()
    return render(request, 'analytics/map.html', {'map_html': map_html})

def get_city_data(request, city_name):
    # Filtra los datos para la ciudad seleccionada
    city_data = data[(data['City_x'] == city_name) | (data['City_y'] == city_name)]

    if city_data.empty:
        # Retorna datos vacíos o en cero para las gráficas
        return JsonResponse({
            "total_sales": 0,
            "num_stores": 0,
            "types_of_alcohol": 0,
            "sales_by_store": 0,
            "inventory_quantity": 0,
            "num_different_products": 0,
            "top_products_quantity": {
                "names": [],  # Sin etiquetas en el eje x
                "values": []  # Sin valores en el eje y
            },
            "top_products_income": {
                "names": [],
                "values": []
            }
        })

    # Cálculos normales cuando hay datos
    total_sales = city_data['SalesDollars'].sum()
    num_stores = city_data['Store'].nunique()
    types_of_alcohol = city_data['Brand'].nunique()
    sales_by_store = city_data.groupby('Store')['SalesDollars'].sum().mean()
    inventory_quantity = city_data['SalesQuantity'].sum()
    num_different_products = city_data['Description'].nunique()

    top_products_quantity = city_data.groupby('Description').agg({
        'SalesQuantity': 'sum'
    }).reset_index().nlargest(10, 'SalesQuantity')

    top_products_income = city_data.groupby('Description').agg({
        'SalesDollars': 'sum'
    }).reset_index().nlargest(10, 'SalesDollars')

    response_data = {
        "total_sales": total_sales,
        "num_stores": num_stores,
        "types_of_alcohol": types_of_alcohol,
        "sales_by_store": sales_by_store,
        "inventory_quantity": inventory_quantity,
        "num_different_products": num_different_products,
        "top_products_quantity": {
            "names": top_products_quantity['Description'].tolist(),
            "values": top_products_quantity['SalesQuantity'].tolist()
        },
        "top_products_income": {
            "names": top_products_income['Description'].tolist(),
            "values": top_products_income['SalesDollars'].tolist()
        }
    }

    return JsonResponse(response_data)

def predictions(request):
    return render(request, 'analytics/predictions.html')

def products(request):
    return render(request, 'analytics/products.html')

def stores(request):
    return render(request, 'analytics/stores.html')
