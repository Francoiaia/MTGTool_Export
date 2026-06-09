import requests
from tqdm import tqdm
import streamlit as st

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'fiaia2070@gmail.com'  # This is another valid field
}
x = requests.get('https://api.scryfall.com/bulk-data/default-cards',headers=headers)
json_value = x.json()
uri_to_download = json_value["download_uri"]

response = requests.get(uri_to_download, headers=headers, stream=True)
total = int(response.headers.get('content-length', 0))

with open('default-cards.json', 'wb') as f, tqdm(
    total=total,
    unit='B',
    unit_scale=True,
    unit_divisor=1024,
    desc='Downloading'
) as bar:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
        bar.update(len(chunk))
