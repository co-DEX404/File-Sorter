import tkinter as tk
import os
import shutil
from tkinter import filedialog, messagebox

window = tk.Tk()
window.config(bg="#092328")

location = tk.StringVar()

status = tk.StringVar()

summary_text = tk.StringVar()

def main():

    window.title("File Sorting Program")
    window.geometry("500x500")

    main_frame = tk.Frame(window,bg="#092328")
    main_frame.pack(pady=25)

    summary_frame = tk.Frame(window, bg="#092328")
    summary_frame.pack(padx=20, pady=10)

    title_header = tk.Label(main_frame, 
                            text="File Sorting", 
                            font=("Arial Bold",20),
                            bg="#092328",
                            fg="#8BBB92")
    title_header.pack(pady=10)

    browse_button = create_button(main_frame, "Browse Folder", browse_clicked)

    browsed_location = tk.Entry(main_frame, 
                                textvariable=location,
                                state="readonly")
    browsed_location.pack(pady=5)

    sort_button = create_button(main_frame, "Sort Folder", sort_clicked)

    clear_button = create_button(main_frame, "Clear", clear_clicked)

    status_label = tk.Label(main_frame, textvariable=status, bg="#092328", fg="#8BBB92", font=("Arial Bold", 10))
    status_label.pack()

    status.set("Ready")

    summary_header = tk.Label(summary_frame,
                              text="Sorting Summary",
                              font=("Arial Bold", 20),
                              bg="#092328",
                              fg="#8BBB92",)
    summary_header.pack()

    summary_label = tk.Label(summary_frame, textvariable=summary_text, fg="#8BBB92", bg="#092328", font=("Arial", 10))
    summary_label.pack()

    window.mainloop()

def button_enter(event):

    event.widget.config(bg="#12544F", fg="#8BBB92")

def button_leave(event):

    event.widget.config(bg="#092328", fg="#8BBB92")

def browse_clicked():

    selected_location = filedialog.askdirectory()
    location.set(selected_location)

    if selected_location == "":
        status.set("Folder selection cancelled.")
    else:
        status.set("Folder Selected.")

def sort_files(selected_location):

    failed_folders = []

    failed_files = []

    extensions = {}

    count, skip = 0, 0

    for file in os.listdir(selected_location):
    
            if os.path.isfile(os.path.join(selected_location, file)):
    
                extension = os.path.splitext(file)[1]
    
                extension = extension.lstrip(".").upper()
    
                if extension == "":            
                    extension = "NO EXTENSION"
    
                if not os.path.exists(os.path.join(selected_location, extension)):
    
                    try:
                        os.mkdir(os.path.join(selected_location, extension))
                    except:
                        failed_folders.append(extension)
                        continue
    
                file_source = os.path.join(selected_location, file)
                file_destination = os.path.join(selected_location, extension, file)
    
                if not os.path.exists(file_destination):
    
                    try:
                        shutil.move(file_source, file_destination)
    
                        count += 1
    
                        if extension not in extensions:
                            extensions[extension] = 1 
                        else:
                            extensions[extension] += 1
    
                    except:
                        failed_files.append(file)
                        continue
    
                else:
                    skip += 1

    return count, skip, extensions, failed_folders, failed_files

def sort_clicked():

    selected_location = location.get()

    if selected_location == "":
        messagebox.showwarning("File Sorter", "Please select a folder first.")
        return

    confirmation = messagebox.askyesno("File Sorter", "Are you sure you want to sort this folder? \n" 
    "This will permanently organize files in this folder. \n"
    "This action cannot be undone.")

    if not confirmation:
        status.set("Sorting cancelled.")
        return

    status.set("Sorting files...")

    count, skip, extensions, failed_folders, failed_files = sort_files(selected_location)

    summary = generate_summary(extensions, failed_folders, failed_files)

    summary_text.set(summary)

    show_result(count, skip, failed_folders, failed_files)



def generate_summary(extensions, failed_folders, failed_files):

    summary = ""
    
    for extension, amount in extensions.items():
        summary += f"{extension}: {amount}\n"

    summary += f"Failed Folders : {len(failed_folders)}\n"
    summary += f"Failed Files : {len(failed_files)}"

    return summary

def show_result(count, skip, failed_folders, failed_files):
        
    if count == 0 and skip == 0 and len(failed_folders) == 0 and len(failed_files) == 0:
        messagebox.showwarning("File Sorter", "No files found to sort.")
        status.set("No files sorted.")
    elif count == 0 and skip == 0 and (len(failed_folders) > 0 or len(failed_files) > 0):
        messagebox.showwarning("File Sorter", f"{count} files sorted. \n {skip} files are skipped. \n {len(failed_folders)} failed folders. \n {len(failed_files)} failed files")
        status.set(f"{count} files sorted successfully. {skip} files are skipped. Sorting failed. {len(failed_folders)} folders and {len(failed_files)} files could not be processed.")
    elif count == 0 and skip > 0 and (len(failed_folders) > 0 or len(failed_files) > 0) :
        messagebox.showinfo("File Sorter", f"{count} files sorted. \n {skip} files are skipped. \n {len(failed_folders)} failed folders. \n {len(failed_files)} failed files")
        status.set(f"{count} files sorted successfully. {skip} files are skipped. \n {len(failed_folders)} failed folders. \n {len(failed_files)} failed files")
    elif count > 0 and (len(failed_folders) > 0 or len(failed_files) > 0):
        messagebox.showinfo("File Sorter", f"{count} files sorted successfully. \n {skip} files are skipped. \n {len(failed_folders)} failed folders. \n {len(failed_files)} failed files")
        status.set(f"{count} files sorted successfully. \n {skip} files are skipped. \n {len(failed_folders)} failed folders. \n {len(failed_files)} failed files")
    else:
        messagebox.showinfo("File Sorter", f"{count} files sorted successfully. \n {skip} files are skipped.")
        status.set(f"All {count} files sorted successfully.")

def clear_clicked():

    location.set("")

def create_button(parent, text, command):

    button = tk.Button(parent,
                       text=text,
                       command=command,
                       width=15, height=1, 
                       font=("Arial Bold",10),
                       bg="#092328", 
                       fg="#8BBB92",
                       activebackground="#857C73",
                       activeforeground="#CBCF78")

    button.pack(pady=10, padx=10)

    button.bind("<Enter>", button_enter)
    button.bind("<Leave>", button_leave)

    return button
    

main()