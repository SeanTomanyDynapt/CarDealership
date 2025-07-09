from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, send_file, session
import json
import os
import sys
from pathlib import Path
from functools import wraps

# Add parent directory to path to import inventory_manager
sys.path.append(str(Path(__file__).parent.parent))
from inventory_manager import InventoryManager

app = Flask(__name__, template_folder='templates', static_folder='../static')
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Initialize inventory manager
inventory_manager = InventoryManager()

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Load data function with reload capability
def load_json_data(filename):
    try:
        with open(f'data/{filename}', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def reload_data():
    """Reload inventory and parts data from JSON files"""
    global inventory, parts_catalog
    inventory = load_json_data('inventory.json')
    parts_catalog = load_json_data('parts_catalog.json')

# Initial data load
reload_data()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ford')
def ford():
    ford_models = inventory.get('Ford', {})
    return render_template('make.html', make='Ford', models=ford_models)

@app.route('/lincoln')
def lincoln():
    lincoln_models = inventory.get('Lincoln', {})
    return render_template('make.html', make='Lincoln', models=lincoln_models)

@app.route('/jeep')
def jeep():
    jeep_models = inventory.get('Jeep', {})
    return render_template('make.html', make='Jeep', models=jeep_models)

@app.route('/model/<make>/<model_name>')
def model_detail(make, model_name):
    model_data = inventory.get(make, {}).get(model_name, {})
    return render_template('model.html', make=make, model_name=model_name, model_data=model_data)

@app.route('/services')
def services():
    return render_template('services.html', parts=parts_catalog)

# API endpoints for Vapi integration
@app.route('/api/inventory')
def api_inventory():
    """Get all inventory data"""
    return jsonify(inventory)

@app.route('/api/inventory/<make>')
def api_inventory_by_make(make):
    """Get inventory for a specific make"""
    make_data = inventory.get(make, {})
    if not make_data:
        return jsonify({"error": f"No inventory found for {make}"}), 404
    return jsonify({make: make_data})

@app.route('/api/inventory/<make>/<model>')
def api_inventory_by_model(make, model):
    """Get details for a specific make and model"""
    model_data = inventory.get(make, {}).get(model, {})
    if not model_data:
        return jsonify({"error": f"No data found for {make} {model}"}), 404
    return jsonify({
        "make": make,
        "model": model,
        "data": model_data
    })

@app.route('/api/search')
def api_search():
    """Search inventory by keyword"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    results = []
    for make, models in inventory.items():
        for model, data in models.items():
            # Search in model name, description, category, and features
            searchable_text = f"{make} {model} {data.get('description', '')} {data.get('category', '')} {' '.join(data.get('features', []))}".lower()
            
            if query in searchable_text:
                results.append({
                    "make": make,
                    "model": model,
                    "category": data.get('category'),
                    "description": data.get('description'),
                    "features": data.get('features', []),
                    "years": data.get('years', [])
                })
    
    return jsonify({"results": results, "count": len(results)})

@app.route('/api/parts')
def api_parts():
    """Get all parts catalog"""
    return jsonify(parts_catalog)

@app.route('/api/parts/<make>')
def api_parts_by_make(make):
    """Get parts for a specific make"""
    make_parts = parts_catalog.get(make, {})
    if not make_parts:
        return jsonify({"error": f"No parts found for {make}"}), 404
    return jsonify({make: make_parts})

@app.route('/api/parts/<make>/<model>')
def api_parts_by_model(make, model):
    """Get parts for a specific make and model"""
    model_parts = parts_catalog.get(make, {}).get(model, {})
    if not model_parts:
        return jsonify({"error": f"No parts found for {make} {model}"}), 404
    return jsonify({
        "make": make,
        "model": model,
        "parts": model_parts
    })

@app.route('/api/business-info')
def api_business_info():
    """Get business information"""
    return jsonify({
        "name": "Premium Auto Dealership",
        "phone": "(555) 123-4567",
        "email": "info@premiumauto.com",
        "address": "123 Auto Lane, Car City, CC 12345",
        "hours": {
            "monday_friday": "8:00 AM - 7:00 PM",
            "saturday": "9:00 AM - 6:00 PM",
            "sunday": "12:00 PM - 5:00 PM"
        },
        "brands": ["Ford", "Lincoln", "Jeep"],
        "services": [
            "New & Used Vehicle Sales",
            "Professional Service Center",
            "Genuine Parts & Accessories",
            "Financing Options Available"
        ]
    })

# Authentication routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('home'))

# Admin CRUD functionality
@app.route('/admin')
@admin_required
def admin_dashboard():
    """Main admin dashboard with statistics"""
    # Load current data
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    parts_data = inventory_manager.load_json(inventory_manager.parts_file)
    
    # Handle case where data might be in different format
    if not isinstance(inventory_data, dict):
        inventory_data = {}
    if not isinstance(parts_data, dict):
        parts_data = {}
    
    # Calculate statistics
    total_vehicles = 0
    total_combinations = 0
    total_parts = 0
    
    for make, models in inventory_data.items():
        if isinstance(models, dict):
            total_vehicles += len(models)
            for model, data in models.items():
                if isinstance(data, dict):
                    total_combinations += len(data.get('years', []))
    
    for make, make_parts in parts_data.items():
        if isinstance(make_parts, dict):
            for model, categories in make_parts.items():
                if isinstance(categories, dict):
                    for category, parts_list in categories.items():
                        if isinstance(parts_list, list):
                            total_parts += len(parts_list)
    
    stats = {
        'total_vehicles': total_vehicles,
        'total_combinations': total_combinations,
        'total_parts': total_parts,
        'makes': list(inventory_data.keys()),
        'excel_exists': os.path.exists('inventory.xlsx')
    }
    
    return render_template('crud_dashboard.html', stats=stats)

@app.route('/admin/vehicles')
@admin_required
def admin_vehicles():
    """Vehicle management page"""
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    if not isinstance(inventory_data, dict):
        inventory_data = {}
    return render_template('crud_vehicles.html', inventory=inventory_data)

@app.route('/admin/vehicles/<make>')
@admin_required
def admin_vehicles_by_make(make):
    """Vehicle management for specific make"""
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    make_inventory = inventory_data.get(make, {})
    return render_template('crud_vehicles_make.html', make=make, vehicles=make_inventory)

@app.route('/admin/vehicle/add', methods=['GET', 'POST'])
@admin_required
def admin_add_vehicle():
    """Add new vehicle"""
    if request.method == 'POST':
        data = request.get_json()
        
        make = data['make']
        model = data['model']
        year = int(data['year'])
        
        inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
        
        if make not in inventory_data:
            inventory_data[make] = {}
        
        if model not in inventory_data[make]:
            inventory_data[make][model] = {
                'years': [],
                'category': data.get('category', ''),
                'description': data.get('description', f'{make} {model}'),
                'features': data.get('features', []),
                'price_range': data.get('price_range', ''),
                'status': data.get('status', 'Available')
            }
        
        if year not in inventory_data[make][model]['years']:
            inventory_data[make][model]['years'].append(year)
            inventory_data[make][model]['years'].sort()
        
        inventory_manager.save_json(inventory_data, inventory_manager.inventory_file)
        reload_data()  # Reload the global data
        return jsonify({'success': True})
    
    return render_template('crud_add_vehicle.html')

@app.route('/admin/vehicle/edit/<make>/<model>')
@admin_required
def admin_edit_vehicle(make, model):
    """Edit vehicle"""
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    vehicle = inventory_data.get(make, {}).get(model, {})
    return render_template('crud_edit_vehicle.html', make=make, model=model, vehicle=vehicle)

@app.route('/admin/vehicle/update', methods=['POST'])
@admin_required
def admin_update_vehicle():
    """Update vehicle"""
    data = request.get_json()
    
    make = data['make']
    model = data['model']
    
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    
    if make in inventory_data and model in inventory_data[make]:
        inventory_data[make][model].update({
            'category': data.get('category', ''),
            'description': data.get('description', ''),
            'features': data.get('features', []),
            'price_range': data.get('price_range', ''),
            'status': data.get('status', 'Available'),
            'years': sorted(data.get('years', []))
        })
        
        inventory_manager.save_json(inventory_data, inventory_manager.inventory_file)
        reload_data()  # Reload the global data
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Vehicle not found'})

@app.route('/admin/vehicle/delete/<make>/<model>')
@admin_required
def admin_delete_vehicle(make, model):
    """Delete vehicle"""
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    
    if make in inventory_data and model in inventory_data[make]:
        del inventory_data[make][model]
        
        # Remove make if no models left
        if not inventory_data[make]:
            del inventory_data[make]
        
        inventory_manager.save_json(inventory_data, inventory_manager.inventory_file)
        reload_data()  # Reload the global data
        flash(f'Successfully deleted {make} {model}', 'success')
    else:
        flash(f'Vehicle {make} {model} not found', 'error')
    
    return redirect(url_for('admin_vehicles'))

@app.route('/admin/parts')
@admin_required
def admin_parts():
    """Parts management page"""
    parts_data = inventory_manager.load_json(inventory_manager.parts_file)
    return render_template('crud_parts.html', parts=parts_data)

@app.route('/admin/part/add', methods=['GET', 'POST'])
@admin_required
def admin_add_part():
    """Add new part"""
    if request.method == 'POST':
        data = request.get_json()
        
        make = data['make']
        model = data['model']
        category = data['category']
        part = data['part']
        
        parts_data = inventory_manager.load_json(inventory_manager.parts_file)
        
        if make not in parts_data:
            parts_data[make] = {}
        if model not in parts_data[make]:
            parts_data[make][model] = {}
        if category not in parts_data[make][model]:
            parts_data[make][model][category] = []
        
        if part not in parts_data[make][model][category]:
            parts_data[make][model][category].append(part)
            parts_data[make][model][category].sort()
        
        inventory_manager.save_json(parts_data, inventory_manager.parts_file)
        reload_data()  # Reload the global data
        return jsonify({'success': True})
    
    # Get available vehicles for dropdown
    inventory_data = inventory_manager.load_json(inventory_manager.inventory_file)
    return render_template('crud_add_part.html', inventory=inventory_data)

@app.route('/admin/part/delete')
@admin_required
def admin_delete_part():
    """Delete part"""
    make = request.args.get('make')
    model = request.args.get('model')
    category = request.args.get('category')
    part = request.args.get('part')
    
    parts_data = inventory_manager.load_json(inventory_manager.parts_file)
    
    try:
        parts_data[make][model][category].remove(part)
        
        # Clean up empty categories/models/makes
        if not parts_data[make][model][category]:
            del parts_data[make][model][category]
        if not parts_data[make][model]:
            del parts_data[make][model]
        if not parts_data[make]:
            del parts_data[make]
        
        inventory_manager.save_json(parts_data, inventory_manager.parts_file)
        reload_data()  # Reload the global data
        flash(f'Successfully deleted part: {part}', 'success')
    except (KeyError, ValueError):
        flash(f'Part not found: {part}', 'error')
    
    return redirect(url_for('admin_parts'))

# Legacy admin endpoints for Excel management (updated with authentication)
@app.route('/admin/legacy')
@admin_required
def admin_legacy():
    """Legacy admin dashboard"""
    excel_exists = os.path.exists('inventory.xlsx')
    return render_template('admin.html', excel_exists=excel_exists)

@app.route('/admin/export-excel', methods=['POST'])
@admin_required
def admin_export_excel():
    """Export current inventory to Excel"""
    if inventory_manager.export_to_excel():
        flash('Successfully exported inventory to Excel with 5 separate sheets!', 'success')
    else:
        flash('Failed to export inventory to Excel.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/import-excel', methods=['POST'])
@admin_required
def admin_import_excel():
    """Import Excel file and update inventory"""
    if inventory_manager.import_from_excel():
        # Reload data in Flask app
        reload_data()
        flash('Successfully imported inventory from Excel!', 'success')
    else:
        flash('Failed to import inventory from Excel.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/download-excel')
@admin_required
def admin_download_excel():
    """Download the current Excel file"""
    if os.path.exists('inventory.xlsx'):
        return send_file('../inventory.xlsx', as_attachment=True)
    else:
        flash('Excel file not found. Please export first.', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/reload-data', methods=['POST'])
@admin_required
def admin_reload_data():
    """Reload data from JSON files"""
    reload_data()
    flash('Data reloaded successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/stats')
@admin_required
def admin_stats():
    """Get inventory statistics"""
    total_models = sum(len(models) for models in inventory.values())
    total_year_models = 0
    total_parts = 0
    
    # Calculate total year-model combinations
    for make, models in inventory.items():
        for model, model_data in models.items():
            years = model_data.get('years', [])
            total_year_models += len(years)
    
    # Calculate total parts
    for make, make_parts in parts_catalog.items():
        if make != 'Services':
            for model, model_parts in make_parts.items():
                for category, parts in model_parts.items():
                    total_parts += len(parts)
    
    stats = {
        'total_makes': len(inventory),
        'total_models': total_models,
        'total_year_models': total_year_models,
        'total_parts': total_parts,
        'makes': list(inventory.keys()),
        'excel_exists': os.path.exists('inventory.xlsx')
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)