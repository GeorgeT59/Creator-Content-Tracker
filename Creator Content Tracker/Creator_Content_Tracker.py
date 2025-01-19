import tkinter as tk            #Changing 'tkinter' to 'tk' for easier reading/writing.
import webbrowser               #For clickable URLs.
import json                     #For reading/writing JSON files.
from datetime import datetime   #To use anything with datetime/timestamps.
import subprocess

is_incognito = False

def toggle_mode():
    """Toggle between regular and incognito mode."""
    global is_incognito
    is_incognito = not is_incognito
    toggle_button.config(text="Incognito Mode ON" if is_incognito else "Incognito Mode OFF")
    print(f"Toggle button clicked. Incognito Mode is now {'ON' if is_incognito else 'OFF'}")  # Debugging log

def refresh_listbox():
    """Refresh Listbox with JSON data."""
    listbox.delete(0, tk.END)
    try:
        with open("../Creator Content Tracker/JSON/test.json", "r") as f:
            data = json.load(f)
        for item in data:
            row_text = " | ".join(str(value) for value in item.values())
            listbox.insert(tk.END, row_text)
    except FileNotFoundError:
        listbox.insert(tk.END, "JSON file not found.")

def on_item_click(event):
    """Handle the selection of a Listbox item."""
    global is_incognito
    print(f"Incognito Mode status before click: {is_incognito}")  # Debugging log
    selected_index = listbox.curselection()
    if selected_index:
        with open("../Creator Content Tracker/JSON/test.json", "r") as f:
            data = json.load(f)  # Load the JSON as a list of dictionaries

        index = selected_index[0]
        selected_item = data[index]

        # Handle behavior based on incognito mode
        if is_incognito:
            url = selected_item.get("website", "")
            if "www." in url or "http" in url:
                url = url if url.startswith("http") else f"https://{url}"
                try:
                    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--incognito", url], check=True)
                except FileNotFoundError:
                    print("Google Chrome is not installed or not in the system PATH.")
                return
            else:
                print("No valid URL found for incognito mode.")
                return
        else:
            # Get the current date (this will overwrite the previous value)
            current_date = datetime.now().strftime("%m/%d/%Y")

            # Overwrite the date_clicked field with the current date
            selected_item["date_clicked"] = current_date

            # Update JSON file
            with open("../Creator Content Tracker/JSON/test.json", "w") as f:
                json.dump(data, f, indent=4)

            # Update the Listbox
            updated_row_text = " | ".join(str(value) for value in selected_item.values())
            listbox.delete(index)
            listbox.insert(index, updated_row_text)

            # Open the URL if it's present
            url = selected_item.get("website", "")
            if "www." in url or "http" in url:
                url = url if url.startswith("http") else f"https://{url}"
                webbrowser.open(url)

def open_url():
    webbrowser.open("https://github.com/GeorgeT59")

def openNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.title("My awesomeness.")
    newWindow.geometry("400x400")
    
    # Create a label in the new window
    label = tk.Label(newWindow, text="This was made with Python. \n Feel free to view my portfolio in the button below.")
    label.pack(pady=20)  # Use .pack() to place it in the new window
    
    # Create a button in the new window
    button = tk.Button(newWindow, text="My Github", command=open_url)
    button.pack(pady=20)

root = tk.Tk()
root.title("Creator Content Tracker")
root.geometry("800x800")

menu = tk.Menu(root)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Exit", command=root.destroy)

about_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About this Program", command = openNewWindow)

root.configure(menu=menu)

myFont = ("Time New Roman", 20)
font_style = ("Times New Roman", 25)
rootColor = "#7a7a78"
buttonColor = "#e2cff4"
root.config(bg=rootColor)

toggle_button = tk.Button(root, text="Incognito Mode OFF", command=toggle_mode, font=("Arial", 12))
toggle_button.pack(pady=10)

listbox = tk.Listbox(root, height=30, width=60, font=font_style)
listbox.pack(pady=150)

listbox.bind("<<ListboxSelect>>", on_item_click)
refresh_listbox()

#Keeps the window running:
root.mainloop()
