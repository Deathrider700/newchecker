# config.py - Configuration settings for the bot
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file if it exists

# --- Bot Token ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# --- Admin User IDs ---
ADMIN_IDS_str = os.environ.get('ADMIN_IDS', '').split(',') # Get comma-separated string from env, split to list
ADMIN_IDS = [int(id) for id in ADMIN_IDS_str if id] # Convert non-empty IDs to integers

# --- Proxy for Shopify Charge Gate (Optional) ---
PROXY_FOR_SHOPIFY_CHARGE = os.environ.get('PROXY_FOR_SHOPIFY_CHARGE')

# --- Other Configuration Variables (Add more as needed) ---
# Example: API_KEY_STRIPE = os.environ.get('API_KEY_STRIPE')

# --- Validation ---
if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable is not set in config.py or .env file.")
    # Consider raising an exception or exiting if BOT_TOKEN is essential
    # raise ValueError("BOT_TOKEN is not set") # Example of raising an error

if not ADMIN_IDS:
    print("Warning: ADMIN_IDS environment variable is not set or is empty. No users will have admin privileges.")


# --- Example usage (for testing - can be removed later) ---
if __name__ == '__main__':
    print("--- Config Settings ---")
    print(f"BOT_TOKEN: {'Set' if BOT_TOKEN else 'Not Set'}") # Mask sensitive info in real logging
    print(f"ADMIN_IDS: {ADMIN_IDS}")
    print(f"PROXY_FOR_SHOPIFY_CHARGE: {'Set' if PROXY_FOR_SHOPIFY_CHARGE else 'Not Set'}")
    # Example for other configs: print(f"API_KEY_STRIPE: {'Set' if API_KEY_STRIPE else 'Not Set'}")
    print("--- End Config Settings ---")