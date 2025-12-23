# ai_service/model/preprocess.py
import os
import re
import logging
from typing import List
from pathlib import Path

# Use pdfplumber for text PDFs, PyMuPDF (fitz) fallback, and pytesseract OCR fallback for scanned pages
import pdfplumber
import fitz  # PyMuPDF
from PIL import Image
import io

# OCR (optional) - requires tesseract installed on system
try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    pytesseract = None
    OCR_AVAILABLE = False

logger = logging.getLogger(__name__)


class PDFPreprocessor:
    """
    Robust PDF preprocessor:
      - tries pdfplumber first (best for text PDFs),
      - falls back to PyMuPDF (fitz) text extraction,
      - if page has no text and OCR available, runs pytesseract OCR on page image.
    Produces cleaned text and intelligently chunked text files.
    """

    def __init__(self, pdf_dir: str = "data/raw_pdfs", ocr_on: bool = True):
        self.pdf_dir = os.path.abspath(pdf_dir)
        self.ocr_on = ocr_on and OCR_AVAILABLE
        if ocr_on and not OCR_AVAILABLE:
            logger.warning("pytesseract not available: OCR disabled. Install pytesseract and Tesseract binary for OCR.")

    # ---------------- extraction ----------------
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        logger.info(f"Extracting: {pdf_path}")
        text_pages = []

        # 1) Try pdfplumber (good for most text PDFs)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_pages.append(page_text)
                    else:
                        text_pages.append("")  # keep placeholder for fallback
        except Exception as e:
            logger.debug(f"pdfplumber failed for {pdf_path}: {e}")
            text_pages = []

        # 2) If pdfplumber returned nothing or empty pages, try PyMuPDF to get images/other encodings
        try_fitz = False
        if not text_pages:
            try_fitz = True
        else:
            # also check per-page empties
            if any(p == "" for p in text_pages):
                try_fitz = True

        if try_fitz:
            try:
                doc = fitz.open(pdf_path)
                fitz_pages = []
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    text = page.get_text("text") or ""
                    fitz_pages.append(text)
                # merge where pdfplumber had text; otherwise overwrite empties
                if not text_pages:
                    text_pages = fitz_pages
                else:
                    # take non-empty from fitz for pages where pdfplumber had empty
                    merged = []
                    for p_pdfplumber, p_fitz in zip(text_pages, fitz_pages):
                        merged.append(p_pdfplumber if p_pdfplumber.strip() else p_fitz)
                    text_pages = merged
            except Exception as e:
                logger.debug(f"PyMuPDF (fitz) extraction failed for {pdf_path}: {e}")

        # 3) For remaining empty pages, try OCR (if available and enabled)
        if self.ocr_on:
            # ensure doc loaded
            try:
                doc = fitz.open(pdf_path)
                for i, page_text in enumerate(text_pages):
                    if not page_text.strip():
                        try:
                            page = doc.load_page(i)
                            pix = page.get_pixmap(dpi=200)
                            img_data = pix.tobytes("png")
                            img = Image.open(io.BytesIO(img_data)).convert("RGB")
                            ocr_text = pytesseract.image_to_string(img, lang='eng')
                            text_pages[i] = ocr_text
                        except Exception as e:
                            logger.debug(f"OCR failed on page {i} of {pdf_path}: {e}")
            except Exception as e:
                logger.debug(f"Could not open with fitz for OCR: {e}")

        # Join pages with double newline and clean
        raw_text = "\n\n".join(p.strip() for p in text_pages if p is not None)
        cleaned = self._clean_text(raw_text)
        logger.info(f"Extracted {len(cleaned)} characters from {os.path.basename(pdf_path)}")
        return cleaned

    # ---------------- cleaning ----------------
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        # Normalize newlines
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove repeated blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Fix hyphenation at line breaks: "exam-\nple" -> "example"
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        # Remove header/footer line duplicates — heuristic:
        # detect short lines that repeat on many pages (like book title or page header)
        lines = text.splitlines()
        freq = {}
        for i, ln in enumerate(lines):
            s = ln.strip()
            if 0 < len(s) <= 80:
                freq[s] = freq.get(s, 0) + 1
        # header/footer candidates: appear on 3+ pages (heuristic)
        candidates = {k for k, v in freq.items() if v >= 3 and len(k.split()) < 6}
        if candidates:
            pattern = r'^(?:' + '|'.join(re.escape(c) for c in sorted(candidates, key=len, reverse=True)) + r')\s*$'
            text = re.sub(pattern, '', text, flags=re.MULTILINE)

        # Remove page numbers lines that are solely digits
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        # Normalize multiple spaces
        text = re.sub(r'[ \t]{2,}', ' ', text)

        # Trim leading/trailing
        text = text.strip()

        return text

    # ---------------- chunking ----------------
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Create chunks of approx chunk_size characters with overlap (characters).
        Prefer splitting at paragraph or sentence boundaries.
        """
        if not text:
            return []

        paragraphs = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
        chunks = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) + 2 <= chunk_size:
                current = (current + "\n\n" + para).strip()
            else:
                if current:
                    chunks.append(current.strip())
                # If paragraph itself huge, split by sentences
                if len(para) > chunk_size:
                    sentences = re.split(r'(?<=[.!?])\s+', para)
                    tmp = ""
                    for s in sentences:
                        if len(tmp) + len(s) <= chunk_size:
                            tmp = (tmp + " " + s).strip()
                        else:
                            if tmp:
                                chunks.append(tmp.strip())
                            tmp = s
                    if tmp:
                        current = tmp
                    else:
                        current = ""
                else:
                    current = para
            # keep overlap by trimming
            if len(current) > chunk_size:
                current = current[:chunk_size]
        if current:
            chunks.append(current.strip())

        # create overlap by adding last N chars from previous chunk to next
        if overlap and len(chunks) > 1:
            new_chunks = []
            for i, ch in enumerate(chunks):
                if i == 0:
                    new_chunks.append(ch)
                else:
                    prev = new_chunks[-1]
                    # get overlap characters from prev (try to get full sentences)
                    overlap_text = prev[-overlap:] if len(prev) > overlap else prev
                    new_chunks.append((overlap_text + "\n\n" + ch).strip())
            chunks = new_chunks

        logger.info(f"Chunked into {len(chunks)} parts (chunk_size={chunk_size}, overlap={overlap})")
        return chunks

    # ---------------- full processing ----------------
    def process_all_pdfs(self, output_dir: str = None, chunk_size: int = 1000, overlap: int = 200) -> dict:
        """
        Process all PDFs in pdf_dir and save per-PDF txt files with CHUNK markers.
        Returns mapping: {pdf_filename: [chunk,...]}
        """
        if not os.path.isdir(self.pdf_dir):
            raise FileNotFoundError(f"PDF directory not found: {self.pdf_dir}")

        pdf_files = [p for p in os.listdir(self.pdf_dir) if p.lower().endswith('.pdf')]
        result = {}
        for pdf_file in pdf_files:
            path = os.path.join(self.pdf_dir, pdf_file)
            try:
                text = self.extract_text_from_pdf(path)
                if not text or len(text) < 50:
                    logger.warning(f"No meaningful text extracted from {pdf_file}")
                    continue
                chunks = self.chunk_text(text, chunk_size=chunk_size, overlap=overlap)
                result[pdf_file] = chunks

                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    out_path = os.path.join(output_dir, pdf_file.replace('.pdf', '.txt'))
                    with open(out_path, 'w', encoding='utf-8') as f:
                        for i, ch in enumerate(chunks):
                            f.write(f"=== CHUNK {i+1} ===\n")
                            f.write(ch)
                            f.write("\n\n" + "="*50 + "\n\n")
                    logger.info(f"Saved processed text: {out_path}")
            except Exception as e:
                logger.exception(f"Failed to process {pdf_file}: {e}")

        return result
