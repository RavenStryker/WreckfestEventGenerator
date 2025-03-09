import os
import subprocess
import ctypes
import ssl
import urllib.request
import sys
import configparser
import random
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import PhotoImage
from tkinter import ttk

# Check if this is the first run
if not os.path.exists("first_run"):
    # Mark this as the first run
    with open("first_run", "w"):
        pass
    def install_package(package):
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call(["pip", "install", package])

    # Check if Python is installed
    if not sys.executable:
        url = 'https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe'

        with urllib.request.urlopen(url, context=ssl.SSLContext()) as u, open('python-installer.exe', 'wb') as f:
            f.write(u.read())

        # Download and install Python
        os.system('python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0')
        os.remove('python-installer.exe')

    # Check if pip is installed
    try:
        import pip
    except ImportError:
        # Download and install pip
        url = 'https://bootstrap.pypa.io/get-pip.py'
        with urllib.request.urlopen(url, context=ssl.SSLContext()) as f:
            data = f.read()
        exec(data)

    install_package("pywin32")
    import win32com.client

    def is_font_installed(font_name):
        wmi = win32com.client.GetObject("winmgmts:")
        fonts = wmi.ExecQuery("SELECT * FROM Win32_FontInfoAction WHERE Caption='{0}'".format(font_name))
        return len(fonts) > 0
        
    script_dir = os.path.dirname(os.path.realpath(__file__))
    font_name = "Nunito-Bold.ttf"
    font_path = os.path.join(script_dir, "fonts", "Nunito-Bold.ttf")
    font_installer_path = os.path.join(script_dir, "fonts", "windows_font_installer.py")

    if not is_font_installed(font_name):
        try:
            subprocess.call(["python", font_installer_path, font_path])
        except Exception as e:
            print(f"Error installing font: {e}")

    print(f"Fonts successfully installed")

# Get the full path to the INI file
inifile = os.path.join(os.path.dirname(__file__), 'settings.ini')

# Create the configparser object and read the INI file
config = configparser.ConfigParser()
config.read(inifile)

def set_title_font(label_widget, text):
    font = ImageFont.truetype(r'fonts\Nunito-Bold.ttf', size=25)
    image = Image.new('RGBA', (250, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, antialias=True, fill="#FFFFFF")
    photo_image = ImageTk.PhotoImage(image)
    label_widget.config(image=photo_image)
    label_widget.image = photo_image
    
def set_sub_font(label_widget, text):
    font = ImageFont.truetype(r'fonts\Nunito-SemiBold.ttf', size=20)
    image = Image.new('RGBA', (250, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, antialias=True, fill="#FFFFFF")
    photo_image = ImageTk.PhotoImage(image)
    label_widget.config(image=photo_image)
    label_widget.image = photo_image

def set_tooltip_font(label_widget, text):
    font = ImageFont.truetype(r'fonts\Nunito-Bold.ttf', size=20)
    image = Image.new('RGBA', (15, 30), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, antialias=True, fill="#FFFFFF")
    photo_image = ImageTk.PhotoImage(image)
    label_widget.config(image=photo_image)
    label_widget.image = photo_image
    
# def set_entry_font(entry_widget, draw_object, font_size):
    # font_path = (r'fonts\Nunito-Bold.ttf')
    # font = ImageFont.truetype(font_path, size=font_size)
    # entry_widget.config(font=(font_path, font_size))
    # draw_object.text((0, 0), "Sample Text", font=font)

    
def set_button_font(button_widget, text):
    font = ImageFont.truetype(r'fonts\Nunito-Bold.ttf', size=25)
    image = Image.new('RGBA', (192, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), text, font=font, spacing=0)
    text_x = (image.width - text_bbox[2]) // 2
    text_y = (image.height - text_bbox[3]) // 2
    draw.text((0, -5), text, font=font, antialias=True, fill="#FFFFFF")
    photo_image = ImageTk.PhotoImage(image)
    button_widget.config(image=photo_image)
    button_widget.image = photo_image


class CustomToolTip:
    def __init__(self, widget, text, font_style=("Helvetica", 14), text_color="#000000"):
        self.widget = widget
        self.text = text
        self.font_style = font_style
        self.text_color = text_color  # Specify the desired text color
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, justify="left", background="#ffffff",
                         relief="solid", borderwidth=2, font=self.font_style, foreground=self.text_color)
        label.pack(ipadx=5, ipady=5)

    def hide_tooltip(self, _):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class ServerConfigGenerator:
    def __init__(self):
        # Load preferences from settings.ini
        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")

        # Check if 'Preferences' section exists and create it if it does not
        if 'Preferences' not in self.config.sections():
            self.config['Preferences'] = {}

        # Set up the window
        self.window = tk.Tk()
        self.window.title("Wreckfest Random Event Generator")
        self.window.geometry("1000x315")
        self.window.resizable(False, False)
        self.window.configure(background="#222222")

        # Get the width and height of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate the x and y coordinates of the top-left corner of the window
        window_width = 1000  # replace with your desired window width
        window_height = 390  # replace with your desired window height
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry of the window
        self.window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
        
        # Define the style for the Entry widgets
        entry_style = ttk.Style()
        entry_style.tk.call("source", r'theme\breeze-dark\breeze-dark.tcl')
        entry_style.theme_use('breeze-dark')
        entry_style.configure('TEntry')

        # Set up the widgets
        self.server_name_label = tk.Label(self.window, background="#222222")
        set_title_font(self.server_name_label, "Server Name")
        self.server_name_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.server_name_entry.insert(tk.END, self.config.get("Preferences", "ServerName"))
        self.server_name_entry.place(x=25, y=37, width=450, height=40)
        self.server_name_draw = ImageDraw.Draw(Image.new("RGB", (25, 50)))


        self.tooltip_server_name_label = tk.Label(self.window, background="#707070")
        set_tooltip_font(self.tooltip_server_name_label, "?")
        CustomToolTip(self.tooltip_server_name_label, "Text coloring for server name and welcome message.\nType these before the text you want to color.\n\nex: ^2Hello World. ^5Today is a good day.\n\nRed: ^1\nGreen: ^2\nOrange ^3\nBlue: ^4\nCyan: ^5\nMagenta: ^6\nWhite: ^7\nGrey: ^8\nBlack: ^9\nYellow: ^:")


        self.password_label = tk.Label(self.window, background="#222222")
        set_title_font(self.password_label, "Password")
        self.password_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.password_entry.insert(0, self.config.get("Preferences", "Password"))
        self.password_entry.place(x=525, y=37, width=450, height=40)


        self.welcome_message_label = tk.Label(self.window, background="#222222")
        set_title_font(self.welcome_message_label, "Welcome Message")
        self.welcome_message_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.welcome_message_entry.insert(tk.END, self.config.get("Preferences", "WelcomeMessage"))
        self.welcome_message_entry.place(x=25, y=112, width=950, height=40)


        self.laps_small_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.laps_small_label, "S.Track Lap Range")
        self.laps_small_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.laps_small_entry.insert(0, self.config.get("Preferences", "LapsSmallRange"))
        self.laps_small_entry.place(x=25, y=186, width=200, height=40)

        
        self.laps_medium_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.laps_medium_label, "M.Track Lap Range")
        self.laps_medium_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.laps_medium_entry.insert(0, self.config.get("Preferences", "LapsMediumRange"))
        self.laps_medium_entry.place(x=275, y=186, width=200, height=40)


        self.laps_large_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.laps_large_label, "L.Track Lap Range")
        self.laps_large_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.laps_large_entry.insert(0, self.config.get("Preferences", "LapsLargeRange"))
        self.laps_large_entry.place(x=525, y=186, width=200, height=40)


        self.events_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.events_label, "Number of Events")
        self.events_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.events_entry.insert(0, self.config.get("Preferences", "NumEvents"))
        self.events_entry.place(x=775, y=186, width=200, height=40)


        self.session_mode_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.session_mode_label, "Session Mode")
        self.session_mode_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.session_mode_entry.insert(0, self.config.get("Preferences", "SessionMode"))
        self.session_mode_entry.place(x=25, y=260, width=200, height=40)


        self.tooltip_session_label = tk.Label(self.window, background="#707070")
        set_tooltip_font(self.tooltip_session_label, "?")
        CustomToolTip(self.tooltip_session_label, "Session mode can be one of the following:\nnormal = standard single event, cup mode disabled.\nqualify-sprint = qualifying sprint to determine grid order for the next race by finishing position when [grid_order] is set to <qualify>.\nqualify-lap = qualifying lap to determine grid order for the next race by lap times when grid_order is set to qualify.\n30p-aggr = Winner 30, then 27, 25, 23, 20 and the rest one less point per position.\n25p-aggr = Winner 25, then 18, 15, 12, 10, 8, 6, 4, 2, 1, and positions 11-24 no points.\n25p-mod = Winner 30, then 20, 16, 11 and the rest one less point per position, positions 16-24 no points.\n24p-lin = Winner 24, then one less point per position for next 23 players.\n16p-lin = Winner 16, then one less point per position for next 15 players.\n10p-double = Winner 20, then two less points per position for next 10 players.\n10p-lin = Winner 10, then one less point per position for next 9 players.\n35p-folk = Winner 35, then 30, 25, 20, 18, 16, then one less point per position and positions 22-24 no points.\nf1-1991 = Winner 10, then 6, 4, 3, 2, 1 and from 7th on no points.\nf1-2003 = Winner 10, then 8, 6, 5, 4, 3, 2, 1 and from 9th on no points.\nf1-2010 = Winner 25, then 18, 15, 12, 10, 8, 6, 4, 2, 1 and from 11th on no points.")


        self.admin_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.admin_label, "Server Admin")
        self.admin_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.admin_entry.insert(0, self.config.get("Preferences", "ServerAdmin"))
        self.admin_entry.place(x=275, y=260, width=325, height=40)


        self.mod_label = tk.Label(self.window, background="#222222")
        set_sub_font(self.mod_label, "Server Moderator")
        self.mod_entry = ttk.Entry(style="TEntry", font=("", 16))
        self.mod_entry.insert(0, self.config.get("Preferences", "ServerModerator"))
        self.mod_entry.place(x=650, y=260, width=325, height=40)


        self.generate_button_style = ttk.Style()
        self.generate_button_style.configure("Style.TButton", font=("", 16))
        self.generate_button = ttk.Button(self.window, style="Style.TButton", command=self.generate_config)
        set_button_font(self.generate_button, "Generate Config")
        self.exit_button = ttk.Button(self.window, style="Style.TButton", command=self.window.quit)
        set_button_font(self.exit_button, "Exit Generator")

        # Add the widgets to the window
        self.server_name_label.place(x=30, y=5)
        self.tooltip_server_name_label.place(x=453, y=40)
        self.password_label.place(x=530, y=5)
        self.welcome_message_label.place(x=30, y=80)
        self.laps_small_label.place(x=30, y=159)
        self.laps_medium_label.place(x=280, y=159)
        self.laps_large_label.place(x=530, y=159)
        self.events_label.place(x=780, y=159)
        self.session_mode_label.place(x=30, y=233)
        self.tooltip_session_label.place(x=203, y=264)
        self.admin_label.place(x=280, y=233)
        self.mod_label.place(x=655, y=233)
        self.generate_button.place(x=25, y=330, width=450, height=40)
        self.exit_button.place(x=525, y=330, width=450, height=40)
        
        # Launch the GUI
        self.run()

    def run(self):
        self.window.mainloop()
        
    def generate_config(self):
        # Save preferences to settings.ini
        self.config.set("Preferences", "ServerName", self.server_name_entry.get())
        self.config.set("Preferences", "WelcomeMessage", self.welcome_message_entry.get())
        self.config.set("Preferences", "Password", self.password_entry.get())
        self.config.set("Preferences", "LapsSmallRange", self.laps_small_entry.get())
        self.config.set("Preferences", "LapsMediumRange", self.laps_medium_entry.get())
        self.config.set("Preferences", "LapsLargeRange", self.laps_large_entry.get())
        self.config.set("Preferences", "NumEvents", self.events_entry.get())
        self.config.set("Preferences", "SessionMode", self.session_mode_entry.get())
        self.config.set("Preferences", "ServerAdmin", self.admin_entry.get())
        self.config.set("Preferences", "ServerModerator", self.mod_entry.get())
        with open("settings.ini", "w") as f:
            self.config.write(f)
            
        # Remove previous event details from initial_server_config.cfg
        with open("initial_server_config.cfg", "r") as f:
            lines = f.readlines()
        with open("initial_server_config.cfg", "w") as f:
            log_found = False
            for line in lines:
                if line.startswith("# Event"):
                    continue
                elif line.startswith("#  Use the command /eventloop to enable/disable rotation while in lobby"):
                    log_found = True
                    f.write(line)
                    continue

                if log_found and line.strip() == "":
                    continue

                f.write(line)

        # Generate events
        laps_ranges = {}
        laps_ranges['tracks_small'] = [int(i) for i in self.laps_small_entry.get().split("-")]
        laps_ranges['tracks_medium'] = [int(i) for i in self.laps_medium_entry.get().split("-")]
        laps_ranges['tracks_large'] = [int(i) for i in self.laps_large_entry.get().split("-")]

        num_events = int(self.events_entry.get())
        events_list = []

        for i in range(num_events):
            event = {}

            # Choose random track and laps
            track_category = random.choice(['tracks_small', 'tracks_medium', 'tracks_large'])
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tracks', track_category + ".txt")) as f:
                tracks = f.readlines()
            event["track"] = random.choice(tracks).strip()
            event["laps"] = random.randint(laps_ranges[track_category][0], laps_ranges[track_category][1])

            # Choose random gamemode
            event["gamemode"] = "racing"
            event["damage"] = "normal"

            # Use the value entered in the session_entry entry widget
            event["session_mode"] = self.session_mode_entry.get()

            events_list.append(event)
            
        # Save config to initial_server_config.cfg
        with open("initial_server_config.cfg", "r") as f:
            lines = f.readlines()
        with open("initial_server_config.cfg", "w") as f:
            log_found = False
            for line in lines:
                if line.startswith("server_name="):
                    line = "server_name=" + self.server_name_entry.get() + "\n"
                elif line.startswith("welcome_message="):
                    line = "welcome_message=" + self.welcome_message_entry.get() + "\n"
                elif line.startswith("password="):
                    line = "password=" + self.password_entry.get() + "\n"
                elif line.startswith("admin_steam_ids="):
                    line = "admin_steam_ids=" + self.admin_entry.get() + "\n"
                elif line.startswith("op_steam_ids="):
                    line = "op_steam_ids=" + self.mod_entry.get() + "\n"
                elif line.startswith("session_mode="):
                    line = "session_mode=" + self.session_mode_entry.get() + "\n"
                elif line.startswith("vehicle_damage="):
                    line = "vehicle_damage=" + event["damage"] + "\n"
                elif line.startswith("gamemode="):
                    line = "gamemode=" + event["gamemode"] + "\n"
                elif line.startswith("el_add="):
                    continue
                elif line.startswith("el_laps="):
                    continue
                elif line.startswith("#  Use the command /eventloop to enable/disable rotation while in lobby"):
                    log_found = True
                    f.write(line)
                    continue

                if log_found and line.strip() == "":
                    continue

                f.write(line)

        # Remove empty line breaks after #  Use the command /eventloop to enable/disable rotation while in lobby
        with open("initial_server_config.cfg", "r") as f:
            lines = f.readlines()

        with open("initial_server_config.cfg", "w") as f:
            for i, line in enumerate(lines):
                if line.startswith("#  Use the command /eventloop to enable/disable rotation while in lobby"):
                    f.write(line)
                    for i, event in enumerate(events_list, start=1):
                        f.write("# Event " + str(i) + "\n")
                        f.write("el_add=" + event["track"] + "\n")
                        f.write("el_laps=" + str(event["laps"]) + "\n")
                elif line.strip() != "":
                    f.write(line)
                    
        messagebox.showinfo("Success", "Configuration file generated.")
        
if __name__ == "__main__":
    app = ServerConfigGenerator()
