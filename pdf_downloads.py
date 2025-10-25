"""
PDF Downloader - A professional PDF downloading tool
Created by Srijan
Srijanxi Technologies

Features:
- Concurrent downloads with configurable thread pool
- Network speed monitoring
- Pause/Resume functionality
- Recursive directory scanning
- Cross-platform support (Windows, Linux, macOS)
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Global variables
visited_urls = set()
pdf_links = []
is_downloading = False
is_paused = False
downloaded_count = 0
total_bytes_downloaded = 0
download_start_time = 0
stats_lock = Lock()


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def find_pdfs(url, depth=0, max_depth=2, log_callback=None):
    """Recursively find PDF links in directories"""
    if depth > max_depth or url in visited_urls:
        return
    
    visited_urls.add(url)
    if log_callback:
        log_callback(f"Scanning: {url}\n")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Skip parent directory links
            if href == "../":
                continue
            
            # Ensure href is a string
            if not isinstance(href, str):
                continue
                
            full_url = urljoin(url, href)
            
            # If it's a PDF, add to list
            if href.lower().endswith(".pdf"):
                pdf_links.append(full_url)
                if log_callback:
                    log_callback(f"Found PDF: {full_url}\n")
            # If it's a directory (ends with /), recursively search
            elif href.endswith("/") and depth < max_depth:
                find_pdfs(full_url, depth + 1, max_depth, log_callback)
    
    except Exception as e:
        if log_callback:
            log_callback(f"Error scanning {url}: {e}\n")

def download_single_pdf(pdf_url, output_folder, log_callback=None):
    """Download a single PDF file with progress tracking"""
    global total_bytes_downloaded
    
    # Wait if paused
    while is_paused and is_downloading:
        time.sleep(0.1)
    
    if not is_downloading:
        return None
    
    # Handle duplicate filenames
    base_filename = pdf_url.split("/")[-1]
    filename = os.path.join(output_folder, base_filename)
    
    # If file exists, add a number suffix
    if os.path.exists(filename):
        name, ext = os.path.splitext(base_filename)
        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(output_folder, f"{name}_{counter}{ext}")
            counter += 1
    
    try:
        response = requests.get(pdf_url, timeout=30, stream=True)
        response.raise_for_status()
        
        file_size = int(response.headers.get('content-length', 0))
        
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                # Check pause/stop
                while is_paused and is_downloading:
                    time.sleep(0.1)
                
                if not is_downloading:
                    # Clean up partial file
                    try:
                        os.remove(filename)
                    except:
                        pass
                    return None
                
                if chunk:
                    f.write(chunk)
                    with stats_lock:
                        total_bytes_downloaded += len(chunk)
        
        return pdf_url
    except Exception as e:
        # Clean up partial file on error
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass
        if log_callback:
            log_callback(f"Error downloading {pdf_url}: {e}\n")
        return None


def download_pdfs(base_url, output_folder, max_depth, max_workers=3, log_callback=None, progress_callback=None, speed_callback=None):
    """Main download function with concurrent downloads"""
    global is_downloading, is_paused, downloaded_count, total_bytes_downloaded, download_start_time
    
    # Reset globals
    visited_urls.clear()
    pdf_links.clear()
    is_downloading = True
    is_paused = False
    downloaded_count = 0
    total_bytes_downloaded = 0
    download_start_time = time.time()
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    if log_callback:
        log_callback(f"Starting PDF search from: {base_url}\n")
    
    # Find all PDFs recursively
    find_pdfs(base_url, max_depth=max_depth, log_callback=log_callback)
    
    if len(pdf_links) == 0:
        if log_callback:
            log_callback(f"\nNo PDFs found at {base_url}\n")
        is_downloading = False
        is_paused = False
        return
    
    if log_callback:
        log_callback(f"\nFound {len(pdf_links)} PDFs. Starting downloads...\n\n")
    
    # Download all PDFs with concurrent workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_single_pdf, pdf_url, output_folder, log_callback): pdf_url 
                         for pdf_url in pdf_links}
        
        for future in as_completed(future_to_url):
            if not is_downloading:
                executor.shutdown(wait=False, cancel_futures=True)
                if log_callback:
                    log_callback("\nDownload cancelled by user.\n")
                break
            
            pdf_url = future_to_url[future]
            result = future.result()
            
            if result:
                with stats_lock:
                    downloaded_count += 1
                
                if log_callback:
                    log_callback(f"Downloaded ({downloaded_count}/{len(pdf_links)}): {pdf_url}\n")
                
                if progress_callback:
                    progress_callback(downloaded_count, len(pdf_links))
                
                # Calculate and report speed
                if speed_callback:
                    elapsed = time.time() - download_start_time
                    if elapsed > 0:
                        speed_mbps = (total_bytes_downloaded / (1024 * 1024)) / elapsed
                        speed_callback(speed_mbps)
    
    is_downloading = False
    is_paused = False
    
    if log_callback:
        elapsed = time.time() - download_start_time
        total_mb = total_bytes_downloaded / (1024 * 1024)
        avg_speed = total_mb / elapsed if elapsed > 0 else 0
        log_callback(f"\nCompleted! Downloaded {downloaded_count} PDFs ({total_mb:.2f} MB) to '{output_folder}' folder.\n")
        log_callback(f"Average speed: {avg_speed:.2f} MB/s\n")

class PDFDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Downloader - Srijanxi Technologies")
        self.root.geometry("800x600")
        
        # Set window icon
        try:
            icon_path = get_resource_path(os.path.join("icon", "logo_pdf.png"))
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # URL Frame
        url_frame = ttk.LabelFrame(root, text="URL Settings", padding=10)
        url_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(url_frame, text="Website URL:").grid(row=0, column=0, sticky="w", pady=5)
        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.insert(0, "Enter website URL here...")
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Output Folder Frame
        folder_frame = ttk.LabelFrame(root, text="Output Settings", padding=10)
        folder_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(folder_frame, text="Output Folder:").grid(row=0, column=0, sticky="w", pady=5)
        self.folder_entry = ttk.Entry(folder_frame, width=50)
        self.folder_entry.insert(0, "pdf_downloads")
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5)
        
        ttk.Label(folder_frame, text="Max Depth:").grid(row=1, column=0, sticky="w", pady=5)
        self.depth_spinbox = ttk.Spinbox(folder_frame, from_=0, to=10, width=10)
        self.depth_spinbox.set(2)
        self.depth_spinbox.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(folder_frame, text="Concurrent Downloads:").grid(row=2, column=0, sticky="w", pady=5)
        self.workers_spinbox = ttk.Spinbox(folder_frame, from_=1, to=10, width=10)
        self.workers_spinbox.set(3)
        self.workers_spinbox.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Buttons Frame
        button_frame = ttk.Frame(root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="Start Download", command=self.start_download)
        self.start_button.pack(side="left", padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_download, state="disabled")
        self.pause_button.pack(side="left", padx=5)
        
        self.resume_button = ttk.Button(button_frame, text="Resume", command=self.resume_download, state="disabled")
        self.resume_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_download, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=5)
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(root, text="Progress", padding=10)
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill="x", pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready")
        self.progress_label.pack()
        
        self.speed_label = ttk.Label(progress_frame, text="Speed: 0.00 MB/s")
        self.speed_label.pack()
        
        # Log Frame
        log_frame = ttk.LabelFrame(root, text="Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
        # Footer with credits
        footer_frame = ttk.Frame(root)
        footer_frame.pack(fill="x", padx=10, pady=5)
        
        credits_label = ttk.Label(footer_frame, text="Created by Srijan | Srijanxi Technologies", 
                                  font=("Arial", 8), foreground="gray")
        credits_label.pack()
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.root.update_idletasks()
    
    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"Downloaded {current} of {total} PDFs")
        self.root.update_idletasks()
    
    def update_speed(self, speed_mbps):
        self.speed_label.config(text=f"Speed: {speed_mbps:.2f} MB/s")
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
    
    def start_download(self):
        url = self.url_entry.get().strip()
        folder = self.folder_entry.get().strip()
        
        # Clear placeholder text
        if url == "Enter website URL here...":
            url = ""
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
        
        # Validate URL format
        if not url.startswith(("http://", "https://")):
            messagebox.showerror("Error", "URL must start with http:// or https://")
            return
        
        if not folder:
            messagebox.showerror("Error", "Please enter an output folder")
            return
        
        try:
            max_depth = int(self.depth_spinbox.get())
        except:
            messagebox.showerror("Error", "Invalid depth value")
            return
        
        try:
            max_workers = int(self.workers_spinbox.get())
            if max_workers < 1 or max_workers > 10:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid concurrent downloads value (1-10)")
            return
        
        # Disable start button, enable pause/stop buttons
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.progress_bar['value'] = 0
        self.progress_label.config(text="Starting...")
        self.speed_label.config(text="Speed: 0.00 MB/s")
        
        # Start download in a separate thread
        thread = threading.Thread(
            target=download_pdfs,
            args=(url, folder, max_depth, max_workers, self.log, self.update_progress, self.update_speed),
            daemon=True
        )
        thread.start()
        
        # Monitor thread completion
        self.monitor_thread(thread)
    
    def monitor_thread(self, thread):
        if thread.is_alive():
            self.root.after(100, lambda: self.monitor_thread(thread))
        else:
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.resume_button.config(state="disabled")
            self.stop_button.config(state="disabled")
            if not is_downloading:
                self.progress_label.config(text="Completed")
    
    def pause_download(self):
        global is_paused
        is_paused = True
        self.log("\n--- Download paused ---\n")
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")
        self.progress_label.config(text="Paused")
    
    def resume_download(self):
        global is_paused
        is_paused = False
        self.log("\n--- Download resumed ---\n")
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.progress_label.config(text="Downloading...")
    
    def stop_download(self):
        global is_downloading, is_paused
        is_downloading = False
        is_paused = False
        self.log("\n--- Stopping download... ---\n")
        self.stop_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="disabled")

def main():
    root = tk.Tk()
    app = PDFDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

