import os
from PIL import Image, ExifTags
from typing import Tuple, Dict, List
import numpy as np
import cv2
from sklearn.cluster import KMeans
from scipy.stats import skew, kurtosis


class ImageAnalyzer:
    def __init__(self, image_path: str):
        if not os.path.isfile(image_path):
            raise FileNotFoundError("Image file not found.")
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")

    def extract_metadata(self) -> Dict[str, str]:
        try:
            exif_data = self.image.getexif()
            return {
            ExifTags.TAGS.get(k, k): v
            for k, v in exif_data.items()
            if k in ExifTags.TAGS
        }
        except Exception:
            return {}

    def get_dpi(self) -> Tuple[int, int]:
        return self.image.info.get("dpi", (72, 72))

    def get_dominant_colors(self, k: int = 3) -> List[str]:
        image_resized = self.image.resize((100, 100))
        img_array = np.array(image_resized).reshape((-1, 3))
        kmeans = KMeans(n_clusters=k, n_init='auto').fit(img_array)
        colors = kmeans.cluster_centers_.astype(int)
        hex_colors = [f'#{r:02X}{g:02X}{b:02X}' for r, g, b in colors]
        return hex_colors
    
    def calculate_entropy(self) -> float:
        img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        hist = cv2.calcHist([img_cv], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()
        entropy = -np.sum([p * np.log2(p + 1e-9) for p in hist_norm])
        return float(entropy)
    
    def calculate_histogram_stats(self) -> Dict[str, float]:
        img_array = np.array(self.image)
        stats = {}
        for i, color in enumerate(['red', 'green', 'blue']):
            channel = img_array[:, :, i].ravel()
            stats[f'{color}_skew'] = float(skew(channel))
            stats[f'{color}_kurtosis'] = float(kurtosis(channel))
        return stats

    def analyze_sharpness(self) -> float:
        img_gray = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
        variance = laplacian.var()
        return float(variance)

    def detect_noise_level(self) -> float:
        img_gray = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        h, w = img_gray.shape
        noise = 0.0
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                neighborhood = img_gray[y-1:y+2, x-1:x+2].astype(np.float32)
                center_pixel = neighborhood[1, 1]
                diff = np.abs(neighborhood - center_pixel)
                noise += np.sum(diff)
        normalized_noise = noise / (h * w * 8)
        return float(normalized_noise)

    def check_brightness(self) -> float:
        img_gray = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2GRAY)
        mean_brightness = np.mean(img_gray)
        return float(mean_brightness)

    def detect_color_cast(self) -> str:
        img_array = np.array(self.image)
        r_mean = np.mean(img_array[:, :, 0])
        g_mean = np.mean(img_array[:, :, 1])
        b_mean = np.mean(img_array[:, :, 2])

        diff_rg = abs(r_mean - g_mean)
        diff_rb = abs(r_mean - b_mean)
        diff_gb = abs(g_mean - b_mean)

        if diff_rg < 5 and diff_rb < 5 and diff_gb < 5:
            return "neutral"
        elif r_mean > g_mean and r_mean > b_mean:
            return "red cast"
        elif g_mean > r_mean and g_mean > b_mean:
            return "green cast"
        elif b_mean > r_mean and b_mean > g_mean:
            return "blue cast"
        elif r_mean + g_mean > b_mean * 2:
            return "yellow cast"
        elif b_mean > r_mean + g_mean:
            return "cyan cast"
        else:
            return "uncertain"

    def is_screenshot(self) -> bool:
        meta = self.extract_metadata()
        width, height = self.image.size

        known_screen_resolutions = [
        (1920, 1080), (1366, 768), (1280, 720), (1440, 900),
        (1170, 2532), (1080, 2400), (828, 1792)
        ]

        if any(x in str(meta.get("Software", "")).lower() for x in ["screenshot", "android", "miui", "ios", "snipping", "macos"]):
            return True
        if not any(k in meta for k in ["Make", "Model", "DateTimeOriginal"]):
            return True
        if (width, height) in known_screen_resolutions or (height, width) in known_screen_resolutions:
            return True

        return False
