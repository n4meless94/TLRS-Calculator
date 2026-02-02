#!/usr/bin/env python3
"""Create a simple icon for QSB TLRS Calculator."""

from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Create a 256x256 image with blue background
    size = 256
    img = Image.new('RGBA', (size, size), (54, 96, 146, 255))  # QSB blue color
    draw = ImageDraw.Draw(img)
    
    # Draw a white calendar shape
    margin = 30
    cal_top = 50
    cal_bottom = size - margin
    cal_left = margin
    cal_right = size - margin
    
    # Calendar body (white rounded rectangle)
    draw.rounded_rectangle(
        [cal_left, cal_top, cal_right, cal_bottom],
        radius=15,
        fill=(255, 255, 255, 255)
    )
    
    # Calendar header (darker blue)
    draw.rounded_rectangle(
        [cal_left, cal_top, cal_right, cal_top + 50],
        radius=15,
        fill=(44, 62, 80, 255)
    )
    draw.rectangle(
        [cal_left, cal_top + 35, cal_right, cal_top + 50],
        fill=(44, 62, 80, 255)
    )
    
    # Calendar rings
    ring_y = cal_top - 5
    for x in [70, 130, 190]:
        draw.ellipse([x-8, ring_y, x+8, ring_y+20], fill=(100, 100, 100, 255))
        draw.ellipse([x-5, ring_y+3, x+5, ring_y+17], fill=(200, 200, 200, 255))
    
    # Grid lines
    grid_top = cal_top + 60
    grid_bottom = cal_bottom - 20
    grid_left = cal_left + 15
    grid_right = cal_right - 15
    
    # Horizontal lines
    for i in range(5):
        y = grid_top + i * (grid_bottom - grid_top) // 4
        draw.line([(grid_left, y), (grid_right, y)], fill=(200, 200, 200, 255), width=1)
    
    # Vertical lines
    for i in range(8):
        x = grid_left + i * (grid_right - grid_left) // 7
        draw.line([(x, grid_top), (x, grid_bottom)], fill=(200, 200, 200, 255), width=1)
    
    # Add checkmark in green
    check_x, check_y = 160, 160
    draw.line([(check_x-20, check_y), (check_x-5, check_y+15)], fill=(39, 174, 96, 255), width=8)
    draw.line([(check_x-5, check_y+15), (check_x+25, check_y-20)], fill=(39, 174, 96, 255), width=8)
    
    # Save as ICO with multiple sizes
    img.save('qsb_tlrs.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("Icon created: qsb_tlrs.ico")

if __name__ == "__main__":
    create_icon()
