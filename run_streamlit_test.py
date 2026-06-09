import streamlit as st
import pandas as pd
import json

st.write("Magic: The Gathering card browser — powered by Scryfall bulk data.")

@st.cache_data
def load_data():
    with open('default-cards.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)

    data = []
    for card in cards:
        image_uris = card.get('image_uris', {})
        prices = card.get('prices', {})
        data.append({
            "Preview": image_uris.get('small', ''),
            "Name": card.get('name', ''),
            "Mana Cost": card.get('mana_cost', ''),
            "Type": card.get('type_line', ''),
            "Rarity": card.get('rarity', '').capitalize(),
            "Set": card.get('set_name', ''),
            "USD": float(prices.get('usd') or 0),
        })

    return pd.DataFrame(data)

data = load_data()


config = {
    "Preview": st.column_config.ImageColumn(),
    "USD": st.column_config.NumberColumn(format="$%.2f"),
}
title = st.text_input("Set Name", "The Lord of the Rings: Tales of Middle-earth")
st.write("The current set name is", title)
data = data[data["Set"].str.fullmatch(title, case=False, na=False)]

if st.toggle("Enable editing"):
    edited_data = st.data_editor(data.head(len(data)), column_config=config, use_container_width=True)
else:
    st.dataframe(data.head(len(data)), column_config=config, use_container_width=True)
