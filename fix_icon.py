from PIL import Image

try:
    img = Image.open('icon-512.png')
    img = img.convert('RGBA')
    img.save('assets/icon.png', 'PNG')
    print("Successfully converted and saved assets/icon.png")
except Exception as e:
    print("Error:", e)
