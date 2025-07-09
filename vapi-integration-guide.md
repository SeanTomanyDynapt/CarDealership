# Vapi Integration Guide for Premium Auto Dealership

## Overview
This guide shows how to integrate your car dealership website with Vapi to create a voice assistant that can check vehicle availability and report back to customers what's in stock.

## API Endpoints Available

Your Flask app provides these API endpoints for Vapi integration:

### Vehicle Inventory
- `GET /api/inventory` - Get all vehicle inventory
- `GET /api/inventory/<make>` - Get vehicles for a specific make (Ford, Lincoln, Jeep)
- `GET /api/inventory/<make>/<model>` - Get details for specific vehicle
- `GET /api/search?q=<query>` - Search vehicles by keyword

### Parts Catalog
- `GET /api/parts` - Get all parts catalog
- `GET /api/parts/<make>` - Get parts for a specific make
- `GET /api/parts/<make>/<model>` - Get parts for specific vehicle

### Business Information
- `GET /api/business-info` - Get dealership contact info, hours, services

## Vapi Function Configuration for Availability Checking

### 1. Check Vehicle Availability Function

```json
{
  "name": "check_vehicle_availability",
  "description": "Check if a specific vehicle make/model is available and report all available years",
  "parameters": {
    "type": "object",
    "properties": {
      "make": {
        "type": "string",
        "description": "Vehicle make (Ford, Lincoln, Jeep)",
        "enum": ["Ford", "Lincoln", "Jeep"]
      },
      "model": {
        "type": "string",
        "description": "Vehicle model (e.g., F-150, Mustang, Wrangler, Navigator)"
      }
    },
    "required": ["make", "model"]
  },
  "url": "http://localhost:5001/api/inventory/{make}/{model}",
  "method": "GET"
}
```

### 2. Search Available Vehicles Function

```json
{
  "name": "search_available_vehicles",
  "description": "Search for vehicles by type/keyword and report what's available",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search term (e.g., 'truck', 'SUV', 'sedan', 'sports car', 'luxury')"
      }
    },
    "required": ["query"]
  },
  "url": "http://localhost:5001/api/search",
  "method": "GET"
}
```

### 3. Check Year-Specific Availability Function

```json
{
  "name": "check_year_availability",
  "description": "Check if a specific year of a vehicle is available",
  "parameters": {
    "type": "object",
    "properties": {
      "make": {
        "type": "string",
        "description": "Vehicle make (Ford, Lincoln, Jeep)"
      },
      "model": {
        "type": "string",
        "description": "Vehicle model"
      },
      "year": {
        "type": "integer",
        "description": "Specific year to check (1990-2025)"
      }
    },
    "required": ["make", "model", "year"]
  },
  "url": "http://localhost:5001/api/inventory/{make}/{model}",
  "method": "GET"
}
```

### 4. Get All Available Makes Function

```json
{
  "name": "get_available_makes",
  "description": "Get all available vehicle makes/brands",
  "parameters": {
    "type": "object",
    "properties": {}
  },
  "url": "http://localhost:5001/api/inventory",
  "method": "GET"
}
```

### 5. Get Business Information Function

```json
{
  "name": "get_business_info",
  "description": "Get dealership contact information, hours, and services",
  "parameters": {
    "type": "object",
    "properties": {}
  },
  "url": "http://localhost:5001/api/business-info",
  "method": "GET"
}
```

## Complete Vapi Assistant Configuration

```json
{
  "name": "Premium Auto Dealership Assistant",
  "voice": "jennifer",
  "model": "gpt-4",
  "functions": [
    {
      "name": "check_vehicle_availability",
      "description": "Check if a specific vehicle make/model is available and report all available years",
      "parameters": {
        "type": "object",
        "properties": {
          "make": {
            "type": "string",
            "description": "Vehicle make (Ford, Lincoln, Jeep)",
            "enum": ["Ford", "Lincoln", "Jeep"]
          },
          "model": {
            "type": "string",
            "description": "Vehicle model (e.g., F-150, Mustang, Wrangler, Navigator)"
          }
        },
        "required": ["make", "model"]
      },
      "url": "http://localhost:5001/api/inventory/{make}/{model}",
      "method": "GET"
    },
    {
      "name": "search_available_vehicles",
      "description": "Search for vehicles by type/keyword and report what's available",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Search term (e.g., 'truck', 'SUV', 'sedan', 'sports car', 'luxury')"
          }
        },
        "required": ["query"]
      },
      "url": "http://localhost:5001/api/search",
      "method": "GET"
    },
    {
      "name": "get_available_makes",
      "description": "Get all available vehicle makes/brands",
      "parameters": {
        "type": "object",
        "properties": {}
      },
      "url": "http://localhost:5001/api/inventory",
      "method": "GET"
    },
    {
      "name": "get_business_info",
      "description": "Get dealership contact information, hours, and services",
      "parameters": {
        "type": "object",
        "properties": {}
      },
      "url": "http://localhost:5001/api/business-info",
      "method": "GET"
    }
  ],
  "systemPrompt": "You are a helpful assistant for Premium Auto Dealership. Your primary job is to check vehicle availability and report back to customers what vehicles are in stock. When customers ask about specific vehicles, always use the functions to check our current inventory and give them specific information about what years are available. We sell Ford, Lincoln, and Jeep vehicles with models available from 1990 to 2025. Always be specific about availability and offer to help schedule test drives or get quotes for available vehicles."
}
```

## Example Customer Interactions & Responses

### 1. Specific Vehicle Availability Check
**Customer**: "Do you have a Ford F-150 available?"
**Assistant**: *calls check_vehicle_availability with make="Ford", model="F-150"*
**Response**: "Yes! We have the Ford F-150 available. It's America's best-selling pickup truck and we have it in stock for model years 1990 through 2025 - that's 36 different model years available! The F-150 features powerful engine options, spacious bed, and advanced towing capacity. Which year are you interested in, or would you like to schedule a test drive?"

### 2. Year-Specific Availability
**Customer**: "Do you have a 2023 Jeep Wrangler?"
**Assistant**: *calls check_vehicle_availability with make="Jeep", model="Wrangler"*
**Response**: "Yes, we do have a 2023 Jeep Wrangler available! The Wrangler is available in model years from 1990 to 2025, so 2023 is definitely in stock. The Wrangler is perfect for off-road adventures and everyday driving. Would you like to schedule a test drive or get a quote for the 2023 model?"

### 3. Vehicle Type Search
**Customer**: "What SUVs do you have available?"
**Assistant**: *calls search_available_vehicles with query="SUV"*
**Response**: "We have several SUVs available! Here's what we have in stock:
- **Ford Explorer**: Available 1991-2025 (35 model years) - Popular midsize SUV with 7-passenger seating
- **Ford Escape**: Available 2001-2025 (25 model years) - Compact SUV, fuel efficient
- **Lincoln Navigator**: Available 1990-2025 (36 model years) - Luxury full-size SUV
- **Jeep Cherokee**: Available 1990-2025 (36 model years) - Versatile midsize SUV
- **Jeep Grand Cherokee**: Available 1990-2025 (36 model years) - Premium SUV with great capability

Which of these SUVs interests you most?"

### 4. Unavailable Vehicle
**Customer**: "Do you have any Toyota vehicles?"
**Assistant**: *calls get_available_makes*
**Response**: "I checked our inventory and we don't carry Toyota vehicles. We specialize in Ford, Lincoln, and Jeep vehicles. We have a wide selection of these brands with models available from 1990 to 2025. Would you like to hear about any Ford, Lincoln, or Jeep vehicles that might meet your needs?"

### 5. General Availability Check
**Customer**: "What vehicles do you have available?"
**Assistant**: *calls get_available_makes*
**Response**: "We have a great selection of vehicles available! Here's what we carry:

**Ford** (9 models): F-150, Mustang, Explorer, Escape, Fusion, Bronco, Ranger, Edge, Fiesta
**Lincoln** (8 models): Navigator, MKZ, Aviator, Continental, Corsair, Nautilus, and more
**Jeep** (8 models): Wrangler, Cherokee, Grand Cherokee, Renegade, Compass, Gladiator, Patriot, and more

All models are available in multiple years from 1990 to 2025. What type of vehicle are you looking for - truck, SUV, sedan, or sports car?"

## Advanced Response Strategies

### When Vehicle is Available
- Always mention specific year range available
- Highlight key features
- Offer next steps (test drive, quote, more info)
- Ask follow-up questions about preferences

### When Vehicle is Not Available
- Clearly state what's not available
- Suggest similar alternatives from inventory
- Explain what brands/models ARE available
- Offer to help find alternatives

### For Partial Matches
- If model name is close, suggest correct names
- If year is out of range, mention available years
- Always be helpful and offer alternatives

## Testing Your Integration

1. **Test API Endpoints**: 
```bash
curl http://localhost:5001/api/inventory/Ford/F-150
curl http://localhost:5001/api/search?q=SUV
curl http://localhost:5001/api/inventory
```

2. **Test Vapi Functions**: Configure the functions in your Vapi dashboard and test with:
   - "Do you have a Ford Mustang?"
   - "What SUVs are available?"
   - "Is a 2020 Lincoln Navigator in stock?"
   - "What vehicles do you sell?"

3. **Test Edge Cases**:
   - Ask for unavailable brands (Toyota, Honda)
   - Ask for years outside range (1980, 2030)
   - Ask for non-existent models

## Production Setup

1. **Replace localhost**: Update all URLs to your production domain
2. **Use HTTPS**: Ensure all API calls use HTTPS in production
3. **Add Authentication**: Consider API keys for production
4. **Monitor Usage**: Track API calls and response times
5. **Error Handling**: Ensure graceful handling of API errors

Your inventory now contains **25 vehicle models** with **900 year-model combinations** total, giving customers plenty of options to choose from! 