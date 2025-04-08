import os
import ffmpeg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import platform
import subprocess

class MetadataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MetaClean")
        self.root.geometry("800x600")
        self.root.config(bg="#1a1a2e")

        # Theme colors from website
        self.bg_color = "#1a1a2e"
        self.fg_color = "#ffffff"
        self.accent_color = "#ff0033"
        self.secondary_accent = "#9d00ff"
        self.button_bg = "#000000"
        self.button_fg = "#ffffff"

        # Configure button style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 12, "bold"),
            padding=12,
            foreground=self.button_fg,
            background=self.button_bg,
            borderwidth=1,
            bordercolor=self.accent_color,
            borderradius=50
        )
        
        # Hover effects
        style.map("Custom.TButton",
            background=[("active", self.accent_color)],
            foreground=[("active", "#ffffff")]
        )

        # Main container
        self.main_container = tk.Frame(root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title and description
        self.title_label = tk.Label(
            self.main_container,
            text="MetaClean",
            font=("Helvetica", 36, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(pady=(0, 5))

        self.description_label = tk.Label(
            self.main_container,
            text="Simple & secure metadata removal",
            font=("Helvetica", 14),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.description_label.pack(pady=(0, 30))

        # Buttons container with gradient border
        self.buttons_frame = tk.Frame(
            self.main_container,
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        self.buttons_frame.pack(fill=tk.X, padx=50)

        # File selection buttons
        self.select_file_button = ttk.Button(
            self.buttons_frame,
            text="SELECT FILE",
            style="Custom.TButton",
            command=self.select_file
        )
        self.select_file_button.pack(fill=tk.X, pady=(0, 10))

        self.select_folder_button = ttk.Button(
            self.buttons_frame,
            text="SELECT FOLDER",
            style="Custom.TButton",
            command=self.select_folder
        )
        self.select_folder_button.pack(fill=tk.X, pady=(0, 10))

        self.start_button = ttk.Button(
            self.buttons_frame,
            text="CLEAN",
            style="Custom.TButton",
            state=tk.DISABLED,
            command=self.start_cleaning
        )
        self.start_button.pack(fill=tk.X, pady=(0, 10))

        # Console
        self.console_frame = tk.Frame(self.root, bg=self.bg_color)
        self.console_text = tk.Text(
            self.console_frame,
            height=8,
            bg="#000000",
            fg=self.accent_color,
            font=("Helvetica", 10),
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.console_visible = False

        # Status bar
        self.status_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))

        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=("Helvetica", 12),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.LEFT)

        self.toggle_console_button = ttk.Button(
            self.status_frame,
            text="▲ Console",
            style="Custom.TButton",
            command=self.toggle_console
        )
        self.toggle_console_button.pack(side=tk.RIGHT)

        # Variables
        self.selected_files = []

    def toggle_console(self):
        if self.console_visible:
            self.console_frame.pack_forget()
            self.toggle_console_button.configure(text="▲ Console")
            self.console_visible = False
        else:
            self.console_frame.pack(side=tk.BOTTOM, fill=tk.X, before=self.status_frame)
            self.toggle_console_button.configure(text="▼ Console")
            self.console_visible = True

    def select_file(self):
        filetypes = [
            ("All Supported Files", "*.mp4 *.mkv *.avi *.mov *.flv *.webm *.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("Video Files", "*.mp4 *.mkv *.avi *.mov *.flv *.webm"),
            ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
            ("All Files", "*.*")
        ]
        file = filedialog.askopenfilename(filetypes=filetypes)
        if file:
            self.selected_files = [file]
            self.status_label.config(text=f"Selected: {os.path.basename(file)}")
            self.start_button.config(state=tk.NORMAL)
            self.log_to_console(f"File selected: {file}")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_files = []
            valid_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm',
                              '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
            
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(valid_extensions):
                        self.selected_files.append(os.path.join(root, file))
            
            if self.selected_files:
                self.status_label.config(text=f"Selected folder: {os.path.basename(folder)}")
                self.start_button.config(state=tk.NORMAL)
                self.log_to_console(f"Folder selected: {folder}")
                self.log_to_console(f"Found {len(self.selected_files)} files to process")
            else:
                self.status_label.config(text="No supported files found in folder")
                self.log_to_console("No supported files found in the selected folder")

    def log_to_console(self, message):
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, f"[*] {message}\n")
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def start_cleaning(self):
        if not self.selected_files:
            self.log_to_console("Error: No files selected!")
            return

        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Cleaning in progress...")
        threading.Thread(target=self.clean_metadata, daemon=True).start()

    def clean_metadata(self):
        total_files = len(self.selected_files)
        successful = 0
        failed = 0

        self.log_to_console(f"Starting metadata cleaning for {total_files} files...")
        
        for file in self.selected_files:
            try:
                self.log_to_console(f"Processing: {os.path.basename(file)}")
                self.clean_file(file)
                successful += 1
                self.log_to_console(f"Successfully cleaned: {os.path.basename(file)}")
            except Exception as e:
                failed += 1
                self.log_to_console(f"Error processing {os.path.basename(file)}: {str(e)}")

        self.root.after(0, self.update_status_complete, successful, failed, total_files)

    def update_status_complete(self, successful, failed, total):
        self.start_button.config(state=tk.NORMAL)
        status = f"Completed: {successful} succeeded, {failed} failed out of {total} files"
        self.status_label.config(text=status)
        self.log_to_console(status)

    def clean_file(self, file):
        temp_file = f"{file}.temp"
        try:
            ffmpeg.input(file).output(temp_file, map_metadata=-1, c='copy').run(overwrite_output=True, quiet=True)
            os.replace(temp_file, file)
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise Exception(f"Failed to clean metadata: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataCleanerApp(root)
    root.mainloop()