#!/usr/bin/env bash
# 商品PDFを再生成する(任意)。make_pdfs.py でHTMLを生成し、Chrome headless で日本語PDFに変換。
# 注: ReportLab等では日本語が文字化けするため、HTML→PDF(システムのCJKフォント使用)を採用。
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/make_pdfs.py"                      # → /tmp/nissay/pdfhtml/*.html
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p "$HERE/pdf"
for h in /tmp/nissay/pdfhtml/*.html; do
  base="$(basename "${h%.html}")"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$HERE/pdf/$base.pdf" "file://$h" 2>/dev/null
  echo "rendered $base.pdf"
done
