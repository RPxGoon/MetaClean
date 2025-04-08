import os
import ffmpeg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import platform
import subprocess
from PIL import Image, ImageTk
import time

class MetadataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MetaClean")
        self.root.geometry("800x600")  # Smaller window size
        self.root.config(bg="#121212")  # Modern dark theme

        # Theme colors - Modern Professional Theme
        self.bg_color = "#121212"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#ff0033"  # Changed to match website's red
        self.secondary_accent = "#9d00ff"  # Changed to purple accent
        self.button_bg = "#1e1e1e"
        self.button_hover = "#2d2d2d"
        self.button_fg = "#ffffff"
        self.success_color = "#00ff00"  # Matrix green
        self.error_color = "#ff0033"  # Matching red

        # About content
        self.about_info = {
            "version": "1.0.0",
            "description": """MetaClean is a powerful metadata removal tool designed for privacy-conscious users: 
            Completely stripping hidden metadata deigned to fingerprint/track you and your files, ensuring original quality preservation.""",
            "supported_formats": {
                "Video": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".webm"],
                "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
            }
        }

        # Configure styles
        self.setup_styles()

        # Main container with modern padding
        self.main_container = tk.Frame(root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

        # Setup UI components in correct order
        self.setup_status_bar()  # Move this first
        self.setup_title_section()
        self.setup_buttons()
        self.setup_progress_bar()
        self.setup_console()

        # Variables
        self.selected_files = []
        self.processing = False
        self.about_window = None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Custom.TButton",
            font=("Fira Code", 11),  # Smaller font
            padding=(15, 10),  # More compact padding
            foreground=self.button_fg,
            background=self.button_bg,
            borderwidth=0,
            focuscolor=self.accent_color,
        )
        
        style.configure(
            "About.TButton",
            font=("Helvetica", 10),
            padding=(15, 8),
            background=self.button_bg,
        )

        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.button_bg,
            background="linear-gradient(90deg, #ff0033, #9d00ff)",  # Gradient effect
            thickness=8,
            borderwidth=0,
        )

        style.map("Custom.TButton",
            background=[("active", self.button_hover)],
            foreground=[("active", self.fg_color)]
        )

        # Add special style for Clean button
        style.configure(
            "Clean.TButton",
            font=("Fira Code", 12, "bold"),  # Slightly larger & bold
            padding=(15, 14),  # Taller button
            foreground=self.accent_color,  # Red text
            background=self.button_bg,
            borderwidth=2,  # More prominent border
            focuscolor=self.accent_color,
        )

        # Add hover effect for Clean button
        style.map("Clean.TButton",
            background=[("active", self.accent_color)],
            foreground=[("active", "#ffffff")]
        )

    def show_about(self):
        if self.about_window is None or not tk.Toplevel.winfo_exists(self.about_window):
            self.about_window = tk.Toplevel(self.root)
            self.about_window.title("About MetaClean")
            self.about_window.geometry("500x600")
            self.about_window.config(bg=self.bg_color)
            self.about_window.transient(self.root)
            
            about_frame = tk.Frame(self.about_window, bg=self.bg_color, padx=25, pady=20)
            about_frame.pack(fill=tk.BOTH, expand=True)

            title = tk.Label(
                about_frame,
                text="MetaClean",
                font=("Helvetica", 24, "bold"),
                fg=self.accent_color,
                bg=self.bg_color
            )
            title.pack(pady=(0, 5))

            version = tk.Label(
                about_frame,
                text=f"Version {self.about_info['version']}",
                font=("Helvetica", 10),
                fg=self.fg_color,
                bg=self.bg_color
            )
            version.pack(pady=(0, 20))

            desc = tk.Label(
                about_frame,
                text=self.about_info['description'],
                font=("Helvetica", 12),
                fg=self.fg_color,
                bg=self.bg_color,
                wraplength=400,
                justify=tk.CENTER
            )
            desc.pack(pady=(0, 30))

            formats_frame = tk.Frame(about_frame, bg=self.bg_color)
            formats_frame.pack(fill=tk.X, pady=(0, 20))

            tk.Label(
                formats_frame,
                text="Supported Formats",
                font=("Helvetica", 14, "bold"),
                fg=self.accent_color,
                bg=self.bg_color
            ).pack(pady=(0, 10))

            for category, formats in self.about_info['supported_formats'].items():
                tk.Label(
                    formats_frame,
                    text=f"{category}:",
                    font=("Helvetica", 12, "bold"),
                    fg=self.secondary_accent,
                    bg=self.bg_color
                ).pack(anchor='w')
                
                tk.Label(
                    formats_frame,
                    text=", ".join(formats),
                    font=("Helvetica", 11),
                    fg=self.fg_color,
                    bg=self.bg_color
                ).pack(anchor='w', pady=(0, 10))

    def setup_title_section(self):
        title_frame = tk.Frame(self.main_container, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(10, 30))  # Reduced padding

        title_center_frame = tk.Frame(title_frame, bg=self.bg_color)
        title_center_frame.pack(expand=True, fill=tk.X)

        self.title_label = tk.Label(
            title_center_frame,
            text="MetaClean",
            font=("Fira Code", 36, "bold"),  # Slightly smaller
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(expand=True, pady=(5, 10))  # Reduced padding

        self.description_label = tk.Label(
            title_center_frame,
            text="Simple & secure metadata removal",
            font=("Fira Code", 12),  # Smaller font
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.description_label.pack(pady=(0, 15))

    def setup_buttons(self):
        self.buttons_frame = tk.Frame(
            self.main_container,
            bg=self.bg_color,
            padx=30,
            pady=20
        )
        self.buttons_frame.pack(fill=tk.X, padx=40)

        # Create a container for the file selection buttons to be side by side
        file_buttons_frame = tk.Frame(self.buttons_frame, bg=self.bg_color)
        file_buttons_frame.pack(fill=tk.X)

        # Left side - Select File button
        self.select_file_button = ttk.Button(
            file_buttons_frame,
            text="SELECT FILE",
            style="Custom.TButton",
            command=self.select_file
        )
        self.select_file_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Right side - Select Folder button
        self.select_folder_button = ttk.Button(
            file_buttons_frame,
            text="SELECT FOLDER",
            style="Custom.TButton",
            command=self.select_folder
        )
        self.select_folder_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # Clean button in its own frame with increased spacing
        clean_frame = tk.Frame(self.buttons_frame, bg=self.bg_color)
        clean_frame.pack(fill=tk.X, pady=(35, 0))  # More space above

        self.start_button = ttk.Button(
            clean_frame,
            text="CLEAN",
            style="Clean.TButton",
            command=self.start_cleaning,
            state=tk.DISABLED
        )
        self.start_button.pack(fill=tk.X, ipady=2)

    def setup_progress_bar(self):
        self.progress_frame = tk.Frame(self.buttons_frame, bg=self.bg_color)
        self.progress_frame.pack(fill=tk.X, pady=(20, 0))

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"] = 0

    def setup_console(self):
        self.console_frame = tk.Frame(self.root, bg=self.bg_color)
        self.console_text = tk.Text(
            self.console_frame,
            height=8,  # Reduced height
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Fira Code", 10),
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            padx=12,
            pady=12
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=25, pady=8)
        self.console_visible = False

    def setup_status_bar(self):
        self.status_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(30, 10))

        status_left = tk.Frame(self.status_frame, bg=self.bg_color)
        status_left.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_label = tk.Label(
            status_left,
            text="Ready",
            font=("Fira Code", 12),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        status_right = tk.Frame(self.status_frame, bg=self.bg_color)
        status_right.pack(side=tk.RIGHT, padx=10)

        self.about_button = ttk.Button(
            status_right,
            text="About",
            style="Custom.TButton",
            command=self.show_about
        )
        self.about_button.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.toggle_console_button = ttk.Button(
            status_right,
            text="▲ Console",
            style="Custom.TButton",
            command=self.toggle_console
        )
        self.toggle_console_button.pack(side=tk.RIGHT)

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

    def start_cleaning(self):
        if not self.selected_files:
            self.log_to_console("Error: No files selected!", color=self.error_color)
            return

        if not self.processing:
            self.processing = True
            self.start_button.config(state=tk.DISABLED)
            self.select_file_button.config(state=tk.DISABLED)
            self.select_folder_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Cleaning in progress...")
            
            threading.Thread(target=self.clean_metadata, daemon=True).start()

    def clean_file(self, file):
        temp_file = f"{file}.temp"
        try:
            ext = os.path.splitext(file)[1].lower()
            
            if ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']:
                stream = ffmpeg.input(file)
                output_args = {
                    'map_metadata': -1,
                    'map_chapters': -1,
                    'fflags': '+bitexact',
                    'acodec': 'copy',
                    'vcodec': 'copy'
                }
                
                     # Format-specific handling while keeping working formats unchanged
                if ext == '.mkv':
                    output_args['f'] = 'matroska'
                elif ext == '.mp4':
                    output_args['f'] = 'mp4'
                    output_args['movflags'] = '+faststart'
                elif ext == '.mov':
                    output_args['f'] = 'mov'
                    output_args['movflags'] = '+faststart'  # QuickTime needs faststart too
                elif ext == '.avi':
                    output_args['f'] = 'avi'
                    output_args['fflags'] += '+genpts'  # Ensure proper timestamps
                elif ext == '.flv':
                    output_args['f'] = 'flv'
                    output_args['flv_metadata'] = ''  # Clear FLV specific metadata
                elif ext == '.webm':
                    output_args['f'] = 'webm'
                    output_args['metadata'] = ''  # Clear WebM metadata
                
                stream = ffmpeg.output(stream, temp_file, **output_args)
                stream = stream.overwrite_output()
                ffmpeg.run(stream, capture_stderr=True)
            
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                format_name = 'jpeg' if ext == '.jpg' else ext[1:]
                
                try:
                    with Image.open(file) as img:
                        cleaned_img = Image.new(img.mode, img.size)
                        cleaned_img.putdata(list(img.getdata()))
                        cleaned_img.save(temp_file, format=format_name)
                except Exception:
                    stream = ffmpeg.input(file)
                    stream = ffmpeg.output(stream, temp_file,
                                        map_metadata=-1,
                                        fflags='+bitexact')
                    stream = stream.overwrite_output()
                    ffmpeg.run(stream, capture_stderr=True)

            if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                raise Exception("Failed to create valid output file")
            
            os.replace(temp_file, file)
            
        except ffmpeg.Error as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            error_message = e.stderr.decode() if e.stderr else 'Unknown FFmpeg error'
            raise Exception(f"FFmpeg error: {error_message}")
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise Exception(f"Failed to clean metadata: {str(e)}")

    def clean_metadata(self):
        total_files = len(self.selected_files)
        successful = 0
        failed = 0

        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_bar["value"] = 0

        self.log_to_console(f"Starting metadata cleaning for {total_files} files...")
        
        for index, file in enumerate(self.selected_files):
            try:
                self.log_to_console(f"Processing: {os.path.basename(file)}")
                
                self.clean_file(file)
                successful += 1
                
                progress = ((index + 1) / total_files) * 100
                self.progress_bar["value"] = progress
                
                success_msg = f"Successfully cleaned: {os.path.basename(file)}"
                self.log_to_console(success_msg, color=self.success_color)
                
            except Exception as e:
                failed += 1
                self.log_to_console(f"Error processing {os.path.basename(file)}: {str(e)}", 
                                  color=self.error_color)

        self.processing = False
        
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.select_file_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.select_folder_button.config(state=tk.NORMAL))

        self.root.after(1000, self.progress_bar.pack_forget)
        self.root.after(0, self.update_status_complete, successful, failed, total_files)

    def update_status_complete(self, successful, failed, total):
        status = f"Completed: {successful} succeeded, {failed} failed out of {total} files"
        self.status_label.config(text=status)
        self.log_to_console(status)

    def log_to_console(self, message, color=None):
        self.console_text.config(state=tk.NORMAL)
        tag = f"color_{time.time()}"
        self.console_text.insert(tk.END, f"[*] {message}\n", tag)
        if color:
            self.console_text.tag_configure(tag, foreground=color)
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)

    def toggle_console(self):
        if self.console_visible:
            self.console_frame.pack_forget()
            self.toggle_console_button.configure(text="▲ Console")
            self.console_visible = False
        else:
            self.console_frame.pack(side=tk.BOTTOM, fill=tk.X, before=self.status_frame)
            self.toggle_console_button.configure(text="▼ Console")
            self.console_visible = True

if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataCleanerApp(root)
    root.mainloop()