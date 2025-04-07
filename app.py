import requests

RAPIDAPI_KEY = "717efc6d4cmsh0b0eac96e27f6e8p170b9ajsnb5ed8a08c301"

def get_property_comps(address, citystatezip):
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    querystring = {"location": f"{address}, {citystatezip}"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        comps = []

        for result in data.get("props", []):
            if result.get("statusType") == "RECENTLY_SOLD":
                comps.append({
                    "address": result.get("address", "N/A"),
                    "price": result.get("price", 0)
                })

        return comps
    else:
        print(f"API Error: {response.status_code} - {response.text}")
        return []

def calculate_arv(comps):
    prices = [comp["price"] for comp in comps if comp["price"] > 0]
    return sum(prices) / len(prices) if prices else 0

def calculate_mao(arv, repair_costs=0):
    return (arv * 0.6) - repair_costs

def run_real_comps(address, citystatezip, repair_costs=0):
    comps = get_property_comps(address, citystatezip)

    if not comps:
        print("❌ No comps found.")
        return

    arv = calculate_arv(comps)
    mao = calculate_mao(arv, repair_costs)

    print("\n✅ Nearby Sold Comps:")
    for comp in comps:
        print(f"- {comp['address']}: ${comp['price']:,}")

    print(f"\n💰 ARV: ${arv:,.2f}")
    print(f"🏷️ MAO (60% Rule): ${mao:,.2f}")

# Example usage
if __name__ == "__main__":
    address = input("Enter property address (e.g., 123 Main St): ")
    citystatezip = input("Enter city/state/zip (e.g., Saint Petersburg, FL): ")
    repair_costs = float(input("Enter estimated repair costs (optional): ") or 0)
    run_real_comps(address, citystatezip, repair_costs)
