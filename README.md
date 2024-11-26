# Danu Project

## Overview

Danu is a Django-based web application for sales data analysis. It provides various tools for filtering, visualizing, and summarizing sales information using interactive maps and charts.

### Key Features

- Interactive map visualization of sales data using **Folium**.
- Advanced filtering options for products, stores, and sales data.
- API endpoints for accessing filtered and summarized data.
- Dynamic charts with **Plotly** for detailed sales insights.

---

## Project Structure

```
danu/
├── analytics/        # Main Django app
│   ├── migrations/   # Database migration files
│   ├── static/       # Static assets (CSS, JS, images)
│   ├── templates/    # HTML templates
│   ├── views.py      # Core logic for views
│   └── ...           # Other files (models.py, forms.py, etc.)
├── data/             # CSV and data files for the application
├── db.sqlite3        # SQLite database
├── manage.py         # Django's management script
├── requiremetns.txt  # Python dependencies
├── static/           # Project-wide static files
└── README.md         # Documentation file
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd danu
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate   # For Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requiremetns.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Load initial data (if required):

   ```bash
   python manage.py loaddata initial_data.json
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Access the Application

Open your browser and go to: `http://127.0.0.1:8000`

---

## Usage

### Endpoints

- **Home Page:** `/`
- **Chatbot:** `/chatbot/`
- **Map:** `/map/`
- **Filter Data API:** `/filter_data/`
- **Products:** `/products/`
- **Stores:** `/stores/`

### Example API Request

To filter sales data for a specific store:

```bash
curl -X POST http://127.0.0.1:8000/filter_data/ -H "Content-Type: application/json" -d '{
    "tienda": "Store_Name",
    "fecha_inicio": "2023-01-01",
    "fecha_fin": "2023-12-31"
}'
```

---

## Key Dependencies

- **Django:** Web framework
- **Pandas:** Data processing
- **Folium:** Interactive maps
- **Plotly:** Data visualization

To view the complete list of dependencies, check `requiremetns.txt`.

---
