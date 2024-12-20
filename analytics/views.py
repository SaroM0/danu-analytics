from django.shortcuts import render
import pandas as pd
import folium
import plotly.graph_objects as go
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Archivo de datos inicial para cargar información
file_path = 'data/df_ventas_concat.csv'

# Función para cargar datos desde un archivo CSV
def cargar_datos(filepath):
    try:
        # Leer el archivo CSV y procesar columnas relevantes
        df = pd.read_csv(filepath)
        df['SalesDate'] = pd.to_datetime(df['SalesDate'], format='%m/%d/%Y', errors='coerce')
        df['Store'] = df['Store'].astype(str)  # Asegurarse de que la columna 'Store' sea de tipo cadena
        return df
    except FileNotFoundError:
        # Manejo de errores si el archivo no existe
        return pd.DataFrame()

# Carga de los datos al iniciar el servidor
data = cargar_datos(file_path) 


# Diccionario de coordenadas para las ciudades
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

# Creación de un DataFrame con las coordenadas de las ciudades
df_cities = pd.DataFrame([
    {'City': city, 'Latitude': coords[0], 'Longitude': coords[1]}
    for city, coords in city_coordinates.items()
])

# Vista principal para cargar la página inicial
def home(request):
    return render(request, 'analytics/home.html')

# Vista secundaria para la página del chatbot
def chatbot(request):
    return render(request, 'analytics/chatbot.html')

# Función para generar un mapa interactivo utilizando Folium
def create_map():
    m = folium.Map(location=[53.0, -1.5], zoom_start=6, tiles="Cartodb Positron")
    for idx, row in df_cities.iterrows():
        city_name = row['City']
        lat, lon = row['Latitude'], row['Longitude']
        
        # Añadir un marcador para cada ciudad
        folium.Marker(
            location=[lat, lon],
            popup=f'<b>{city_name}</b>',  # Aseguramos que el popup tenga solo el nombre
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    return m

# Vista API para filtrar datos por tienda y rango de fechas
@csrf_exempt
def filter_data(request):
    if request.method == "POST":
        try:
           # Parsear datos del cuerpo de la solicitud
            body = json.loads(request.body)
            tienda = str(body.get("tienda"))  # Convertir tienda a cadena
            fecha_inicio = pd.to_datetime(body.get("fecha_inicio"), errors='coerce')
            fecha_fin = pd.to_datetime(body.get("fecha_fin"), errors='coerce')

            # Validar fechas
            if pd.isnull(fecha_inicio) or pd.isnull(fecha_fin):
                return JsonResponse({"error": "Fechas inválidas."})

            # Filtrar datos según los criterios especificados
            data_filtrada = data[
                (data['Store'] == tienda) &
                (data['SalesDate'] >= fecha_inicio) &
                (data['SalesDate'] <= fecha_fin)
            ]

            if data_filtrada.empty:
                return JsonResponse({"error": "No hay datos para los filtros seleccionados."})
            
            data_filtrada.fillna("", inplace=True)

            # Preparar datos para la tabla y la gráfica
            tabla = data_filtrada[['Store', 'City_x', 'SalesQuantity', 'SalesDollars', 'SalesDate', 'Description']].to_dict(orient='records')
            ventas_diarias = data_filtrada.groupby('SalesDate')[['SalesDollars']].sum().reset_index()
            ventas_diarias_data = {
                "SalesDate": ventas_diarias['SalesDate'].dt.strftime('%Y-%m-%d').tolist(),
                "SalesDollars": ventas_diarias['SalesDollars'].tolist()
            }

            return JsonResponse({"tabla": tabla, "ventas_diarias": ventas_diarias_data})

        except Exception as e:
            print(f"Error en el procesamiento: {str(e)}")
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Método no permitido"}, status=405)



def get_global_data():
    total_sales = data['SalesDollars'].sum()
    num_stores = data['Store'].nunique()
    types_of_alcohol = data['Brand'].nunique()
    return {
        "total_sales": total_sales,
        "num_stores": num_stores,
        "types_of_alcohol": types_of_alcohol
    }

def map(request):
    folium_map = create_map()
    map_html = folium_map._repr_html_()
    return render(request, 'analytics/map.html', {'map_html': map_html})

def get_global_data_api(request):
    global_data = get_global_data()
    return JsonResponse(global_data)

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
            },
            "monthly_sales": {
                "months": [],
                "sales": []
            },
            "sales_prices": {
                "months": [],
                "prices": []
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
    
    city_data['SalesDate'] = pd.to_datetime(city_data['SalesDate'])
    city_data['Month'] = city_data['SalesDate'].dt.month_name()
    
    monthly_sales = city_data.groupby('Month')['SalesDollars'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values(by='Month', key=lambda x: pd.Categorical(x, categories=[
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ], ordered=True))
    
    sales_prices = city_data[['Month', 'SalesPrice']].dropna()

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
         },
        "monthly_sales": {
            "months": monthly_sales['Month'].tolist(),
            "sales": monthly_sales['SalesDollars'].tolist()
        },
        "sales_prices": {
            "months": sales_prices['Month'].tolist(),
            "prices": sales_prices['SalesPrice'].tolist()
        }
    }

    return JsonResponse(response_data)



@csrf_exempt
def filter_product_weekday_sales(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            producto = body.get("producto")
            fecha_inicio = pd.to_datetime(body.get("fecha_inicio"), errors='coerce')
            fecha_fin = pd.to_datetime(body.get("fecha_fin"), errors='coerce')

            if pd.isnull(fecha_inicio) or pd.isnull(fecha_fin):
                return JsonResponse({"error": "Fechas inválidas."})

            # Filtrar datos
            data_filtrada = data[
                (data['Description'] == producto) &
                (data['SalesDate'] >= fecha_inicio) &
                (data['SalesDate'] <= fecha_fin)
            ]

            if data_filtrada.empty:
                return JsonResponse({"error": "No hay datos para los filtros seleccionados."})

            # Preparar datos para la tabla
            tabla = data_filtrada[['Description', 'SalesQuantity', 'SalesDollars', 'SalesDate', 'Store']].to_dict(orient='records')

            # Crear columna para días de la semana
            dias_semana_map = {
                0: "Lunes",
                1: "Martes",
                2: "Miércoles",
                3: "Jueves",
                4: "Viernes",
                5: "Sábado",
                6: "Domingo"
            }
            data_filtrada['DiaSemana'] = data_filtrada['SalesDate'].dt.weekday.map(dias_semana_map)

            # Calcular promedio de ventas por día de la semana
            promedio_dias = (
                data_filtrada.groupby('DiaSemana')[['SalesDollars']].mean()
                .reindex(["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"])  # Ordenar días
                .reset_index()
            )
            promedio_dias.rename(columns={'SalesDollars': 'PromedioVentas'}, inplace=True)

            # Preparar datos para la gráfica
            ventas_dias_data = {
                "DiasSemana": promedio_dias['DiaSemana'].tolist(),
                "PromedioVentas": promedio_dias['PromedioVentas'].tolist()
            }

            return JsonResponse({"tabla": tabla, "ventas_semana": ventas_dias_data})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Método no permitido"}, status=405)


def predictions(request):
    image_indices = range(1, 6)
    return render(request, 'analytics/predictions.html', {'image_indices': image_indices})

# Vista para obtener y mostrar información sobre los productos disponibles
def products(request):
    if request.method == "GET":
        # Obtiene la lista de productos únicos, omitiendo valores nulos
        productos = data['Description'].dropna().unique().tolist()
        # Calcula la fecha mínima y máxima en los datos, formateándolas como 'YYYY-MM-DD'
        fecha_min = data['SalesDate'].min().strftime('%Y-%m-%d')
        fecha_max = data['SalesDate'].max().strftime('%Y-%m-%d')

        # Renderiza la plantilla 'products.html', pasando los datos procesados
        return render(request, 'analytics/products.html', {
            'productos': productos,
            'fecha_min': fecha_min,
            'fecha_max': fecha_max
        })

# Vista para obtener y mostrar información sobre las tiendas disponibles
def stores(request):
    if request.method == "GET":
        # Obtiene la lista de tiendas únicas, omitiendo valores nulos
        tiendas = data['Store'].dropna().unique().tolist()
         # Calcula la fecha mínima y máxima en los datos, formateándolas como 'YYYY-MM-DD'
        fecha_min = data['SalesDate'].min().strftime('%Y-%m-%d')
        fecha_max = data['SalesDate'].max().strftime('%Y-%m-%d')

        # Renderiza la plantilla 'stores.html', pasando los datos procesados
        return render(request, 'analytics/stores.html', {
            'tiendas': tiendas,
            'fecha_min': fecha_min,
            'fecha_max': fecha_max
        })