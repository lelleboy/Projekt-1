import csv
import curses
import webbrowser
import urllib.parse

CSV_FILE = "db_skins.csv"

def generate_link(name):
    """Genererar en Google-sökning baserat på skin-namnet"""
    # Lägg till "CS2 skin" för bättre sökresultat
    search_query = name + " CS2 skin"
    # URL-encode sökningen
    encoded_query = urllib.parse.quote(search_query)
    return f"https://www.google.com/search?q={encoded_query}&tbm=isch"

def load_data(filename):
    skins = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    link = row.get('link', '')
                    if not link:
                        # Generera automatisk länk om ingen finns
                        link = generate_link(row['name'])
                    
                    skins.append({
                        "id": int(row['id']),
                        "name": row['name'],
                        "description": row['description'],
                        "price": float(row['price']),
                        "exterior": row['exterior'],
                        "collection": row['collection'],
                        "link": link
                    })
                except (ValueError, KeyError) as e:
                    # Hoppa över korrupta rader
                    continue
    except FileNotFoundError:
        pass
    return skins

def save_data(skins):
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "id", "name", "description", "price", "exterior", "collection", "link"
            ])
            writer.writeheader()
            writer.writerows(skins)
    except IOError as e:
        # Returnera False om sparandet misslyckades
        return False
    return True

def get_input(stdscr, prompt):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()
    try:
        value = stdscr.getstr(1, 0, 2000).decode("utf-8")
    except:
        value = ""
    curses.noecho()
    return value

def show_message(stdscr, message, wait=True):
    """Visar ett meddelande till användaren"""
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(h // 2, max(0, (w - len(message)) // 2), message)
    stdscr.refresh()
    if wait:
        stdscr.getch()

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
        try:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            # Kontrollera minimal terminalstorlek
            if h < 10 or w < 50:
                stdscr.addstr(0, 0, "Terminal för liten! Behöver minst 50x10")
                stdscr.refresh()
                stdscr.getch()
                continue
            
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
        except curses.error:
            # Hantera curses-fel (t.ex. terminalstorlek)
            continue

def show_details(stdscr, skin):
    try:
        h, w = stdscr.getmaxyx()
        
        # Popup dimensioner
        popup_h = min(20, h - 4)
        popup_w = min(70, w - 4)
        
        # Kontrollera att terminalen är stor nog
        if popup_h < 10 or popup_w < 30:
            show_message(stdscr, "Terminal för liten för att visa detaljer!")
            return
        
        start_y = (h - popup_h) // 2
        start_x = (w - popup_w) // 2
        
        # Rita bakgrunden (huvudmenyn) först
        stdscr.refresh()
        
        # Skapa popup-fönster
        popup = curses.newwin(popup_h, popup_w, start_y, start_x)
        popup.box()
        
        y = 2
        popup.addstr(y, 2, f"ID: {skin['id']}")
        y += 1
        popup.addstr(y, 2, f"Namn: {skin['name']}")
        y += 1
        popup.addstr(y, 2, f"Pris: {skin['price']:.2f} kr")
        y += 1
        popup.addstr(y, 2, f"Exterior: {skin['exterior']}")
        y += 1
        popup.addstr(y, 2, f"Collection: {skin['collection']}")
        y += 1
        
        if skin.get('link'):
            popup.addstr(y, 2, f"Länk: {skin['link']}")
            y += 1
        
        y += 1
        popup.addstr(y, 2, "Beskrivning:")
        y += 1
        popup.addstr(y, 2, "-" * (popup_w - 4))
        y += 1
        
        # Visa beskrivning med wordwrap
        max_width = popup_w - 6
        words = skin['description'].split()
        line = ""
        
        for word in words:
            test = line + " " + word if line else word
            if len(test) <= max_width:
                line = test
            else:
                if y < popup_h - 3:
                    popup.addstr(y, 4, line)
                    y += 1
                line = word
        
        if line and y < popup_h - 3:
            popup.addstr(y, 4, line)
        
        # Footer
        if skin.get('link'):
            popup.addstr(popup_h - 2, 2, "L: Öppna länk | Tryck valfri knapp för att gå tillbaka...", curses.A_DIM)
        else:
            popup.addstr(popup_h - 2, 2, "Tryck valfri knapp för att gå tillbaka...", curses.A_DIM)
        
        popup.refresh()
        
        key = popup.getch()
        if key in (ord('l'), ord('L')) and skin.get('link'):
            try:
                webbrowser.open(skin['link'])
                popup.getch()
            except Exception as e:
                show_message(stdscr, f"Kunde inte öppna länk: {str(e)}")
    except curses.error:
        show_message(stdscr, "Fel vid visning av detaljer")

def add_skin(stdscr, skins):
    try:
        new_id = max([s["id"] for s in skins], default=0) + 1
        name = get_input(stdscr, "Namn (Weapon | Skin):")
        if not name:
            show_message(stdscr, "Namn kan inte vara tomt!")
            return
        
        desc = get_input(stdscr, "Beskrivning:")
        
        price_str = get_input(stdscr, "Pris:")
        try:
            price = float(price_str)
            if price < 0:
                show_message(stdscr, "Priset kan inte vara negativt!")
                return
        except ValueError:
            show_message(stdscr, "Ogiltigt pris! Måste vara ett nummer.")
            return
        
        ext = get_input(stdscr, "Exterior:")
        coll = get_input(stdscr, "Collection:")
        link = get_input(stdscr, "Länk (valfri):")
        
        skins.append({
            "id": new_id,
            "name": name,
            "description": desc,
            "price": price,
            "exterior": ext,
            "collection": coll,
            "link": link
        })
        
        if save_data(skins):
            show_message(stdscr, "Skin tillagd!")
        else:
            show_message(stdscr, "Fel: Kunde inte spara data!")
            skins.pop()  # Ta bort den tillagda skinen om sparandet misslyckades
    except Exception as e:
        show_message(stdscr, f"Fel vid tillägg: {str(e)}")



# Tar bort skin
def delete_skin(stdscr, skins):
    try:
        remove_id_str = get_input(stdscr, "ID att ta bort:")
        try:
            remove_id = int(remove_id_str)
        except ValueError:
            show_message(stdscr, "Ogiltigt ID! Måste vara ett nummer.")
            return
        
        original_len = len(skins)
        skins[:] = [s for s in skins if s["id"] != remove_id]
        
        if len(skins) < original_len:
            for i, skin in enumerate(skins, start=1):
                skin["id"] = i
            if save_data(skins):
                show_message(stdscr, "Skin borttagen!")
            else:
                show_message(stdscr, "Fel: Kunde inte spara data!")
        else:
            show_message(stdscr, f"Ingen skin med ID {remove_id} hittades!")
    except Exception as e:
        show_message(stdscr, f"Fel vid borttagning: {str(e)}")


# Förendrar skin
def edit_skin(stdscr, skins):
    try:
        edit_id_str = get_input(stdscr, "ID att ändra:")
        try:
            edit_id = int(edit_id_str)
        except ValueError:
            show_message(stdscr, "Ogiltigt ID! Måste vara ett nummer.")
            return
        
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
                    try:
                        price_val = float(new_price)
                        if price_val < 0:
                            show_message(stdscr, "Priset kan inte vara negativt!")
                            return
                        skin["price"] = price_val
                    except ValueError:
                        show_message(stdscr, "Ogiltigt pris! Måste vara ett nummer.")
                        return
                
                new_ext = get_input(stdscr, f"Ny exterior ({skin['exterior']}):")
                if new_ext:
                    skin["exterior"] = new_ext
                
                new_coll = get_input(stdscr, f"Ny collection ({skin['collection']}):")
                if new_coll:
                    skin["collection"] = new_coll
                
                new_link = get_input(stdscr, f"Ny länk ({skin.get('link', '')}):")
                if new_link:
                    skin["link"] = new_link
                
                if save_data(skins):
                    show_message(stdscr, "Skin uppdaterad!")
                else:
                    show_message(stdscr, "Fel: Kunde inte spara data!")
                return
        
        show_message(stdscr, f"Ingen skin med ID {edit_id} hittades!")
    except Exception as e:
        show_message(stdscr, f"Fel vid redigering: {str(e)}")


# Meny som väljer vad det är man vill göra
def main(stdscr):
    try:
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    except:
        pass  # Ignorera färgfel om terminalen inte stödjer färg
    
    skins = load_data(CSV_FILE)
    
    while True:
        try:
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
        except KeyboardInterrupt:
            break
        except Exception as e:
            show_message(stdscr, f"Ett oväntat fel uppstod: {str(e)}")

curses.wrapper(main)