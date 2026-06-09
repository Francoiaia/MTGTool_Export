import streamlit as st
import pandas as pd
import json

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

config = {
    "Preview": st.column_config.ImageColumn(),
    "USD": st.column_config.NumberColumn(format="$%.2f"),
}

all_data = load_data()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "type": "text", "content": "Welcome! Type a **set name** to browse MTG cards 🃏"}]

# Render history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["type"] == "table":
            st.dataframe(message["data"], column_config=config, use_container_width=True)

# Chat input
if prompt := st.chat_input("Type a set name, e.g. 'Rivals of Ixalan'"):
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        filtered = all_data[all_data["Set"].str.contains(prompt, case=False, na=False)]

        if filtered.empty:
            response_text = f"No cards found for **{prompt}**. Try a different name!"
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": response_text})
        else:
            response_text = f"Found **{len(filtered)}** cards in **{prompt}** 🃏"
            st.markdown(response_text)
            st.dataframe(filtered, column_config=config, use_container_width=True)
            st.session_state.messages.append({
                "role": "assistant",
                "type": "table",
                "content": response_text,
                "data": filtered,
            })
