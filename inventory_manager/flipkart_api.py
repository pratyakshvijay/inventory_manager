# inventory_manager/utils/flipkart_api.py

import requests
import base64
import json
from django.conf import settings

def get_flipkart_token():
    url = "https://seller.api.flipkart.net/oauth-service/oauth/token"
    querystring = {"grant_type": "client_credentials", "scope": "Seller_Api"}
    client_id = settings.FLIPKART_CLIENT_ID
    client_secret = settings.FLIPKART_CLIENT_SECRET

    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Flipkart Auth Error: {response.status_code} - {response.text}")


def sync_inventory_to_flipkart(sku, token):
    from inventory_manager.models import ChannelListing  # avoid circular import

    listings = ChannelListing.objects.filter(master_sku=sku)
    if not listings:
        return

    location_id = "LOC83ea38515d3e482bac3be6b2d389e30d"

    payload = {}

    for listing in listings:
        if listing.fsn:
            payload[listing.channel_sku] = {
                "product_id": listing.fsn,
                "locations": [
                    {
                        "id": location_id,
                        "inventory": sku.stock_quantity
                    }
                ]
            }

    url = "https://api.flipkart.net/sellers/listings/v3/update/inventory"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.ok:
        print(f"✅ Inventory synced for SKU: {sku.sku_code}")
        return True
    else:
        print(f"❌ Failed to sync {sku.sku_code}: {response.status_code} - {response.text}")
        return False
