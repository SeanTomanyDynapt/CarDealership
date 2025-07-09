# Premium Auto Dealership Website

A Python Flask web application for a car dealership specializing in Ford, Lincoln, and Jeep vehicles (model years 1990-present).

## Features

- **Home Page**: Business information, hours, and contact details
- **Brand Pages**: Dedicated pages for Ford, Lincoln, and Jeep models
- **Model Details**: Individual pages for each vehicle model with specifications
- **Services & Parts**: Service center information and parts catalog
- **Responsive Design**: Mobile-friendly Bootstrap interface

## Project Structure

```
CarDealership/
├── app/
│   ├── main.py              # Flask application entry point
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── home.html        # Homepage
│       ├── make.html        # Brand listing page
│       ├── model.html       # Individual model page
│       └── services.html    # Services and parts page
├── static/
│   ├── css/
│   │   └── style.css        # Custom styling
│   └── images/              # Vehicle images (placeholder)
├── data/
│   ├── inventory.json       # Vehicle model data
│   └── parts_catalog.json   # Parts and services data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   cd app
   python main.py
   ```

3. **Access the Website**
   - Open your browser and go to `http://localhost:5000`

## Development Commands

- **Run the application**: `python app/main.py`
- **Check syntax**: `python -m py_compile app/main.py`
- **Interactive debugging**: `python -i app/main.py`

## Data Structure

### Inventory Data
- Located in `data/inventory.json`
- Contains Ford, Lincoln, and Jeep models from 1990-present
- Includes model descriptions, categories, features, and available years

### Parts Catalog
- Located in `data/parts_catalog.json`
- Organized by brand and model
- Categories include Engine, Transmission, Brakes, Suspension, and Electrical
- Also includes service offerings

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Data Storage**: JSON files
- **Responsive Design**: Bootstrap grid system

## Future Enhancements

- Database integration
- User authentication
- Online parts ordering
- Service appointment scheduling
- Vehicle inventory management
- Voice agent integration

## Contact

For questions or support, contact the development team or refer to the business contact information on the website.