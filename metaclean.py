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
        self.root.geometry("800x600")
        self.root.config(bg="#121212")  # Modern dark theme

        # Theme colors - Modern Professional Theme
        self.bg_color = "#121212"
        self.fg_color = "#e0e0e0"
        self.accent_color = "#4a90e2"  # Modern blue
        self.secondary_accent = "#2ecc71"  # Fresh green
        self.button_bg = "#1e1e1e"
        self.button_hover = "#2d2d2d"
        self.button_fg = "#ffffff"
        self.success_color = "#2ecc71"
        self.error_color = "#e74c3c"

        # About content
        self.about_info = {
            "version": "1.0.0",
            "description": """MetaClean is a powerful metadata removal tool designed for privacy-conscious users. 
            It completely strips metadata while preserving file quality.""",
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

        # Setup UI components
        self.setup_title_section()
        self.setup_buttons()
        self.setup_progress_bar()
        self.setup_console()
        self.setup_status_bar()

        # Variables
        self.selected_files = []
        self.processing = False
        self.about_window = None

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Modern button style with animations
        style.configure(
            "Custom.TButton",
            font=("Helvetica", 12),
            padding=(20, 12),
            foreground=self.button_fg,
            background=self.button_bg,
            borderwidth=0,
            focuscolor=self.accent_color,
        )
        
        # About button style
        style.configure(
            "About.TButton",
            font=("Helvetica", 10),
            padding=(15, 8),
            background=self.button_bg,
        )

        # Progress bar style
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.button_bg,
            background=self.accent_color,
            thickness=8,
            borderwidth=0,
        )

        # Hover effects
        style.map("Custom.TButton",
            background=[("active", self.button_hover)],
            foreground=[("active", self.fg_color)]
        )

    def show_about(self):
        if self.about_window is None or not tk.Toplevel.winfo_exists(self.about_window):
            self.about_window = tk.Toplevel(self.root)
            self.about_window.title("About MetaClean")
            self.about_window.geometry("500x600")
            self.about_window.config(bg=self.bg_color)
            self.about_window.transient(self.root)
            
            # Add padding
            about_frame = tk.Frame(self.about_window, bg=self.bg_color, padx=25, pady=20)
            about_frame.pack(fill=tk.BOTH, expand=True)

            # Logo/Title
            title = tk.Label(
                about_frame,
                text="MetaClean",
                font=("Helvetica", 24, "bold"),
                fg=self.accent_color,
                bg=self.bg_color
            )
            title.pack(pady=(0, 5))

            # Version
            version = tk.Label(
                about_frame,
                text=f"Version {self.about_info['version']}",
                font=("Helvetica", 10),
                fg=self.fg_color,
                bg=self.bg_color
            )
            version.pack(pady=(0, 20))

            # Description
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

            # Supported Formats
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
        title_frame.pack(fill=tk.X, pady=(0, 20))

        self.title_label = tk.Label(
            title_frame,
            text="MetaClean",
            font=("Helvetica", 36, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.title_label.pack(side=tk.LEFT, pady=(0, 5))

        # About button
        self.about_button = ttk.Button(
            title_frame,
            text="About",
            style="About.TButton",
            command=self.show_about
        )
        self.about_button.pack(side=tk.RIGHT, pady=(15, 0))

        self.description_label = tk.Label(
            self.main_container,
            text="Simple & secure metadata removal",
            font=("Helvetica", 14),
            fg=self.fg_color,
            bg=self.bg_color
        )
        self.description_label.pack(pady=(0, 30))

    def setup_buttons(self):
        self.buttons_frame = tk.Frame(
            self.main_container,
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        self.buttons_frame.pack(fill=tk.X, padx=50)

        # File selection buttons with hover animation
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

    def setup_progress_bar(self):
        self.progress_bar = ttk.Progressbar(
            self.buttons_frame,
            mode='determinate',
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress_bar["maximum"] = 100
        self.progress_bar["value"] = 0

    def setup_console(self):
        self.console_frame = tk.Frame(self.root, bg=self.bg_color)
        self.console_text = tk.Text(
            self.console_frame,
            height=8,
            bg="#1a1a1a",
            fg=self.accent_color,
            font=("Consolas", 10),
            insertbackground=self.accent_color,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.console_visible = False

    def setup_status_bar(self):
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
            
            # Start processing in a separate thread
            threading.Thread(target=self.clean_metadata, daemon=True).start()

    def clean_file(self, file):
        temp_file = f"{file}.temp"
        try:
            ext = os.path.splitext(file)[1].lower()
            
            # Handle video files with complete metadata removal
            if ext in ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm']:
                stream = ffmpeg.input(file)
                output_args = {
                    'map_metadata': -1,  # Remove metadata
                    'map_chapters': -1,  # Remove chapters
                    'fflags': '+bitexact',  # Ensure deterministic output
                    'acodec': 'copy',
                    'vcodec': 'copy'
                }
                
                # Format-specific handling
                if ext == '.mkv':
                    output_args['f'] = 'matroska'
                elif ext == '.mp4':
                    output_args['f'] = 'mp4'
                    output_args['movflags'] = '+faststart'  # Optimize for web playback
                
                stream = ffmpeg.output(stream, temp_file, **output_args)
                stream = stream.overwrite_output()
                ffmpeg.run(stream, capture_stderr=True)
            
            # Handle image files
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
                format_name = 'jpeg' if ext == '.jpg' else ext[1:]
                
                try:
                    with Image.open(file) as img:
                        # Create clean image without metadata
                        cleaned_img = Image.new(img.mode, img.size)
                        cleaned_img.putdata(list(img.getdata()))
                        cleaned_img.save(temp_file, format=format_name)
                except Exception:
                    # Fallback to ffmpeg for images
                    stream = ffmpeg.input(file)
                    stream = ffmpeg.output(stream, temp_file,
                                        map_metadata=-1,
                                        fflags='+bitexact')
                    stream = stream.overwrite_output()
                    ffmpeg.run(stream, capture_stderr=True)

            # Verify output file
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

        # Show and reset progress bar
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        self.progress_bar["value"] = 0

        self.log_to_console(f"Starting metadata cleaning for {total_files} files...")
        
        for index, file in enumerate(self.selected_files):
            try:
                self.log_to_console(f"Processing: {os.path.basename(file)}")
                
                # Process file
                self.clean_file(file)
                successful += 1
                
                # Update progress with smooth animation
                progress = ((index + 1) / total_files) * 100
                self.progress_bar["value"] = progress
                
                # Success message with color
                success_msg = f"Successfully cleaned: {os.path.basename(file)}"
                self.log_to_console(success_msg, color=self.success_color)
                
            except Exception as e:
                failed += 1
                self.log_to_console(f"Error processing {os.path.basename(file)}: {str(e)}", 
                                  color=self.error_color)

        # Reset processing state
        self.processing = False
        
        # Re-enable buttons with animation
        self.root.after(0, lambda: self.start_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.select_file_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.select_folder_button.config(state=tk.NORMAL))

        # Hide progress bar with animation
        self.root.after(1000, self.progress_bar.pack_forget)
        self.root.after(0, self.update_status_complete, successful, failed, total_files)

    def update_status_complete(self, successful, failed, total):
        status = f"Completed: {successful} succeeded, {failed} failed out of {total} files"
        self.status_label.config(text=status)
        self.log_to_console(status)

    def log_to_console(self, message, color=None):
        self.console_text.config(state=tk.NORMAL)
        tag = f"color_{time.time()}"  # Unique tag for each message
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