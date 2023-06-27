import tkinter as tk
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
import easyocr
from fpdf import FPDF
import pyperclip
from PIL import ImageDraw

languages = {
    "Telugu": "te",
    "Vietnamese": "vi",
    "Lithuanian": "lt",
    "French": "fr",
    "Thai": "th",
    "Czech": "cs",
    "Bengali": "bn",
    "Spanish": "es",
    "Russian": "ru",
    'Urdu': 'ur',
    'Latvian': 'lv',
    'Italian': 'it',
    'Swahili': 'sw',
    'Ukrainian': 'uk',
    'Korean': 'ko',
    'English': 'en',
    'Romanian': 'ro',
    'Nepali': 'ne',
    'Indonesian': 'id',
    'marathi': 'mr',
    'arabic': 'ar',
    'hindi': 'hi',
    'german': 'de',
    'persian': 'fa',
    'estonian': 'et',
    'polish': 'pl',
    'sweden': 'sv',
    "Portugese": "pt",
    "Turkish": "tr",
    "Afrikaans": "af",
    "Tamil": "ta",
    "Dutch": "nl",
    "Tagalog": "tl",
    "Slovenian": "sl"
}


def copy_to_clipboard():
    text = text_output.get(1.0, tk.END)
    pyperclip.copy(text)


# Function to save text to a file
def save_text_to_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


# Function to convert text file to PDF
def convert_to_pdf(filename):
    pdf = FPDF()
    pdf.add_page()
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_filename = filename[:-4] + '.pdf'
    pdf.output(pdf_filename)

def draw_boxes(image, bounds, color='green', width=3):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image


# Function to handle image selection
def select_image():
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    
    if image_path and language_var.get() in languages :
        image = Image.open(image_path)
        image.thumbnail((200, 200))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent garbage collection

        reader = easyocr.Reader([languages[language_var.get()]])
        output = reader.readtext(image_path)
        text = [elem[1] for elem in output]
        
        im = Image.open(image_path)
        
        image = draw_boxes(im,output)
        
        image.thumbnail((200, 200))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label2.config(image=photo)
        image_label2.image = photo  # Keep a reference to the image to prevent garbage collection

        var = ""
        for lines in text:
            var += lines + '\n'

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, var)


# Function to handle saving text to a file
def save_text_file():
    text = text_output.get(1.0, tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        save_text_to_file(text, filename)


# Function to handle converting text to PDF
def convert_to_pdf_action():
    text = text_output.get(1.0, tk.END)
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filename:
        convert_to_pdf(text)


# Create the Tkinter app
app = tk.Tk()
app.title("Image Text Extractor")
app.geometry("600x700")


# Language selection drop-down
# Add more languages as needed
language_label = tk.Label(app, text="Select Language:")
language_label.pack()
language_var = tk.StringVar(app)
language_dropdown = tk.OptionMenu(app, language_var, *languages.keys())
language_dropdown.pack(pady=5)


# def on_language_change(*args):
#     select_image(language_changed=True)


# language_var.trace("w", on_language_change)


# Image selection button
image_button = tk.Button(app, text="Select Image", command=select_image)
image_button.pack(pady=10)

# Image display
image_label = tk.Label(app)
image_label.pack()

# Image display
image_label2 = tk.Label(app)
image_label2.pack()

# Text output fields
text_output_label = tk.Label(app, text="Extracted Text in Chosen Language:")
text_output_label.pack()
text_output = tk.Text(app, height=5)
text_output.pack(pady=5)

# Copy to clipboard button
copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=10)

# Save text file button
save_text_button = tk.Button(app, text="Download Text File", command=save_text_file)
save_text_button.pack(pady=10)

# Convert to PDF button
pdf_button = tk.Button(app, text="Download PDF", command=convert_to_pdf_action)
pdf_button.pack()

# Run the Tkinter event loop
app.mainloop()
