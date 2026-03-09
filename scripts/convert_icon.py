"""
Icon Conversion Utility
Converts PNG to ICO format for Windows EXE icons
"""
from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path, sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]):
    """Convert PNG to ICO with multiple sizes"""
    try:
        img = Image.open(png_path)
        
        # Convert RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create list of resized images
        icon_sizes = []
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icon_sizes.append(resized)
        
        # Save as ICO
        icon_sizes[0].save(ico_path, format='ICO', sizes=[(s[0], s[1]) for s in sizes])
        print(f"✓ Successfully created {ico_path}")
        return True
    except Exception as e:
        print(f"✗ Error converting icon: {e}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    png_file = os.path.join(project_root, "icon", "logo_pdf.png")
    ico_file = os.path.join(project_root, "icon", "logo_pdf.ico")
    
    if not os.path.exists(png_file):
        print(f"✗ PNG file not found: {png_file}")
        exit(1)
    
    print(f"Converting {png_file} to {ico_file}...")
    if convert_png_to_ico(png_file, ico_file):
        print(f"✓ Icon ready for use in EXE build")
    else:
        exit(1)
