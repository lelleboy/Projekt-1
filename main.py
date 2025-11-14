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

def curses_input(win, prompt):
    curses.echo()
    win.clear()
    win.addstr(0, 0, prompt)
    win.refresh()
    value = win.getstr(1, 0).decode("utf-8")
    curses.noecho()
    return value

def skin_menu(stdscr, skins):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    current_row = 0
    scroll_offset = 0

    menu_items = skins.copy()
    menu_items.append({"name": "➡ Lägg till skin"})
    menu_items.append({"name": "➡ Ta bort skin"})
    menu_items.append({"name": "➡ Ändra skin"})
    menu_items.append({"name": "➡ Avsluta"})

    def draw():
        nonlocal scroll_offset
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        visible_height = h - 8

        if current_row < scroll_offset:
            scroll_offset = current_row
        elif current_row >= scroll_offset + visible_height:
            scroll_offset = current_row - visible_height + 1

        header_text = "ID".ljust(4) + " | " + "Weapon".ljust(20) + " | " + "Skin".ljust(25) + " | " + "Price".ljust(10)
        x = max(0, w // 2 - len(header_text) // 2)
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, x, header_text[:w-1])
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(2, x, "─" * min(len(header_text), w-1))

        for i in range(scroll_offset, min(len(menu_items), scroll_offset + visible_height)):
            item = menu_items[i]
            y = 4 + (i - scroll_offset)
            if "price" in item and " | " in item["name"]:
                weapon, skin = item["name"].split(" | ", 1)
                price = f"{item['price']:.2f} kr"
                id_str = str(item["id"]).ljust(4)
            else:
                weapon = item["name"]
                skin = ""
                price = ""
                id_str = "    "
            text = id_str + " | " + weapon.ljust(20) + " | " + skin.ljust(25) + " | " + price.ljust(10)
            x_text = max(0, w // 2 - len(text) // 2)
            display_text = ("→ " if i == current_row else "  ") + text
            stdscr.addstr(y, x_text - 3, display_text[:w-1], curses.color_pair(1) if i == current_row else curses.color_pair(3))

        footer = "↑/↓ navigera   ENTER välj   Q avsluta"
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(h - 2, max(0, w // 2 - len(footer) // 2), footer)
        stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()

    draw()

    while True:
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key in (10, 13):
            return current_row
        elif key in (ord("q"), ord("Q")):
            return None
        draw()

def main(stdscr):
    skins = load_data(CSV_FILE)
    while True:
        choice = skin_menu(stdscr, skins)
        if choice is None or choice == len(skins) + 3:
            break
        if choice == len(skins):
            new_id = max([s["id"] for s in skins], default=0) + 1
            name = curses_input(stdscr, "Namn (Weapon | Skin):")
            desc = curses_input(stdscr, "Beskrivning:")
            price = float(curses_input(stdscr, "Pris:"))
            ext = curses_input(stdscr, "Exterior:")
            coll = curses_input(stdscr, "Collection:")
            skins.append({
                "id": new_id,
                "name": name,
                "description": desc,
                "price": price,
                "exterior": ext,
                "collection": coll
            })
            save_data(skins)
        elif choice == len(skins) + 1:
            remove_id = int(curses_input(stdscr, "ID att ta bort:"))
            skins = [s for s in skins if s["id"] != remove_id]
            save_data(skins)
        elif choice == len(skins) + 2:
            edit_id = int(curses_input(stdscr, "ID att ändra:"))
            target = next((s for s in skins if s["id"] == edit_id), None)
            if target:
                target["name"] = curses_input(stdscr, f"Nytt namn ({target['name']}):") or target["name"]
                target["description"] = curses_input(stdscr, f"Ny beskrivning ({target['description']}):") or target["description"]
                new_price = curses_input(stdscr, f"Nytt pris ({target['price']}):")
                if new_price:
                    target["price"] = float(new_price)
                target["exterior"] = curses_input(stdscr, f"Ny exterior ({target['exterior']}):") or target["exterior"]
                target["collection"] = curses_input(stdscr, f"Ny collection ({target['collection']}):") or target["collection"]
                save_data(skins)
        else:
            s = skins[choice]
            stdscr.clear()
            stdscr.addstr(2, 2, f"ID: {s['id']}")
            stdscr.addstr(3, 2, f"Namn: {s['name']}")
            stdscr.addstr(4, 2, f"Beskrivning: {s['description']}")
            stdscr.addstr(5, 2, f"Pris: {s['price']:.2f} kr")
            stdscr.addstr(6, 2, f"Exterior: {s['exterior']}")
            stdscr.addstr(7, 2, f"Collection: {s['collection']}")
            stdscr.addstr(9, 2, "Tryck valfri knapp för att återgå till menyn...")
            stdscr.refresh()
            stdscr.getch()

curses.wrapper(main)
