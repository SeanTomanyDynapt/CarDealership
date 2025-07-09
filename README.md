# Car Dealership Management System

A comprehensive Flask-based car dealership management system with CRUD operations, Excel integration, and Vapi voice assistant capabilities.

## Features

- **Public Website**: Complete vehicle inventory display with search functionality
- **Admin Panel**: Full CRUD operations for vehicles, parts, and services (admin/password)
- **Voice Assistant**: Vapi integration with 4 configured functions
- **Excel Integration**: 5 organized sheets for easy client editing
- **API Endpoints**: RESTful API for voice assistant integration
- **Modern UI**: Bootstrap-based responsive design

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SeanTomanyDynapt/CarDealership.git
   cd CarDealership
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app/main.py
   ```

4. **Access the application:**
   - Website: http://localhost:5001
   - Admin Panel: http://localhost:5001/admin/login (admin/password)
   - API: http://localhost:5001/api/inventory

### Deployment Options

This application is configured for multiple deployment platforms:

#### Option 1: Render.com (Recommended - Free Tier Available)

1. **Go to [Render.com](https://render.com) and sign up**
2. **Connect your GitHub account**
3. **Create a new Web Service:**
   - Choose your repository: `SeanTomanyDynapt/CarDealership`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`
4. **Deploy automatically** - Render will detect the `render.yaml` configuration

#### Option 2: Railway (Requires Paid Plan)

1. **Deploy on Railway:**
   - Go to [Railway.app](https://railway.app)
   - Upgrade to a paid plan ($5/month)
   - Deploy from GitHub repo: `SeanTomanyDynapt/CarDealership`

#### Option 3: Heroku (Free with GitHub Student Pack)

1. **Go to [Heroku.com](https://heroku.com)**
2. **Create new app from GitHub:**
   - Connect repository: `SeanTomanyDynapt/CarDealership`
   - Heroku will use `Procfile` and `runtime.txt`

#### Option 4: PythonAnywhere (Free Tier)

1. **Upload your code to [PythonAnywhere](https://pythonanywhere.com)**
2. **Set up a web app** pointing to `app/main.py`

### Configuration Files Included:

- `Procfile`: Railway/Heroku deployment
- `railway.json`: Railway-specific settings  
- `render.yaml`: Render.com configuration
- `runtime.txt`: Python version specification
- `requirements.txt`: Dependencies

## Application Structure

```
CarDealership/
├── app/
│   ├── main.py              # Main Flask application
│   └── templates/           # HTML templates
├── data/
│   ├── inventory.json       # Vehicle inventory data
│   └── parts_catalog.json   # Parts catalog data
├── static/
│   └── css/
│       └── style.css        # Custom styling
├── inventory.xlsx           # Excel file with 5 sheets
├── inventory_manager.py     # Excel/JSON data management
├── requirements.txt         # Python dependencies
├── Procfile                 # Railway deployment config
└── railway.json             # Railway settings
```

## API Endpoints

The application provides RESTful API endpoints for voice assistant integration:

- `GET /api/inventory` - Get all vehicle inventory
- `GET /api/inventory/<make>` - Get vehicles by make
- `GET /api/inventory/<make>/<model>` - Get specific model details
- `GET /api/search?q=<query>` - Search vehicles
- `GET /api/parts` - Get all parts catalog
- `GET /api/parts/<make>` - Get parts by make
- `GET /api/parts/<make>/<model>` - Get parts by model
- `GET /api/business-info` - Get business information

## Vapi Voice Assistant

The application includes 4 configured Vapi functions:

1. **Check Vehicle Availability** - Search inventory by make/model/year
2. **Get Vehicle Details** - Retrieve detailed vehicle information
3. **Search Parts** - Find available parts for specific vehicles
4. **Get Business Info** - Provide contact and business information

## Excel Integration

The system uses a 5-sheet Excel file for easy client editing:

- **Ford_Vehicles** - Ford vehicle inventory
- **Lincoln_Vehicles** - Lincoln vehicle inventory  
- **Jeep_Vehicles** - Jeep vehicle inventory
- **Parts** - Parts catalog
- **Services** - Service offerings

## Admin Panel

Access the admin panel at `/admin/login` with credentials:
- **Username**: admin
- **Password**: password

Features:
- Vehicle management (add/edit/delete)
- Parts catalog management
- Excel import/export
- Real-time inventory updates
- Professional dashboard

## Data Management

The system automatically syncs between Excel and JSON formats:
- **Excel → JSON**: Import Excel data into the web application
- **JSON → Excel**: Export web data back to Excel format
- **Real-time updates**: Changes reflect immediately in the web interface

## Production Deployment

For production deployment:
1. Change admin credentials in `app/main.py`
2. Set `debug=False` (already configured)
3. Use environment variables for sensitive data
4. Configure proper SSL/HTTPS

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the API endpoints for integration

## License

This project is licensed under the MIT License.