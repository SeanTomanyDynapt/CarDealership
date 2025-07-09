#!/usr/bin/env python3
"""
Inventory Management System for Premium Auto Dealership
Handles Excel import/export and automatic website updates
"""

import pandas as pd
import json
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventoryManager:
    def __init__(self, excel_file='inventory.xlsx', json_dir='data'):
        self.excel_file = excel_file
        self.json_dir = json_dir
        self.inventory_file = os.path.join(json_dir, 'inventory.json')
        self.parts_file = os.path.join(json_dir, 'parts_catalog.json')
        
        # Create data directory if it doesn't exist
        os.makedirs(json_dir, exist_ok=True)
    
    def export_to_excel(self):
        """Export JSON data to Excel with 5 separate sheets"""
        try:
            logger.info("Exporting inventory data to Excel...")
            
            # Load JSON data
            inventory_data = self.load_json(self.inventory_file)
            parts_data = self.load_json(self.parts_file)
            
            # Create Excel writer
            with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
                
                # Create separate sheets for each make
                for make in ['Ford', 'Lincoln', 'Jeep']:
                    if make in inventory_data:
                        make_vehicles = []
                        for model, data in inventory_data[make].items():
                            for year in data['years']:
                                make_vehicles.append({
                                    'Make': make,
                                    'Model': model,
                                    'Year': year,
                                    'Category': data.get('category', ''),
                                    'Description': data.get('description', f'{year} {make} {model}'),
                                    'Features': ', '.join(data.get('features', [])),
                                    'Price_Range': data.get('price_range', ''),
                                    'Status': data.get('status', 'Available')
                                })
                        
                        if make_vehicles:
                            df = pd.DataFrame(make_vehicles)
                            df.to_excel(writer, sheet_name=f'{make}_Vehicles', index=False)
                
                # Create Parts sheet (combined from all makes)
                all_parts = []
                for make in ['Ford', 'Lincoln', 'Jeep']:
                    if make in parts_data:
                        for model, categories in parts_data[make].items():
                            for category, parts in categories.items():
                                for part in parts:
                                    all_parts.append({
                                        'Make': make,
                                        'Model': model,
                                        'Category': category,
                                        'Part': part,
                                        'Status': 'Available',
                                        'Price': '',
                                        'Notes': ''
                                    })
                
                if all_parts:
                    parts_df = pd.DataFrame(all_parts)
                    parts_df.to_excel(writer, sheet_name='Parts', index=False)
                
                # Create Services sheet
                services_data = [
                    {'Service_Category': 'Maintenance', 'Service_Name': 'Oil Change', 'Price': '$39.95-$69.95', 'Duration': '30 min'},
                    {'Service_Category': 'Maintenance', 'Service_Name': 'Tire Rotation', 'Price': '$29.95', 'Duration': '20 min'},
                    {'Service_Category': 'Maintenance', 'Service_Name': 'Brake Inspection', 'Price': '$49.95', 'Duration': '45 min'},
                    {'Service_Category': 'Maintenance', 'Service_Name': 'Multi-Point Inspection', 'Price': '$79.95', 'Duration': '60 min'},
                    {'Service_Category': 'Repair', 'Service_Name': 'Brake Repair', 'Price': '$199.95+', 'Duration': '2-3 hours'},
                    {'Service_Category': 'Repair', 'Service_Name': 'Engine Diagnostics', 'Price': '$129.95', 'Duration': '1 hour'},
                    {'Service_Category': 'Repair', 'Service_Name': 'Transmission Service', 'Price': '$299.95+', 'Duration': '3-4 hours'},
                    {'Service_Category': 'Tire Services', 'Service_Name': 'Tire Installation', 'Price': '$25 per tire', 'Duration': '45 min'},
                    {'Service_Category': 'Tire Services', 'Service_Name': 'Wheel Alignment', 'Price': '$99.95', 'Duration': '1 hour'},
                    {'Service_Category': 'Specialty', 'Service_Name': 'State Inspection', 'Price': '$25.00', 'Duration': '30 min'},
                    {'Service_Category': 'Specialty', 'Service_Name': 'Emissions Testing', 'Price': '$35.00', 'Duration': '20 min'},
                    {'Service_Category': 'Detailing', 'Service_Name': 'Basic Wash', 'Price': '$29.95', 'Duration': '30 min'},
                    {'Service_Category': 'Detailing', 'Service_Name': 'Full Detail', 'Price': '$149.95', 'Duration': '3 hours'}
                ]
                
                services_df = pd.DataFrame(services_data)
                services_df.to_excel(writer, sheet_name='Services', index=False)
            
            logger.info(f"Successfully exported inventory to {self.excel_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            return False
    
    def import_from_excel(self):
        """Import data from Excel with 5 separate sheets"""
        try:
            logger.info("Importing inventory data from Excel...")
            
            # Create backup
            self.create_backup()
            
            excel_file = pd.ExcelFile(self.excel_file)
            
            # Initialize data structures
            inventory = {}
            parts_catalog = {}
            
            # Process vehicle sheets
            for make in ['Ford', 'Lincoln', 'Jeep']:
                sheet_name = f'{make}_Vehicles'
                if sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
                    
                    if make not in inventory:
                        inventory[make] = {}
                    
                    for _, row in df.iterrows():
                        model = str(row['Model']).strip()
                        year = int(row['Year'])
                        
                        if model not in inventory[make]:
                            inventory[make][model] = {
                                'years': [],
                                'category': str(row.get('Category', '')).strip(),
                                'description': str(row.get('Description', f'{make} {model}')).strip(),
                                'features': [],
                                'price_range': str(row.get('Price_Range', '')).strip(),
                                'status': str(row.get('Status', 'Available')).strip()
                            }
                        
                        if year not in inventory[make][model]['years']:
                            inventory[make][model]['years'].append(year)
                        
                        # Handle features
                        features = str(row.get('Features', ''))
                        if features and features != 'nan':
                            feature_list = [f.strip() for f in features.split(',') if f.strip()]
                            inventory[make][model]['features'] = list(set(inventory[make][model]['features'] + feature_list))
                    
                    # Sort years for each model
                    for model in inventory[make]:
                        inventory[make][model]['years'].sort()
            
            # Process Parts sheet
            if 'Parts' in excel_file.sheet_names:
                parts_df = pd.read_excel(self.excel_file, sheet_name='Parts')
                
                for _, row in parts_df.iterrows():
                    make = str(row['Make']).strip()
                    model = str(row['Model']).strip()
                    category = str(row['Category']).strip()
                    part = str(row['Part']).strip()
                    
                    if make not in parts_catalog:
                        parts_catalog[make] = {}
                    if model not in parts_catalog[make]:
                        parts_catalog[make][model] = {}
                    if category not in parts_catalog[make][model]:
                        parts_catalog[make][model][category] = []
                    
                    if part not in parts_catalog[make][model][category]:
                        parts_catalog[make][model][category].append(part)
            
            # Save to JSON files
            self.save_json(inventory, self.inventory_file)
            self.save_json(parts_catalog, self.parts_file)
            
            logger.info("Successfully updated inventory.json")
            logger.info("Successfully updated parts_catalog.json")
            
            return True
            
        except Exception as e:
            logger.error(f"Error importing from Excel: {e}")
            return False
    
    def load_json(self, file_path):
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"File {file_path} not found, returning empty dict")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {file_path}")
            return {}
    
    def save_json(self, data, file_path):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_backup(self):
        """Create backup of current JSON files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if os.path.exists(self.inventory_file):
            backup_file = f'backup_inventory_{timestamp}.json'
            with open(self.inventory_file, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
            logger.info(f"Created backup: {backup_file}")

class ExcelFileHandler:
    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager
        self.last_modified = 0
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path.endswith('.xlsx') and 'inventory' in event.src_path.lower():
            # Prevent multiple rapid fire updates
            current_time = time.time()
            if current_time - self.last_modified < 2:  # 2 second cooldown
                return
            
            self.last_modified = current_time
            logger.info(f"Excel file modified: {event.src_path}")
            
            # Wait a moment for file to be fully written
            time.sleep(1)
            
            if self.inventory_manager.import_from_excel():
                logger.info("Website data updated successfully!")
            else:
                logger.error("Failed to update website data")

def start_file_monitor(inventory_manager):
    """Start monitoring Excel file for changes"""
    event_handler = ExcelFileHandler(inventory_manager)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    logger.info("Started file monitoring. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("File monitoring stopped.")
    
    observer.join()

def main():
    import argparse
    import time
    from watchdog.observers import Observer
    
    parser = argparse.ArgumentParser(description='Premium Auto Dealership Inventory Manager')
    parser.add_argument('--export', action='store_true', help='Export JSON to Excel')
    parser.add_argument('--import', action='store_true', help='Import Excel to JSON')
    parser.add_argument('--monitor', action='store_true', help='Monitor Excel file for changes')
    parser.add_argument('--excel-file', default='inventory.xlsx', help='Excel file name')
    
    args = parser.parse_args()
    
    manager = InventoryManager(excel_file=args.excel_file)
    
    if args.export:
        if manager.export_to_excel():
            print(f"✅ Successfully exported to {args.excel_file}")
        else:
            print("❌ Export failed")
    
    elif getattr(args, 'import'):
        if manager.import_from_excel():
            print("✅ Successfully imported from Excel")
        else:
            print("❌ Import failed")
    
    elif args.monitor:
        # Create Excel file if it doesn't exist
        # manager.create_sample_excel() # This line is removed as per the new_code
        start_file_monitor(manager)
    
    else:
        print("Please specify an action: --export, --import, or --monitor")
        print("Example: python inventory_manager.py --export")

if __name__ == "__main__":
    main() 