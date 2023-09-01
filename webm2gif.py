# refer to https://gist.github.com/Potherca/18423260e2c9a4324c9ecb0c0a284066
#inputfile='/path/to/file.webm';
#outputfile="$(basename "${inputfile%.*}")";
#ffmpeg -i "${inputfile}" -pix_fmt rgb8 "${outputfile}.gif" \
#    && gifsicle --optimize=3 --output "${outputfile}-optimized.gif" --resize-height 600 "${outputfile}.gif"

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import ffmpeg
from tkinter import ttk
import subprocess

VALID_EXTENSIONS = {".webp", ".webm"}

def open_gif_folder():
    folder_path = os.path.join(label_source_value.cget("text"), "gif")
    print("gif_file_path_var:",folder_path)
    try:
        os.system(f'start, {folder_path}')
    except FileNotFoundError:
        print(f"Error: Folder not found: {folder_path}")

def convert_command(input_filename):
    if not os.path.exists(input_filename):
        return "File does not exist"

    input_dir = os.path.dirname(input_filename)
    gif_dir = os.path.join(input_dir, "gif")
    
    if not os.path.exists(gif_dir):
        os.makedirs(gif_dir)

    output_filename = os.path.join(gif_dir, os.path.splitext(os.path.basename(input_filename))[0] + ".gif")

    if not input_filename.endswith(".gif") and not input_filename.endswith(".GIF"):
        try:
            stream = ffmpeg.input(input_filename)
            stream = ffmpeg.output(stream, output_filename, pix_fmt='rgb8')
            stream.run(overwrite_output=True)

            if checkbox_var.get() == 1:
                gifsiclecommand = f"gifsicle --optimize=3 --output \"{output_filename}\" --resize-height 100 \"{output_filename}\""
                result = os.system(gifsiclecommand)

            #return f"Success: Converted {input_filename} to {output_filename}"
            return f"Success: {os.path.splitext(os.path.basename(input_filename))[0] + '.gif'}"
        except ffmpeg.Error as e:
            return f"Failed: {e}"

def open_file_dialog(label_widget):
    file_path = filedialog.askdirectory()
    if file_path:
        label_widget.config(text=file_path)

def start_convert():
    input_folder = label_source_value.cget("text")
    if not input_folder:
        messagebox.showinfo("Msg", "Select a folder!")
        return
    progressbar["value"] = 0
    progressbar["maximum"] = 100

    total_files = 0
    completed_files = 0

    for dirpath, _, input_filenames in os.walk(input_folder):
        for input_filename in input_filenames:
            if os.path.splitext(input_filename)[1].lower() in VALID_EXTENSIONS:
                total_files += 1

    for dirpath, _, input_filenames in os.walk(input_folder):
        for input_filename in input_filenames:
            if os.path.splitext(input_filename)[1].lower() in VALID_EXTENSIONS:
                input_filepath = os.path.join(label_source_value.cget("text"), input_filename)
                result = convert_command(input_filepath)
                formatted_result = f"{result}\n"
                text_result.insert("1.0", formatted_result)
                text_result.tag_add("result", "1.0", "1.end")
                text_result.tag_config("result", foreground="green")
                completed_files += 1
                progress = int((completed_files / total_files) * 100)
                progressbar["value"] = progress
                root.update_idletasks()
    open_gif_folder_button.config(state=tk.NORMAL)

def clean_all():
    text_result.delete("1.0", "end")
    progressbar["value"] = 0
    progressbar["maximum"] = 100
    open_gif_folder_button.config(state=tk.DISABLED)


root = tk.Tk()
root.geometry("470x320")
root.title("Webm2Gif")


checkbox_var = tk.IntVar()
checkbox_sicle = tk.Checkbutton(variable=checkbox_var, text="resize-height 100")
checkbox_sicle.grid(row=1, column=2)

label_source_text = tk.Label(text="Source")
label_source_text.grid(row=1, column=1)

label_source_value = tk.Label(text="")
label_source_value.grid(row=2, column=1, columnspan=3)

select_file_button_source = tk.Button(root, text="Select folder", command=lambda: open_file_dialog(label_source_value))
select_file_button_source.grid(row=1, column=3)

text_result = tk.Text(width=68, height=15)
text_result.grid(row=4, column=1, columnspan=3)

start_button = tk.Button(root, text="Start", command=start_convert)
start_button.grid(row=5, column=1)

clean_button = tk.Button(root, text="Clean", command=clean_all)
clean_button.grid(row=5, column=2)

open_gif_folder_button = tk.Button(root, text="Open GIF folder", command=open_gif_folder,state=tk.DISABLED)
open_gif_folder_button.grid(row=5, column=3)
progressbar = ttk.Progressbar(root, length=400, mode="determinate")
progressbar.grid(row=3, column=1, columnspan=3, pady=10)

# 添加一个tag，用于设置文本颜色
text_result.tag_configure("result", foreground="green")

root.mainloop()
