# MetaClean

A simple, lightweight, and fast metadata removal tool designed to support multiple file types across Windows, macOS, and Linux.
<img width="790" alt="Screenshot 2025-04-08 at 1 00 35 PM" src="https://github.com/user-attachments/assets/e13a0150-4bf4-4e6c-ace4-90cba7751dc3" />



## Features

- **Cross-Platform Support**: Runs seamlessly on Windows, macOS, and Linux
- **Modern GUI**: Clean, intuitive interface built with Tkinter
- **Batch Processing**: Clean multiple files or entire folders at once
- **Live Console**: Real-time progress tracking and detailed logs
- **Secure Processing**: Files are processed locally with no data transmission
- **Fast Processing**: Leverages FFmpeg for efficient metadata removal

## Supported File Types

### Video Formats
- MP4 (.mp4)
- Matroska (.mkv)
- AVI (.avi)
- QuickTime (.mov)
- Flash Video (.flv)
- WebM (.webm)

### Image Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- Bitmap (.bmp)
- TIFF (.tiff)

## Requirements

- Python 3.6+
- FFmpeg (automatically installed for Windows & macOS users)

## Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/MetaClean.git
cd MetaClean
```

2. **Install Dependencies**
```bash
python setup.py
```

## Usage

1. **Launch the Application**
```bash
python metaclean.py
```

2. **Select Files**
   - Use "SELECT FILE" for single file processing
   - Use "SELECT FOLDER" for batch processing
   - Click "CLEAN" to begin metadata removal
   - Monitor progress in the console (toggle with console button)

## How It Works

MetaClean utilizes FFmpeg to safely remove metadata while preserving file content through:
1. Creating a temporary working copy
2. Stripping all metadata using FFmpeg
3. Replacing the original with the cleaned version
4. Automatic cleanup of temporary files


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add NewFeature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [RPxGoon]
