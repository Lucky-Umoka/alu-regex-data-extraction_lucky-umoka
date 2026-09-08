# Regex Data Extraction & Secure Validation Assignment

Regex-based program that extracts emails (with ALU domain classification), credit card numbers, phone numbers, and times (12/24-hour) from raw text, which defensive input handling.

## How it works
- Reads 'input/raw-text.txt'
- Sanitizes input (type/size checks, strips null bytes)
- Extracts credit cards and dates first, masks their positions, then extracts phones - avoids misclassifying card numbers or dates as phone numbers (they share the same digit-group shape)
- Classifies emails as alu-official, alu-alumni, alu-si, or general
- Masks credit card numbers to last 4 digits before writing output
- Writes results to 'output/sample-output.json'


## How to run

python3 src/main.py


## Security considerations
- Rejects non-string or oversized input before processing
- Strips null bytes that could manipulate downstream systems
- Credit card numbers are never stored or printed in full - only last 4 digits
- Extraction order (cards/dates before phones) prevents shape-collision misclassification