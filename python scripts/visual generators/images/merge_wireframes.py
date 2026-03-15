from PIL import Image
import os
import glob

# Directory containing the wireframes
out_dir = '/Users/neelmishra/antigravity/synthetic growth/Numeral Growth/wireframes'

# Get all slide images
images_list = sorted(glob.glob(os.path.join(out_dir, 'slide_*.png')))

if not images_list:
    print("No wireframe images found.")
    exit()

# Open all images
images = [Image.open(x) for x in images_list]

# Calculate total height and max width
widths, heights = zip(*(i.size for i in images))
total_height = sum(heights)
max_width = max(widths)

# Create a new blank image
new_im = Image.new('RGB', (max_width, total_height), color='#0A0F1D')

# Paste images one by one
y_offset = 0
for im in images:
    new_im.paste(im, (0, y_offset))
    y_offset += im.size[1]

# Save the result
output_path = os.path.join(out_dir, 'numeral_wireframes_merged.png')
new_im.save(output_path)
print(f"✅ Successfully merged {len(images)} slides into: {output_path}")
