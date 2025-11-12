import csv
import os
import pandas as pd  

CSV_FILE = "db_skins.csv"


def load_data(filename):
    skins = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            skins.append({
                "id": int(row['id']),
                "name": row['name'],
                "description": row['description'],
                "price": float(row['price']),
                "exterior": row['exterior'],
                "collection": row['collection']
            })
    return skins


skins = load_data(CSV_FILE)


def save_data():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "id", "name", "description", "price", "exterior", "collection"
        ])
        writer.writeheader()
        writer.writerows(skins)
    print("Data sparad!")


def list_skins():
    print("\n--- Alla Skins ---")
    if not skins:
        print("Inga skins hittades.")
        return

    
    df = pd.DataFrame(skins)
    df = df[["id", "name", "price", "exterior", "collection"]]
    df = df.sort_values("id").reset_index(drop=True)

    
    df[["weapon", "skin"]] = df["name"].str.split(" \| ", expand=True)
    df["price"] = df["price"].map(lambda x: f"{x:,.2f}")

    
    df = df[["id", "weapon", "skin", "price", "exterior", "collection"]]

   
    col_widths = {}
    for col in df.columns:
        max_len = max(df[col].astype(str).map(len).max(), len(col))
        # lite extra luft för snyggare spacing
        col_widths[col] = max_len + 2

    
    extra_space_after_price = 4

    
    header = (
        f"{'id'.ljust(col_widths['id'])}"
        f"{'weapon'.ljust(col_widths['weapon'])}"
        f"{'skin'.ljust(col_widths['skin'])}"
        f"{'price'.rjust(col_widths['price'])}{' ' * extra_space_after_price}"
        f"{'exterior'.ljust(col_widths['exterior'])}"
        f"{'collection'.ljust(col_widths['collection'])}"
    )
    print(header)
    print("-" * len(header))

    
    for _, row in df.iterrows():
        print(
            f"{str(row['id']).ljust(col_widths['id'])}"
            f"{row['weapon'].ljust(col_widths['weapon'])}"
            f"{row['skin'].ljust(col_widths['skin'])}"
            f"{row['price'].rjust(col_widths['price'])}{' ' * extra_space_after_price}"
            f"{row['exterior'].ljust(col_widths['exterior'])}"
            f"{row['collection'].ljust(col_widths['collection'])}"
        )

    print("-" * len(header))





def add_skin():
    new_id = max([s['id'] for s in skins], default=0) + 1
    print("\n--- Lägg till skin ---")
    name = input("Namn: ")
    description = input("Beskrivning: ")
    price = float(input("Pris: "))
    exterior = input("Exterior: ")
    collection = input("Collection: ")

    skins.append({
        "id": new_id,
        "name": name,
        "description": description,
        "price": price,
        "exterior": exterior,
        "collection": collection
    })

    print("Skin tillagt!")
    save_data()


def delete_skin():
    id_to_delete = int(input("Vilket id vill du ta bort?: "))
    for s in skins:
        if s["id"] == id_to_delete:
            skins.remove(s)
            print("Skin borttaget!")
            save_data()
            return
    print("Hittades inte!")


def change_skin():
    id_to_change = int(input("Vilket id vill du ändra?: "))
    for s in skins:
        if s["id"] == id_to_change:
            print(f"Ändrar {s['name']}...")

            s['name'] = input(f"Nytt namn ({s['name']}): ") or s['name']
            s['description'] = input(f"Ny beskrivning ({s['description']}): ") or s['description']

            new_price = input(f"Nytt pris ({s['price']}): ")
            if new_price:
                s['price'] = float(new_price)

            s['exterior'] = input(f"Ny exterior ({s['exterior']}): ") or s['exterior']
            s['collection'] = input(f"Ny collection ({s['collection']}): ") or s['collection']

            print("Skin ändrat!")
            save_data()
            return

    print("Hittades inte!")


while True:
    list_skins()
    print("\n MENY")
    print("1: Lägg till skin")
    print("2: Ta bort skin")
    print("3: Ändra skin")
    print("Q: Avsluta")

    val = input("Vad vill du göra?: ")

    if val == "1":
        add_skin()
    elif val == "2":
        delete_skin()
    elif val == "3":
        change_skin()
    elif val == "q" or "Q":
        print("Avslutar")
        break
    else:
        print(" Ogiltigt val!")
