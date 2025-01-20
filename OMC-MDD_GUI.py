import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import joblib
import numpy as np

# Load the pre-trained models
def load_model():
    try:
        omc_model = joblib.load("./results/models/OMC_Gradient Boosting_best.pkl")
        mdd_model = joblib.load("./results/models/MDD_Gradient Boosting_best.pkl")
        return omc_model, mdd_model
    except Exception as e:
        messagebox.showerror("Error", f"Error loading models: {e}")
        return None, None

# Update Clay dynamically
def update_clay():
    try:
        gravel = float(entry_widgets["Gravel (%)"].get() or 0)
        sand = float(entry_widgets["Sand (%)"].get() or 0)
        silt = float(entry_widgets["Silt (%)"].get() or 0)
        clay = 100 - (gravel + sand + silt)

        if clay < 0 or clay > 100:
            clay_label.config(text="Invalid")
            messagebox.showerror("Input Error", "The sum of Gravel, Sand, and Silt cannot exceed 100%.")
            return None
        else:
            clay_label.config(text=f"{clay:.2f}%")
            return clay
    except ValueError:
        clay_label.config(text="Invalid")
        return None

# Calculate Plasticity Index dynamically
def calculate_plasticity_index():
    try:
        liquid_limit = entry_widgets["Liquid Limit (%)"].get()
        plastic_limit = entry_widgets["Plastic Limit (%)"].get()

        if liquid_limit and plastic_limit:
            liquid_limit = float(liquid_limit)
            plastic_limit = float(plastic_limit)
            plasticity_index = liquid_limit - plastic_limit

            if plasticity_index < 0:
                plasticity_index_label.config(text="Invalid")
                messagebox.showerror("Input Error", "Plasticity Index cannot be negative.")
                return None
            else:
                plasticity_index_label.config(text=f"{plasticity_index:.2f}")
                return plasticity_index
        else:
            plasticity_index_label.config(text="N/A")
            return None
    except ValueError:
        plasticity_index_label.config(text="Invalid Input")
        return None

# Predict OMC and MDD
def predict_results():
    try:
        omc_model, mdd_model = load_model()
        if omc_model is None or mdd_model is None:
            return

        # Update Clay and Plasticity Index
        clay = update_clay()
        plasticity_index = calculate_plasticity_index()
        if clay is None or plasticity_index is None:
            return

        # Collect inputs from fields
        inputs = []
        for label, entry in entry_widgets.items():
            value = entry.get()
            if not value.strip():
                messagebox.showerror("Input Error", f"Please fill in the {label}.")
                return
            inputs.append(float(value))

        # Append calculated Clay and Plasticity Index to inputs
        inputs.append(plasticity_index)
        inputs.append(clay)

        # Reshape inputs for model prediction
        inputs = np.array(inputs).reshape(1, -1)

        # Make predictions
        omc_prediction = omc_model.predict(inputs)
        mdd_prediction = mdd_model.predict(inputs)

        # Display results
        result_label.config(
            text=(f"Predicted OMC: {omc_prediction[0]:.2f}%\n"
                  f"Predicted MDD: {mdd_prediction[0]:.2f} g/cm³")
        )
    except Exception as e:
        messagebox.showerror("Prediction Error", f"Error during prediction: {e}")

# Copy all entries and results
def copy_all():
    try:
        inputs = [f"{field}: {entry.get()}" for field, entry in entry_widgets.items()]
        clay_text = f"Clay: {clay_label.cget('text')}"
        pi_text = f"Plasticity Index: {plasticity_index_label.cget('text')}"
        results = result_label.cget("text")
        clipboard_content = "\n".join(inputs + [clay_text, pi_text, "\nResults:\n" + results])
        root.clipboard_clear()
        root.clipboard_append(clipboard_content)
        messagebox.showinfo("Copied", "All inputs and results copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Error", f"Error copying data: {e}")

# About the application
def about_application():
    messagebox.showinfo(
        "About This Application",
        "This application predicts the Optimum Moisture Content (OMC) and Maximum Dry Density (MDD) "
        "for soil compaction based on soil properties. Designed and developed by Willie Roy.",
    )

# How to use the application
def how_to_use():
    messagebox.showinfo(
        "How to Use",
        "1. Enter the percentages for Gravel, Sand, and Silt.\n"
        "2. Enter the Liquid Limit, Plastic Limit, and Compaction Energy.\n"
        "3. The values for Clay and Plasticity Index will be calculated automatically.\n"
        "4. Click 'Predict OMC & MDD' to get results.\n"
        "5. Use the 'Copy All' button to save the inputs and results.",
    )

# Create the GUI window
root = tk.Tk()
ico = Image.open('logo.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

root.title("OMC and MDD Prediction Application")
root.geometry("550x650")
root.configure(bg="#e3f2fd")

# Top buttons
top_frame = tk.Frame(root, bg="#e3f2fd")
top_frame.pack(pady=10, fill="x")
tk.Button(top_frame, text="About", command=about_application, bg="#42a5f5", fg="white").pack(side="left", padx=10)
tk.Button(top_frame, text="How to Use", command=how_to_use, bg="#1e88e5", fg="white").pack(side="left", padx=10)


# Logo
try:
    logo_path = "./presentation2.png"
    logo = Image.open(logo_path).resize((500, 100), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    tk.Label(root, image=logo_img, bg="#e8f5e9").pack(pady=10)
except Exception:
    tk.Label(root, text="Logo not available.", fg="red", bg="#e8f5e9").pack()

    
# Input frame
input_frame = tk.Frame(root, bg="#e3f2fd")
input_frame.pack(pady=10, padx=10, fill="x")
fields_dict = {
    "Gravel (%)": "Gravel content as a percentage",
    "Sand (%)": "Sand content as a percentage",
    "Silt (%)": "Silt content as a percentage",
    "Liquid Limit (%)": "Water content where soil flows",
    "Plastic Limit (%)": "Water content where soil deforms plastically",
    "Compaction Energy (kN-m/m³)": "Energy applied during compaction",
}
entry_widgets = {}
for i, (label_text, desc_text) in enumerate(fields_dict.items()):
    tk.Label(input_frame, text=label_text, anchor="w", bg="#e3f2fd", font=("Arial", 10)).grid(row=i * 2, column=0, padx=10, pady=2, sticky="w")
    tk.Label(input_frame, text=desc_text, anchor="w", bg="#e3f2fd", fg="gray", font=("Arial", 8, "italic")).grid(row=i * 2 + 1, column=0, padx=10, sticky="w")
    entry = tk.Entry(input_frame, bg="white", fg="black")
    entry.grid(row=i * 2, column=1, padx=10, pady=2, sticky="ew")
    entry_widgets[label_text] = entry

# Calculated values frame
calc_frame = tk.Frame(root, bg="#e3f2fd")
calc_frame.pack(pady=10, fill="x")
tk.Label(calc_frame, text="Clay (%):", anchor="w", bg="#e3f2fd", font=("Arial", 10)).pack(side="left", padx=10)
clay_label = tk.Label(calc_frame, text="N/A", bg="#e3f2fd", fg="blue", font=("Arial", 10, "bold"))
clay_label.pack(side="left", padx=5)

tk.Label(calc_frame, text="Plasticity Index:", anchor="w", bg="#e3f2fd", font=("Arial", 10)).pack(side="left", padx=20)
plasticity_index_label = tk.Label(calc_frame, text="N/A", bg="#e3f2fd", fg="blue", font=("Arial", 10, "bold"))
plasticity_index_label.pack(side="left", padx=5)

# Buttons
btn_frame = tk.Frame(root, bg="#e3f2fd")
btn_frame.pack(pady=20)
tk.Button(btn_frame, text="Predict OMC & MDD", command=predict_results, bg="#4caf50", fg="white", font=("Arial", 10)).pack(side="left", padx=10)
tk.Button(btn_frame, text="Copy All", command=copy_all, bg="#ff9800", fg="white", font=("Arial", 10)).pack(side="left", padx=10)

# Results
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#e3f2fd", fg="blue")
result_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="Developed by Rod WIll", font=("Arial", 10, "italic"), bg="#e3f2fd", fg="gray")
footer.pack(side="bottom", pady=5)

# Bind entry changes to update functions
entry_widgets["Gravel (%)"].bind("<KeyRelease>", lambda event: update_clay())
entry_widgets["Sand (%)"].bind("<KeyRelease>", lambda event: update_clay())
entry_widgets["Silt (%)"].bind("<KeyRelease>", lambda event: update_clay())
entry_widgets["Liquid Limit (%)"].bind("<KeyRelease>", lambda event: calculate_plasticity_index())
entry_widgets["Plastic Limit (%)"].bind("<KeyRelease>", lambda event: calculate_plasticity_index())

# Run the application
root.mainloop()
