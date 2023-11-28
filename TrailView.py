import tkinter as tk
from tkinter import ttk, messagebox
from trail_data_reader import read_trail_data

def display_filtered_trails(trail_data, foot, bicycle, horse, wheelchair, motor_vehi):
    if not trail_data:
        messagebox.showinfo("Message", "No trail data available.")
        return

    text_widget.delete("1.0", tk.END)  # Clear previous content

    # Display trails based on selected filter options
    filtered_trails = []
    for trail in trail_data:
        if (foot == "All" or str(trail.get("foot", "")).lower() == foot.lower()) and \
           (bicycle == "All" or str(trail.get("bicycle", "")).lower() == bicycle.lower()) and \
           (horse == "All" or str(trail.get("horse", "")).lower() == horse.lower()) and \
           (wheelchair == "All" or str(trail.get("wheelchair", "")).lower() == wheelchair.lower()) and \
           (motor_vehi == "All" or str(trail.get("motor_vehi", "")).lower() == motor_vehi.lower()):
            filtered_trails.append(trail)

    for trail in filtered_trails:
        for key, value in trail.items():
            text_widget.insert(tk.END, f"{key}: {value}\n", "bold")
        text_widget.insert(tk.END, "\n")

# Function to handle filter button click
def filter_trails():
    foot_value = foot_var.get()
    bicycle_value = bicycle_var.get()
    horse_value = horse_var.get()
    wheelchair_value = wheelchair_var.get()
    motor_vehi_value = motor_vehi_var.get()

    display_filtered_trails(trail_data, foot_value, bicycle_value, horse_value, wheelchair_value, motor_vehi_value)

# Create the main application window
root = tk.Tk()
root.title("TrailView")
root.geometry("1200x1200")

# Create a Text widget with vertical scroll bar
text_widget = tk.Text(root, wrap=tk.WORD, height=20, width=80)
scroll_y = tk.Scrollbar(root, command=text_widget.yview)
text_widget.configure(yscrollcommand=scroll_y.set)

text_widget.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Dropdown menus for filtering
filter_labels = ["Foot", "Bicycle", "Horse", "Wheelchair", "Motor Vehicle"]
filter_options = ["All", "Yes", "No"]

foot_var = tk.StringVar()
foot_var.set(filter_options[0])

bicycle_var = tk.StringVar()
bicycle_var.set(filter_options[0])

horse_var = tk.StringVar()
horse_var.set(filter_options[0])

wheelchair_var = tk.StringVar()
wheelchair_var.set(filter_options[0])

motor_vehi_var = tk.StringVar()
motor_vehi_var.set(filter_options[0])

filter_vars = [foot_var, bicycle_var, horse_var, wheelchair_var, motor_vehi_var]

for i, label in enumerate(filter_labels):
    label_widget = tk.Label(root, text=f"{label} Filter:")
    label_widget.pack(pady=(10, 0))

    filter_dropdown = ttk.Combobox(root, textvariable=filter_vars[i], values=filter_options)
    filter_dropdown.pack(pady=(0, 10))

filter_button = tk.Button(root, text="Apply Filter", command=filter_trails)
filter_button.pack()

# Specify the path to the CSV file
csv_file_path = 'California_Coastal_Trail_(CCT)_.csv'

# Read trail data from the CSV file
trail_data = read_trail_data(csv_file_path)

# Display all trails in the Tkinter application initially
display_filtered_trails(trail_data, "All", "All", "All", "All", "All")

# Run the Tkinter event loop
root.mainloop()