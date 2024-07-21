# process_data.py
import pywhatkit


def process_selected_items(items, image_path):
    # Your processing logic here
    for name, contact in items:
        print(f"Processing item: {name}")
        pywhatkit.sendwhats_image(contact, image_path, tab_close=True)
