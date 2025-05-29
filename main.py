import sys
from services.image_service import ImageAnalyzer
from rules.year_classifier import classify_photo


import sys
import os
from services.image_service import ImageAnalyzer
from rules.year_classifier import classify_photo

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_image>")
        return

    image_path = sys.argv[1]

    try:
        analyzer = ImageAnalyzer(image_path)

        analysis = {
            "metadata": analyzer.extract_metadata(),
            "dpi": analyzer.get_dpi(),
            "dominant_colors": analyzer.get_dominant_colors(),
            "entropy": analyzer.calculate_entropy(),
            "hist_stats": analyzer.calculate_histogram_stats(),
            "sharpness": analyzer.analyze_sharpness(),
            "noise": analyzer.detect_noise_level(),
            "brightness": analyzer.check_brightness(),
            "color_cast": analyzer.detect_color_cast(),
        }

        result = classify_photo(analysis)

        print("\n📊 Analysis Summary:")
        for key, value in analysis.items():
            print(f"{key}: {value}")
        print(f"\n🕵️ Predicted Photo Era: {result}")

        # Simpan ke file
        filename = os.path.splitext(os.path.basename(image_path))[0]
        output_file = f"/Users/morieshutapea/Desktop/{filename}_analysis.txt"

        with open(output_file, "w") as f:
            f.write("📊 ANALYSIS SUMMARY\n")
            f.write("=====================\n\n")

            # Metadata ringkas
            meta = analysis["metadata"]
            f.write("📷 Metadata:\n")
            for key in ["Make", "Model", "Software", "DateTimeOriginal", "DateTime"]:
                if key in meta:
                    f.write(f"  {key}: {meta[key]}\n")
            f.write("\n")

            # Metrik utama
            f.write("📈 Visual Features:\n")
            f.write(f"  DPI: {analysis['dpi']}\n")
            f.write(f"  Brightness: {analysis['brightness']:.2f} (>=150 = terang modern)\n")
            f.write(f"  Entropy: {analysis['entropy']:.2f} (<=5 = scan/lama)\n")
            f.write(f"  Sharpness: {analysis['sharpness']:.2f} (<=30 = soft/scan)\n")
            f.write(f"  Noise: {analysis['noise']:.2f} (>=10 = film grain)\n")
            f.write(f"  Color Cast: {analysis['color_cast']}\n")
            f.write(f"  Dominant Colors: {', '.join(analysis['dominant_colors'])}\n")
            f.write("\n")

            # Statistik histogram
            f.write("📊 Histogram Stats (RGB skew & kurtosis):\n")
            for k, v in analysis["hist_stats"].items():
                f.write(f"  {k}: {v:.2f}\n")
            f.write("\n")

            # Final result
            f.write("🕵️ PREDICTION\n")
            f.write("=====================\n")
            f.write(f"{result}\n")


        print(f"\n📄 Hasil disimpan ke '{output_file}'")

    except Exception as e:
        print(f"❌ Error: {str(e)}")



if __name__ == "__main__":
    main()
