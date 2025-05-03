import argparse
from ocr_solver import CaptchaSolver

def main():
    parser = argparse.ArgumentParser(description='CAPTCHA Breaker CLI')
    parser.add_argument('image', help='Path to CAPTCHA image')
    parser.add_argument('--tesseract', help='Custom Tesseract path')
    args = parser.parse_args()

    solver = CaptchaSolver(args.tesseract)
    text, confidence = solver.solve(args.image)
    print(f"Result: {text} (Confidence: {confidence:.1f}%)")

if __name__ == "__main__":
    main()
