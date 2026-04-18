
# Download and prepare reference genome (chromosome 17)

set -euo pipefail  # Exit on error, undefined vars, pipe failures

echo "DOWNLOADING REFERENCE GENOME (CHR17)"
echo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Directories
REF_DIR="resources/reference"
TEMP_DIR="resources/temp"

mkdir -p $REF_DIR
mkdir -p $TEMP_DIR

# Reference URL (UCSC hg38 chromosome 17)
CHR17_URL="https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr17.fa.gz"
OUTPUT_FILE="$REF_DIR/chr17.fa"

echo -e "${BLUE}Downloading chr17 from UCSC...${NC}"
echo "URL: $CHR17_URL"
echo

# Download
if [ ! -f "$OUTPUT_FILE.gz" ]; then
    wget -O "$TEMP_DIR/chr17.fa.gz" "$CHR17_URL"
    mv "$TEMP_DIR/chr17.fa.gz" "$REF_DIR/"
    echo -e "${GREEN}✓ Download complete${NC}"
else
    echo -e "${GREEN}✓ File already exists, skipping download${NC}"
fi

# Decompress
echo
echo -e "${BLUE}Decompressing...${NC}"
if [ ! -f "$OUTPUT_FILE" ]; then
    gunzip -c "$REF_DIR/chr17.fa.gz" > "$OUTPUT_FILE"
    echo -e "${GREEN}✓ Decompression complete${NC}"
else
    echo -e "${GREEN}✓ Already decompressed${NC}"
fi

# Verify file
echo
echo -e "${BLUE}Verifying reference file...${NC}"
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    LINES=$(wc -l < "$OUTPUT_FILE")
    echo "File size: $SIZE"
    echo "Total lines: $LINES"
    # Check header
    HEADER=$(head -n1 "$OUTPUT_FILE")
    if [[ $HEADER == ">chr17"* ]]; then
        echo -e "${GREEN}✓ Reference genome valid${NC}"
    else
        echo -e "${RED}✗ Invalid FASTA format${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Reference file not found${NC}"
    exit 1
fi

echo
echo -e "${GREEN}REFERENCE DOWNLOAD COMPLETE${NC}"
echo "Location: $OUTPUT_FILE"
echo "Next step: Run prepare_reference.sh to create indices"
