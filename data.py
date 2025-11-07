import csv

skins = [
    {
        "id": 1,
        "name": "AK-47 | Redline",
        "description": "A fan-favorite AK-47 skin with a sleek red and black design.",
        "price": 19.99,
        "exterior": "Field-Tested",
        "collection": "The Phoenix Collection"
    },
    {
        "id": 2,
        "name": "AWP | Asiimov",
        "description": "A bold futuristic white and orange AWP design.",
        "price": 149.99,
        "exterior": "Battle-Scarred",
        "collection": "The Winter Offensive Collection"
    },
    {
        "id": 3,
        "name": "M4A4 | Howl",
        "description": "Infamous and rare red wolf design, classified contraband.",
        "price": 4500.00,
        "exterior": "Minimal Wear",
        "collection": "Contraband"
    },
    {
        "id": 4,
        "name": "Glock-18 | Fade",
        "description": "A smooth gradient fade finish, extremely sought after.",
        "price": 799.99,
        "exterior": "Factory New",
        "collection": "The Assault Collection"
    },
    {
        "id": 5,
        "name": "Desert Eagle | Blaze",
        "description": "Legendary skin with fiery artwork on the slide.",
        "price": 899.99,
        "exterior": "Factory New",
        "collection": "The Dust Collection"
    },
    {
        "id": 6,
        "name": "USP-S | Kill Confirmed",
        "description": "Skull and bullet graphic design – popular covert USP.",
        "price": 125.50,
        "exterior": "Field-Tested",
        "collection": "The Shadow Collection"
    },
    {
        "id": 7,
        "name": "Karambit | Doppler",
        "description": "Popular Doppler knife with mesmerizing gemstone-like finish.",
        "price": 1500.00,
        "exterior": "Factory New",
        "collection": "Knife Case"
    },
    {
        "id": 8,
        "name": "AK-47 | Vulcan",
        "description": "Aggressive black, white, and blue military style.",
        "price": 220.00,
        "exterior": "Field-Tested",
        "collection": "The Huntsman Collection"
    },
    {
        "id": 9,
        "name": "AWP | Dragon Lore",
        "description": "Iconic sniper skin with medieval dragon artwork.",
        "price": 9500.00,
        "exterior": "Factory New",
        "collection": "The Cobblestone Collection"
    },
    {
        "id": 10,
        "name": "P90 | Emerald Dragon",
        "description": "Green dragon artwork wrapped around the weapon.",
        "price": 79.99,
        "exterior": "Minimal Wear",
        "collection": "The Operation Bravo Collection"
    }
]

# CSV file path
csv_file_path = "db_skins.csv"

# Write the skins data to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "description", "price", "exterior", "collection"])
    writer.writeheader()
    writer.writerows(skins)

print(f"✅ Data successfully saved to {csv_file_path}")
