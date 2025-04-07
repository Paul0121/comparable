import streamlit as st
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
        st.error(f"API Error: {response.status_code} - {response.text}")
        return []

def calculate_arv(comps):
    prices = [comp["price"] for comp in comps if comp["price"] > 0]
    return sum(prices) / len(prices) if prices else 0

def calculate_mao(arv, repair_costs=0):
    return (arv * 0.6) - repair_costs

# Streamlit UI
st.title("🏘️ Real Estate Comps & MAO Calculator")

with st.form("comp_form"):
    address = st.text_input("Property Address (e.g. 123 Main St)")
    citystatezip = st.text_input("City/State/Zip (e.g. Saint Petersburg, FL)")
    repair_costs = st.number_input("Estimated Repair Costs", min_value=0, value=0, step=1000)
    submitted = st.form_submit_button("Run Comps")

if submitted:
    if address and citystatezip:
        with st.spinner("Fetching comps..."):
            comps = get_property_comps(address, citystatezip)
        
        if comps:
            st.subheader("📍 Comparable Sold Properties")
            for comp in comps:
                st.write(f"- {comp['address']}: ${comp['price']:,}")

            arv = calculate_arv(comps)
            mao = calculate_mao(arv, repair_costs)

            st.markdown(f"### 💰 Estimated ARV: `${arv:,.2f}`")
            st.markdown(f"### 🏷️ Maximum Allowable Offer (60% Rule): `${mao:,.2f}`")
        else:
            st.warning("No sold comps found. Try a nearby ZIP or full city name.")
    else:
        st.error("Please enter both the address and city/state/zip.")
