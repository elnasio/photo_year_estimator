from typing import Dict

def classify_photo(analysis: Dict) -> str:
    metadata = analysis.get("metadata", {})
    entropy = analysis.get("entropy", 0)
    sharpness = analysis.get("sharpness", 0)
    noise = analysis.get("noise", 0)
    brightness = analysis.get("brightness", 0)
    dpi_x, _ = analysis.get("dpi", (72, 72))
    color_cast = analysis.get("color_cast", "neutral")
    software = metadata.get("Software", "").lower()
    model = metadata.get("Model", "")

    # --- Rule 1: Metadata year from EXIF ---
    for date_key in ["DateTimeOriginal", "DateTime", "CreateDate"]:
        if date_key in metadata:
            year = str(metadata[date_key])[:4]
            return f"From metadata: {year}"

    # --- Rule 2: Screenshot detection ---
    if (
        130 <= dpi_x <= 160 and
        entropy < 5 and
        sharpness > 500 and
        brightness < 100 and
        not metadata.get("Make") and
        not metadata.get("Model")
    ):
        return "Likely Screenshot – not a real photo"

    # --- Rule 3: Edited digital (Photoshop etc.) ---
    if (
        dpi_x <= 100 and
        entropy > 5 and
        sharpness < 30 and
        brightness > 140 and
        "photoshop" in software
    ):
        return "Likely 2015–2020 (digitally edited or retouched)"

    # --- Rule 4: Very Modern (camera, high res) ---
    if (
        dpi_x >= 300 and
        entropy > 6.5 and
        sharpness > 100 and
        brightness > 120
    ):
        return "Modern (2019+)"

    # --- Rule 5: Recent digital (mobile or studio) ---
    if (
        50 < sharpness <= 100 and
        entropy > 6 and
        brightness > 100
    ):
        return "Likely 2010–2018"

    # --- Rule 6: Probable Digital without metadata ---
    if (
        entropy > 6 and
        sharpness >= 100 and
        brightness > 120 and
        dpi_x <= 100 and
        not metadata.get("Make") and
        not metadata.get("Model")
    ):
        return "Possibly Recent (2015–2020) – no metadata but strong digital features"

    # --- Rule 7: Early digital camera era ---
    if (
        100 <= dpi_x <= 200 and
        5 < entropy < 6.5
    ):
        return "2000–2010"

    # --- Rule 8: Analog scan or low-quality copy ---
    if (
        dpi_x < 150 and
        entropy <= 5.0 and
        noise > 15
    ):
        return "Before 2000"

    # --- Rule 9: Color cast with dark brightness (yellow/green scan) ---
    if (
        color_cast in ["yellow cast", "green cast"] and
        brightness < 100
    ):
        return "Possibly Scanned (Before 2000)"

    # --- Fallback ---
    return "Unknown – ambiguous visual signal"

