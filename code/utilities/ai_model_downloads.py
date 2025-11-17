import os
import urllib.request

# Use RAW URLs, not the HTML page links
urls = {
    "deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
    "res10_300x300_ssd_iter_140000.caffemodel": "https://github.com/shiyazt/Face-Recognition-using-Opencv-/raw/master/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
}

# Target directory
target_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(target_dir, exist_ok=True)

# Download each file
for filename, url in urls.items():
    filepath = os.path.join(target_dir, filename)
    print(f"Downloading {filename} from {url}...")
    urllib.request.urlretrieve(url, filepath)
    print(f"Saved to {filepath}")

print("🎉 All files downloaded successfully!")
