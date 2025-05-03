import pytesseract
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CaptchaSolver:
    def __init__(self, tesseract_path=None):
        """Initialize with optional Tesseract path."""
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.ocr_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    def solve(self, image_path):
        """Solve CAPTCHA image and return (text, confidence)."""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Invalid image path")
            img = cv2.fastNlMeansDenoising(img, h=15)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 4)
            img = self._deskew(img)
            data = pytesseract.image_to_data(img, config=self.ocr_config, output_type=pytesseract.Output.DICT)
            confidences = [float(c) for c in data['conf'] if c != '-1']
            if not confidences:
                return ("", 0.0)
            avg_conf = sum(confidences)/len(confidences)
            text = ''.join(data['text']).strip()
            return (text, avg_conf)
        except Exception as e:
            logger.error(f"Solving failed: {str(e)}")
            return ("", 0.0)

    def _deskew(self, image):
        """Deskew CAPTCHA image for better OCR."""
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        angle = angle + 90 if angle < -45 else angle
        center = (image.shape[1]//2, image.shape[0]//2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC)
