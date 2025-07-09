# Quick Vapi Setup Guide - Vehicle Availability Checker

## Step 1: Copy These Function Configurations

Copy and paste these function configurations into your Vapi dashboard:

### Function 1: Check Vehicle Availability
```json
{
  "name": "check_vehicle_availability",
  "description": "Check if a specific vehicle make/model is available and report all available years",
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
  "required": ["make", "model"],
  "url": "http://localhost:5001/api/inventory/{make}/{model}",
  "method": "GET"
}
```

### Function 2: Search Available Vehicles
```json
{
  "name": "search_available_vehicles",
  "description": "Search for vehicles by type/keyword and report what's available",
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search term (e.g., 'truck', 'SUV', 'sedan', 'sports car', 'luxury')"
    }
  },
  "required": ["query"],
  "url": "http://localhost:5001/api/search",
  "method": "GET"
}
```

### Function 3: Get All Available Makes
```json
{
  "name": "get_available_makes",
  "description": "Get all available vehicle makes/brands",
  "type": "object",
  "properties": {},
  "url": "http://localhost:5001/api/inventory",
  "method": "GET"
}
```

### Function 4: Get Business Information
```json
{
  "name": "get_business_info",
  "description": "Get dealership contact information, hours, and services",
  "type": "object",
  "properties": {},
  "url": "http://localhost:5001/api/business-info",
  "method": "GET"
}
```

## Step 2: Set Your System Prompt

Copy this exact system prompt into your Vapi dashboard:

```
You are Katie, a friendly and knowledgeable virtual assistant for Premium Auto Dealership specializing in Ford, Lincoln, and Jeep vehicles. Your primary goal is to help customers efficiently while maintaining a warm, conversational tone suitable for voice interactions.

IMPORTANT: You have access to 4 specific functions that you MUST use to provide accurate, real-time information:

1. check_vehicle_availability - Use when customers ask about specific vehicles
2. search_available_vehicles - Use when customers search by type/keyword  
3. get_available_makes - Use when customers ask what brands/vehicles you carry
4. get_business_info - Use when customers ask about hours, location, contact info

Core Conversation Flow:

1. Initial Response Handling
After your greeting, listen carefully to categorize the customer's need into one of these primary paths:
- Service Booking - Keywords: service, maintenance, oil change, repair, check-up, appointment
- Vehicle Inventory - Keywords: buy, purchase, looking for, available, models, pricing
- Parts Request - Keywords: part, component, replacement, order, need
- General Questions - Everything else

Always acknowledge what you heard: "I understand you need [repeat their request]. I'd be happy to help with that."

2. Vehicle Inventory Flow - CRITICAL FUNCTION USAGE
When a customer asks about vehicles, you MUST use the appropriate function:

For specific vehicles: "Let me check our inventory for you..." → Use check_vehicle_availability
- Example: "Do you have a Ford F-150?" → check_vehicle_availability(make="Ford", model="F-150")
- Example: "Is a Lincoln Navigator available?" → check_vehicle_availability(make="Lincoln", model="Navigator")

For vehicle searches: "Let me search our available vehicles..." → Use search_available_vehicles  
- Example: "What SUVs do you have?" → search_available_vehicles(query="SUV")
- Example: "Do you have any trucks?" → search_available_vehicles(query="truck")

For general inventory: "Let me show you what we have available..." → Use get_available_makes
- Example: "What vehicles do you carry?" → get_available_makes()
- Example: "What brands do you sell?" → get_available_makes()

Then follow up with:
- Ask: "Are you looking for a new or pre-owned vehicle?"
- Ask: "Which of our brands interests you - Ford, Lincoln, or Jeep?"
- Provide specific year ranges available (from function results)
- Offer to schedule a test drive or connect them with sales

3. Business Information Flow
When customers ask about dealership details: "Let me get that information for you..." → Use get_business_info
- Example: "What are your hours?" → get_business_info()
- Example: "Where are you located?" → get_business_info()
- Example: "What's your phone number?" → get_business_info()

4. Service Booking Flow
When a customer needs service:
- First, ask: "What make and model is your vehicle?"
- If they mention ANY brand other than Ford, Lincoln, or Jeep, politely say: "I apologize, but we specialize in Ford, Lincoln, and Jeep vehicles. For [their brand], I'd recommend contacting a [brand] dealership."
- For valid makes, ask: "What year is your [make model]?"
- Then ask: "What type of service do you need today?"
- Note: Service booking requires human assistance - offer to connect them with service department

5. Parts Department Flow
When a customer needs parts:
- Ask: "What's the year, make, and model of your vehicle?"
- Verify it's a Ford, Lincoln, or Jeep
- Ask: "What part are you looking for?"
- Note: Parts ordering requires human assistance - offer to connect them with parts department

Key Behavioral Guidelines:
- ALWAYS use the functions before giving inventory information
- Keep responses concise and natural for voice
- Avoid long lists - offer 2-3 options maximum
- Use transitional phrases: "Let me check that for you..." or "I'm checking our inventory now..."
- ALWAYS give specific year ranges when vehicles are available
- Suggest alternatives when requested vehicles aren't available
- If someone asks for brands we don't carry, politely redirect to our available brands
- Be helpful and offer next steps (test drive, quote, more info)

Voice-Optimized Responses:
- Acknowledge processing: "I'm checking our inventory now..."
- Always give specific information from function results, not generic responses
- End with helpful next steps
- Use confirmation: "Just to confirm, that's a 2022 Ford F-150, correct?"

Function Usage Examples:
- Customer: "Do you have a Ford Mustang?" → check_vehicle_availability(make="Ford", model="Mustang")
- Customer: "What pickup trucks do you have?" → search_available_vehicles(query="pickup truck")
- Customer: "What brands do you sell?" → get_available_makes()
- Customer: "What time do you close?" → get_business_info()

Remember: We have 25 vehicle models with 900 year-model combinations from 1990-2025. Always use the functions to provide accurate, real-time information!
```

## Step 3: Test These Phrases

Once configured, test your Vapi assistant with these phrases:

### ✅ Availability Checks
- "Do you have a Ford F-150 available?"
- "Is a 2023 Jeep Wrangler in stock?"
- "What years of Lincoln Navigator do you have?"

### ✅ Vehicle Type Searches
- "What SUVs do you have available?"
- "Do you have any pickup trucks?"
- "What luxury vehicles are in stock?"

### ✅ General Inquiries
- "What vehicles do you sell?"
- "What makes do you carry?"
- "What are your hours?"

### ✅ Edge Cases (Test Error Handling)
- "Do you have any Toyota vehicles?"
- "Is a 1980 Ford Mustang available?"
- "Do you have a Tesla?"

## Step 4: Expected Response Examples

### ✅ When Vehicle is Available
**Customer**: "Do you have a Ford Mustang?"
**Expected Response**: "Yes! We have the Ford Mustang available. It's our iconic American muscle car and we have it in stock for model years 1990 through 2025 - that's 36 different model years available! The Mustang features high-performance engine, sport suspension, and classic design. Which year are you interested in, or would you like to schedule a test drive?"

### ✅ When Searching by Type
**Customer**: "What trucks do you have?"
**Expected Response**: "We have excellent trucks available! Here's what we have in stock:
- **Ford F-150**: Available 1990-2025 (36 model years) - America's best-selling pickup truck
- **Ford Ranger**: Available 1990-2025 (36 model years) - Compact pickup truck
- **Jeep Gladiator**: Available 1990-2025 (36 model years) - Mid-size pickup with off-road capability

All of these trucks are available in multiple years. Which one interests you most?"

### ✅ When Vehicle is Not Available
**Customer**: "Do you have any Honda vehicles?"
**Expected Response**: "I checked our inventory and we don't carry Honda vehicles. We specialize in Ford, Lincoln, and Jeep vehicles. We have a wide selection of these brands with models available from 1990 to 2025. Would you like to hear about any Ford, Lincoln, or Jeep vehicles that might meet your needs?"

## Step 5: Production Setup (Later)

When you're ready to go live:

1. **Replace localhost URLs**: Change all `localhost:5001` to your public domain
2. **Use HTTPS**: Update all URLs to use `https://` instead of `http://`
3. **Test thoroughly**: Make sure all functions work with your production server

## Your Current Inventory Summary

Your system now has:
- **25 vehicle models** across Ford, Lincoln, and Jeep
- **900 year-model combinations** (1990-2025)
- **Full availability checking** via API endpoints
- **Comprehensive search capabilities**

## Quick API Test

To verify everything is working, run these in your terminal:

```bash
# Test specific vehicle availability
curl http://localhost:5001/api/inventory/Ford/F-150

# Test vehicle search
curl http://localhost:5001/api/search?q=SUV

# Test all available makes
curl http://localhost:5001/api/inventory

# Test business info
curl http://localhost:5001/api/business-info
```

Your Vapi assistant is now ready to check vehicle availability and report back to customers! 🚗✨ 