import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
import os
import sys

# -----------------------------
# Create the Root Window First
# -----------------------------
root = tk.Tk()

# -----------------------------
# Custom Font Loading
# -----------------------------
# Pre-requisite: Download DS-Digital from https://www.dafont.com/ds-digital.font and place DS-DIGIT.ttf in a "fonts" folder.
font_path = os.path.join("fonts", "DS-DIGIT.ttf")
if os.name == "nt" and os.path.exists(font_path):
    try:
        import ctypes
        ctypes.windll.gdi32.AddFontResourceExW(os.path.abspath(font_path), 0, 0)
    except Exception as e:
        print("Greška pri učitavanju prilagođenog fonta:", e)

try:
    timer_font = font.Font(root=root, family="DS-Digital", size=48)
except Exception:
    timer_font = font.Font(root=root, family="Courier", size=48)

try:
    ui_font = font.Font(root=root, family="DS-Digital", size=24)
except Exception:
    ui_font = font.Font(root=root, family="Courier", size=24)

# -----------------------------
# Konfiguracija i Globalni Podaci
# -----------------------------
TIMER_A_INITIAL = 20 * 60  # Timer A: levo – podrazumevano 20:00 (1200 sekundi)
timerA_remaining = TIMER_A_INITIAL
timerA_paused = False

timerB_remaining = 0      # Timer B: desno – postavlja se na osnovu opcije
timerB_paused = False     # Za pauziranje Timer B

images = [
    {"file": "assets/replika.png",         "duration": 60,  "name": "Replika"},
    {"file": "assets/pitanje.png",         "duration": 90,  "name": "Pitanje"},
    {"file": "assets/novarec.png",         "duration": 120, "name": "Nova Rec"},
    {"file": "assets/tehnickareplika.png",         "duration": 30,  "name": "Tehnicka Replika"}
]
current_image_index = 0
loaded_images = {}

# -----------------------------
# Utility Functions
# -----------------------------
def format_time(seconds):
    """Vraća vreme u formatu MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

# -----------------------------
# Timer Update Functions
# -----------------------------
def update_timers():
    global timerA_remaining, timerB_remaining, timerA_paused, timerB_paused
    if not timerA_paused and timerA_remaining > 0:
        timerA_remaining -= 1
        left_clock_label.config(text=format_time(timerA_remaining))
    if timerB_remaining > 0:
        if not timerB_paused:
            update_timerB(1)
    else:
        right_clock_label.config(text="00:00")
    root.after(1000, update_timers)

def update_timerB(decrement):
    global timerB_remaining
    timerB_remaining = max(0, timerB_remaining - decrement)
    right_clock_label.config(text=format_time(timerB_remaining))

# -----------------------------
# Event Handlers
# -----------------------------
def reset_timerA(event):
    """Resetuje Timer A na početnu vrednost kada se klikne."""
    global timerA_remaining
    timerA_remaining = TIMER_A_INITIAL
    left_clock_label.config(text=format_time(timerA_remaining))

def toggle_pause():
    """Prekida pauzu/nastavak Timer A."""
    global timerA_paused
    timerA_paused = not timerA_paused
    pause_button.config(text="Nastavi" if timerA_paused else "Pauziraj")

def toggle_pause_timerB():
    """Prekida pauzu/nastavak Timer B."""
    global timerB_paused
    timerB_paused = not timerB_paused
    pause_button_B.config(text="Nastavi T2" if timerB_paused else "Pauziraj T2")

def trigger_image_by_index(index):
    """
    Aktivira opciju na osnovu indeksa (kao pritiskom tastera 1-4).
    Postavlja Timer B na trajanje odgovarajuće opcije i osvežava prikaz.
    """
    global timerB_remaining, current_image_index
    if 0 <= index < len(images):
        current_image_index = index
        image_data = images[index]
        timerB_remaining = image_data["duration"]
        right_clock_label.config(text=format_time(timerB_remaining))
        update_image()

def update_image():
    """Učitava i prikazuje trenutnu sliku (ili njeno ime ako fajl ne postoji)."""
    global current_image_index, image_label, images, loaded_images
    image_data = images[current_image_index]
    if os.path.exists(image_data["file"]):
        pil_image = Image.open(image_data["file"])
        pil_image = pil_image.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(pil_image)
        loaded_images[current_image_index] = photo
        image_label.config(image=photo, text="", anchor="center")
        image_label.image = photo
    else:
        image_label.config(text=image_data["name"], image="",
                           fg="black", bg="dark gray", font=ui_font, anchor="center")

def open_settings():
    """
    Otvara modalni prozor sa podešavanjima za Timer A i trajanja opcija.
    """
    settings_window = tk.Toplevel(root)
    settings_window.title("Podešavanja")
    settings_window.configure(bg="dark gray")
    settings_window.transient(root)
    settings_window.grab_set()
    settings_window.attributes('-topmost', True)
    
    tk.Label(settings_window, text="Početno vreme Timer A (sekundi):", fg="black", bg="dark gray", font=ui_font)\
        .grid(row=0, column=0, padx=10, pady=10, sticky="e")
    timer_a_entry = tk.Entry(settings_window, font=ui_font)
    timer_a_entry.grid(row=0, column=1, padx=10, pady=10)
    timer_a_entry.insert(0, str(TIMER_A_INITIAL))
    
    image_entries = {}
    row_offset = 1
    for i, img in enumerate(images):
        tk.Label(settings_window, text=f"Trajanje '{img['name']}' (sekundi):", fg="black", bg="dark gray", font=ui_font)\
            .grid(row=row_offset+i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(settings_window, font=ui_font)
        entry.grid(row=row_offset+i, column=1, padx=10, pady=5)
        entry.insert(0, str(img["duration"]))
        image_entries[img["name"]] = entry
        
    def save_settings():
        global TIMER_A_INITIAL, timerA_remaining, images
        try:
            new_timer_a = int(timer_a_entry.get())
            TIMER_A_INITIAL = new_timer_a
            timerA_remaining = new_timer_a
            left_clock_label.config(text=format_time(timerA_remaining))
        except ValueError:
            print("Nevažeća vrednost za Timer A")
        
        for img in images:
            entry = image_entries.get(img["name"])
            if entry:
                try:
                    new_duration = int(entry.get())
                    img["duration"] = new_duration
                except ValueError:
                    print(f"Nevažeće trajanje za {img['name']}")
        settings_window.destroy()
    
    save_button = tk.Button(settings_window, text="Sačuvaj", command=save_settings,
                            bg="dark gray", fg="black", font=ui_font)
    save_button.grid(row=row_offset+len(images), column=0, columnspan=2, pady=10)

# -----------------------------
# Gradient Background Effect
# -----------------------------
def create_gradient_image(width, height, start_color, end_color):
    """Pravi vertikalni gradijent od start_color do end_color."""
    gradient = Image.new("RGB", (width, height), start_color)
    draw = ImageDraw.Draw(gradient)
    for y in range(height):
        ratio = y / height
        r = int(start_color[0]*(1-ratio) + end_color[0]*ratio)
        g = int(start_color[1]*(1-ratio) + end_color[1]*ratio)
        b = int(start_color[2]*(1-ratio) + end_color[2]*ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return gradient

# -----------------------------
# Main Window Setup
# -----------------------------
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_height = int(screen_height * 0.3)  # Povećana visina na 30% ekrana
root.geometry(f"{screen_width}x{window_height}+0+0")

# Kreiramo gradient pozadinsku sliku i postavljamo je kao pozadinu
start_color = (80, 80, 80)
end_color   = (100, 100, 100)
gradient_img = create_gradient_image(screen_width, window_height, start_color, end_color)
gradient_photo = ImageTk.PhotoImage(gradient_img)
background_label = tk.Label(root, image=gradient_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()

# Uklanjamo standardne prozorske dekoracije
root.overrideredirect(True)

# -----------------------------
# Allow re-enabling override-redirect when the window is restored
# -----------------------------
def on_map(event):
    root.overrideredirect(True)

root.bind("<Map>", on_map)

# -----------------------------
# Minimize Window Function
# -----------------------------
def minimize_window():
    # Temporarily disable override-redirect to allow iconification
    root.overrideredirect(False)
    root.iconify()

# Koristimo grid raspored za glavni prozor
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# -----------------------------
# Top Bar: Settings, Minimize and Close Buttons
# -----------------------------
top_frame = tk.Frame(root, bg="dark gray")
top_frame.grid(row=0, column=0, sticky="ew")
top_frame.columnconfigure(0, weight=1)  # Left side space
top_frame.columnconfigure(1, weight=0)  # Right buttons

# Settings button stays left
settings_button = tk.Button(top_frame, text="Podešavanja", command=open_settings,
                            bg="dark gray", fg="black", bd=0, highlightthickness=0, font=ui_font)
settings_button.grid(row=0, column=0, padx=10, pady=2, sticky="w")



# Right-aligned buttons frame for minimize and close
right_buttons = tk.Frame(top_frame, bg="dark gray")
right_buttons.grid(row=0, column=1, sticky="e")

# Close button with "X" symbol (packed first, appears on the far right)
close_button = tk.Button(right_buttons, text="X", command=root.destroy,
                         bg="dark gray", fg="black", bd=0, highlightthickness=0,
                         font=("Courier", 15, "bold"), width=2, height=1)
close_button.pack(side=tk.RIGHT, padx=(0,10))

# Minimize button with "_" symbol (packed second, appears to the left of close)
minimize_button = tk.Button(right_buttons, text="_", command=minimize_window,
                            bg="dark gray", fg="black", bd=0, highlightthickness=0,
                            font=("Courier", 15, "bold"), width=2, height=1)
minimize_button.pack(side=tk.RIGHT, padx=(0,5))


# -----------------------------
# Middle Area: Dva Tajmera, Slika i Pause Dugmad
# -----------------------------
middle_frame = tk.Frame(root, bg="dark gray")
middle_frame.grid(row=1, column=0, sticky="nsew")
middle_frame.columnconfigure(0, weight=1)
middle_frame.columnconfigure(1, weight=1)
middle_frame.columnconfigure(2, weight=1)

# Kreiramo sub-frame za Timer A
frameA = tk.Frame(middle_frame, bg="dark gray")
frameA.grid(row=0, column=0, sticky="nsew")
left_clock_label = tk.Label(frameA, text=format_time(TIMER_A_INITIAL),
                            font=timer_font, fg="black", bg="dark gray")
left_clock_label.pack(padx=20, pady=(10,5))
left_clock_label.bind("<Button-1>", reset_timerA)
pause_button = tk.Button(frameA, text="Pauziraj", command=toggle_pause,
                         bg="dark gray", fg="black", font=ui_font)
pause_button.pack(pady=(5,10))

# Kreiramo sub-frame za Timer B
frameB = tk.Frame(middle_frame, bg="dark gray")
frameB.grid(row=0, column=1, sticky="nsew")
right_clock_label = tk.Label(frameB, text="00:00",
                             font=timer_font, fg="black", bg="dark gray")
right_clock_label.pack(padx=20, pady=(10,5))
pause_button_B = tk.Button(frameB, text="Pauziraj T2", command=toggle_pause_timerB,
                           bg="dark gray", fg="black", font=ui_font)
pause_button_B.pack(pady=(5,10))

# Image Area u trećoj koloni
image_label = tk.Label(middle_frame, bg="dark gray", anchor="center")
image_label.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")
update_image()

# -----------------------------
# Bottom Area: Dugmad 1 2 3 4 sa Tooltip-om
# -----------------------------
bottom_frame = tk.Frame(root, bg="dark gray")
bottom_frame.grid(row=2, column=0, sticky="ew", pady=5)

tooltip_label = tk.Label(bottom_frame, text="", fg="black", bg="dark gray", font=ui_font)
tooltip_label.pack(side=tk.BOTTOM, pady=(0,5))

buttons_frame = tk.Frame(bottom_frame, bg="dark gray")
buttons_frame.pack(side=tk.TOP)
for i in range(4):
    btn = tk.Button(buttons_frame, text=str(i+1), font=ui_font,
                    bg="dark gray", fg="black", bd=1,
                    command=lambda i=i: trigger_image_by_index(i))
    btn.grid(row=0, column=i, padx=10, pady=5)
    btn.bind("<Enter>", lambda e, i=i: tooltip_label.config(text=images[i]["name"]))
    btn.bind("<Leave>", lambda e: tooltip_label.config(text=""))

# -----------------------------
# Key Bindings
# -----------------------------
root.bind("1", lambda event: trigger_image_by_index(0))
root.bind("2", lambda event: trigger_image_by_index(1))
root.bind("3", lambda event: trigger_image_by_index(2))
root.bind("4", lambda event: trigger_image_by_index(3))

update_timers()
root.mainloop()
