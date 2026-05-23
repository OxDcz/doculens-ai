#!/usr/bin/env bash
# Setup OCR dependencies for DocuLens AI
# Tested on: Ubuntu 22.04, Debian 12

set -euo pipefail

echo "Installing system dependencies for OCR..."

sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    poppler-utils \
    libpoppler-dev

echo "Tesseract version:"
tesseract --version

pip install pytesseract pdf2image paddleocr

echo ""
echo "OCR setup complete."
echo ""
echo "To use PaddleOCR with GPU, install:"
echo "  pip install paddlepaddle-gpu"
echo ""
echo "Set DOCULENS_OCR_BACKEND in .env:"
echo "  DOCULENS_OCR_BACKEND=tesseract  # or paddleocr"
