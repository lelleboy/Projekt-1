import csv
import os

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
    for skin in skins:
        print(f"{skin['id']}: {skin['name']} | {skin['price']} | {skin['exterior']}")
    print("------------------\n")


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
    print("\n MENY")
    print("1: Lista skins")
    print("2: Lägg till skin")
    print("3: Ta bort skin")
    print("4: Ändra skin")
    print("5: Avsluta")

    val = input("Vad vill du göra?: ")

    if val == "1":
        list_skins()
    elif val == "2":
        add_skin()
    elif val == "3":
        delete_skin()
    elif val == "4":
        change_skin()
    elif val == "5":
        print("Avslutar")
        break
    else:
        print(" Ogiltigt val!")
