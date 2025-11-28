import csv
import curses

CSV_FILE = "db_skins.csv"

def load_data(filename):
    skins = []
    try:
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
    except FileNotFoundError:
        pass
    return skins

def save_data(skins):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "id", "name", "description", "price", "exterior", "collection"
        ])
        writer.writeheader()
        writer.writerows(skins)

def get_input(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    value = stdscr.getstr(1, 0, 2000).decode("utf-8")
    curses.noecho()
    return value

def show_menu(stdscr, skins):
    curses.curs_set(0)
    current = 0
    
    menu_options = []
    for skin in skins:
        menu_options.append(skin)
    menu_options.append({"name": "→ Lägg till skin"})
    menu_options.append({"name": "→ Ta bort skin"})
    menu_options.append({"name": "→ Ändra skin"})
    menu_options.append({"name": "→ Avsluta"})
    
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # Header
        header = "ID   | Weapon               | Skin                      | Price"
        stdscr.addstr(1, 2, header, curses.A_BOLD)
        stdscr.addstr(2, 2, "-" * len(header))
        
        # Lista items
        for i, item in enumerate(menu_options):
            y = 4 + i
            if y >= h - 3:
                break
                
            if "price" in item:
                if " | " in item["name"]:
                    weapon, skin_name = item["name"].split(" | ", 1)
                else:
                    weapon = item["name"]
                    skin_name = ""
                text = f"{item['id']:<4} | {weapon:<20} | {skin_name:<25} | {item['price']:.2f} kr"
            else:
                text = item["name"]
            
            prefix = "→ " if i == current else "  "
            if i == current:
                stdscr.addstr(y, 2, prefix + text, curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, prefix + text)
        
        # Footer
        stdscr.addstr(h - 2, 2, "↑/↓: Navigera | ENTER: Välj | Q: Avsluta", curses.A_DIM)
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP and current > 0:
            current -= 1
        elif key == curses.KEY_DOWN and current < len(menu_options) - 1:
            current += 1
        elif key in (10, 13):
            return current
        elif key in (ord('q'), ord('Q')):
            return None

def show_details(stdscr, skin):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    stdscr.addstr(1, 2, f"ID: {skin['id']}")
    stdscr.addstr(2, 2, f"Namn: {skin['name']}")
    stdscr.addstr(3, 2, f"Pris: {skin['price']:.2f} kr")
    stdscr.addstr(4, 2, f"Exterior: {skin['exterior']}")
    stdscr.addstr(5, 2, f"Collection: {skin['collection']}")
    stdscr.addstr(7, 2, "Beskrivning:")
    stdscr.addstr(8, 2, "-" * (w - 4))
    
    # Visa beskrivning med wordwrap
    y = 9
    max_width = w - 6
    words = skin['description'].split()
    line = ""
    
    for word in words:
        test = line + " " + word if line else word
        if len(test) <= max_width:
            line = test
        else:
            if y < h - 3:
                stdscr.addstr(y, 4, line)
                y += 1
            line = word
    
    if line and y < h - 3:
        stdscr.addstr(y, 4, line)
    
    stdscr.addstr(h - 2, 2, "Tryck valfri knapp för att gå tillbaka...", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()

def add_skin(stdscr, skins):
    new_id = max([s["id"] for s in skins], default=0) + 1
    name = get_input(stdscr, "Namn (Weapon | Skin):")
    desc = get_input(stdscr, "Beskrivning:")
    price = float(get_input(stdscr, "Pris:"))
    ext = get_input(stdscr, "Exterior:")
    coll = get_input(stdscr, "Collection:")
    
    skins.append({
        "id": new_id,
        "name": name,
        "description": desc,
        "price": price,
        "exterior": ext,
        "collection": coll
    })
    save_data(skins)

def delete_skin(stdscr, skins):
    remove_id = int(get_input(stdscr, "ID att ta bort:"))
    original_len = len(skins)
    skins[:] = [s for s in skins if s["id"] != remove_id]
    
    if len(skins) < original_len:
        for i, skin in enumerate(skins, start=1):
            skin["id"] = i
        save_data(skins)

def edit_skin(stdscr, skins):
    edit_id = int(get_input(stdscr, "ID att ändra:"))
    
    for skin in skins:
        if skin["id"] == edit_id:
            new_name = get_input(stdscr, f"Nytt namn ({skin['name']}):")
            if new_name:
                skin["name"] = new_name
            
            new_desc = get_input(stdscr, f"Ny beskrivning ({skin['description'][:30]}...):")
            if new_desc:
                skin["description"] = new_desc
            
            new_price = get_input(stdscr, f"Nytt pris ({skin['price']}):")
            if new_price:
                skin["price"] = float(new_price)
            
            new_ext = get_input(stdscr, f"Ny exterior ({skin['exterior']}):")
            if new_ext:
                skin["exterior"] = new_ext
            
            new_coll = get_input(stdscr, f"Ny collection ({skin['collection']}):")
            if new_coll:
                skin["collection"] = new_coll
            
            save_data(skins)
            return

def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    
    skins = load_data(CSV_FILE)
    
    while True:
        choice = show_menu(stdscr, skins)
        
        if choice is None or choice == len(skins) + 3:
            break
        elif choice == len(skins):
            add_skin(stdscr, skins)
        elif choice == len(skins) + 1:
            delete_skin(stdscr, skins)
        elif choice == len(skins) + 2:
            edit_skin(stdscr, skins)
        else:
            show_details(stdscr, skins[choice])

curses.wrapper(main)