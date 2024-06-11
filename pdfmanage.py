import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import os

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_input_path.delete(0, tk.END)
    entry_input_path.insert(0, file_path)

def choose_save_location():
    directory = filedialog.askdirectory()
    entry_save_location.delete(0, tk.END)
    entry_save_location.insert(0, directory)

def choose_color():
    color_code = colorchooser.askcolor(title="Colour Picker")
    if color_code:
        rgb_color = color_code[0]
        if rgb_color:
            color_str = f"{int(rgb_color[0])},{int(rgb_color[1])},{int(rgb_color[2])}"
            entry_color.delete(0, tk.END)
            entry_color.insert(0, color_str)

def highlight_pdf():
    pdf_path = entry_input_path.get()
    save_location = entry_save_location.get()
    output_filename = entry_output_filename.get()
    column_name = column_name_entry.get()
    highlight_value = highlight_value_entry.get()
    highlight_color = entry_color.get()

    if not pdf_path or not save_location or not output_filename:
        messagebox.showerror("Error", "All fields are required.")
        return

    output_path = f"{save_location}/{output_filename}.pdf"
    

    if os.path.exists(output_path):
        overwrite = messagebox.askyesno("File Exists", f"The file '{output_filename}.pdf' already exists. Do you want to overwrite it?")
        if not overwrite:
            return

    try:
        highlight_color = tuple(map(int, highlight_color.split(',')))
        highlight_color = tuple(c / 255.0 for c in highlight_color)  # RGB değerlerini 1 üzerinden normalize et
    except ValueError:
        messagebox.showerror("Error", "The colour value is invalid. It must be in RGB format (for example, 255,0,0).")
        return

    document = fitz.open(pdf_path)

    for page_num in range(len(document)):
        page = document[page_num]
        text_instances_qty = page.search_for(column_name)

        if text_instances_qty:
            qty_bbox = text_instances_qty[0]
            print(f"Page {page_num + 1} - {column_name} value in the column:", qty_bbox)

            all_words = page.get_text("words")

            for word in all_words:
                bbox, text = word[:4], word[4].strip()
                if (qty_bbox.x0 - 10 <= bbox[0] <= qty_bbox.x1 + 10) and (qty_bbox.y1 < bbox[1]):
                    print(f"Page {page_num + 1} - {column_name} value in the column:", text, "Coordinates:", bbox)
                    if text == highlight_value:
                        highlight = page.add_highlight_annot(fitz.Rect(bbox))
                        highlight.set_colors(stroke=highlight_color)
                        highlight.update()

    document.save(output_path)
    messagebox.showinfo("Completed", "The operation is complete. Check the output file.")

root = tk.Tk()
root.title("PDF Highlighting Tool")

tk.Label(root, text="PDF Input:").grid(row=0, column=0, padx=10, pady=5)
entry_input_path = tk.Entry(root, width=50)
entry_input_path.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Open", command=open_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Save Location:").grid(row=1, column=0, padx=10, pady=5)
entry_save_location = tk.Entry(root, width=50)
entry_save_location.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Choose Location", command=choose_save_location).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Output Filename:").grid(row=2, column=0, padx=10, pady=5)
entry_output_filename = tk.Entry(root, width=50)
entry_output_filename.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Column Name:").grid(row=3, column=0, padx=10, pady=5)
column_name_entry = tk.Entry(root, width=50)
column_name_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Value to be Coloured:").grid(row=4, column=0, padx=10, pady=5)
highlight_value_entry = tk.Entry(root, width=50)
highlight_value_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Painting Colour (RGB):").grid(row=5, column=0, padx=10, pady=5)
entry_color = tk.Entry(root, width=50)
entry_color.grid(row=5, column=1, padx=10, pady=5)
entry_color.insert(0, "255,0,0")

tk.Button(root, text="Select Colour", command=choose_color).grid(row=5, column=2, padx=10, pady=5)

tk.Button(root, text="Highlight PDF", command=highlight_pdf).grid(row=6, columnspan=3, pady=10)

root.mainloop()
