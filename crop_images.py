from PIL import Image
import glob
import os

images = glob.glob('images/*.png')
target_images = [
    'images/hero-dashboard.png',
    'images/topology-graph.png',
    'images/multicloud-mockup.png',
    'images/idi-score-gauge.png',
    'images/predictive-alerts-mockup.png',
    'images/deploy-gate-flow.png'
]

for img_path in target_images:
    if os.path.exists(img_path):
        img = Image.open(img_path)
        width, height = img.size
        # Crop 15% from each side
        left = int(width * 0.15)
        top = int(height * 0.15)
        right = int(width * 0.85)
        bottom = int(height * 0.85)
        
        cropped = img.crop((left, top, right, bottom))
        cropped.save(img_path)
        print(f"Cropped {img_path} from {img.size} to {cropped.size}")
