
# Create all necessary indices for reference genome

set -euo pipefail

echo "PREPARING REFERENCE INDICES"
echo

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

REF_FILE="resources/reference/chr17.fa"

# Check reference exists
if [ ! -f "$REF_FILE" ]; then
    echo "Error: Reference file not found!"
    echo "Run download_reference.sh first"
    exit 1
fi

echo -e "${BLUE}Reference: $REF_FILE${NC}"
echo

# 1. BWA Index (for alignment)
echo "Creating BWA index..."
if [ ! -f "$REF_FILE.bwt" ]; then
    echo "This will take 2-5 minutes..."
    bwa index $REF_FILE
    echo -e "${GREEN}✓ BWA index created${NC}"
else
    echo -e "${GREEN}✓ BWA index already exists${NC}"
fi
echo

# 2. SAMtools Index (for BAM processing)
echo "Creating SAMtools faidx..."
if [ ! -f "$REF_FILE.fai" ]; then
    samtools faidx $REF_FILE
    echo -e "${GREEN}✓ SAMtools index created${NC}"
else
    echo -e "${GREEN}✓ SAMtools index already exists${NC}"
fi
echo

# 3. GATK Dictionary (for variant calling)
echo "Creating GATK sequence dictionary..."
DICT_FILE="${REF_FILE%.fa}.dict"
if [ ! -f "$DICT_FILE" ]; then
    gatk CreateSequenceDictionary \
        -R $REF_FILE \
        -O $DICT_FILE
    echo -e "${GREEN}✓ GATK dictionary created${NC}"
else
    echo -e "${GREEN}✓ GATK dictionary already exists${NC}"
fi
echo

# Verify all indices
echo "VERIFICATION"

files_ok=true

echo "Checking index files..."
[ -f "$REF_FILE.bwt" ] && echo "✓ BWA index (.bwt)" || { echo "✗ Missing .bwt"; files_ok=false; }
[ -f "$REF_FILE.pac" ] && echo "✓ BWA index (.pac)" || { echo "✗ Missing .pac"; files_ok=false; }
[ -f "$REF_FILE.ann" ] && echo "✓ BWA index (.ann)" || { echo "✗ Missing .ann"; files_ok=false; }
[ -f "$REF_FILE.amb" ] && echo "✓ BWA index (.amb)" || { echo "✗ Missing .amb"; files_ok=false; }
[ -f "$REF_FILE.sa" ] && echo "✓ BWA index (.sa)" || { echo "✗ Missing .sa"; files_ok=false; }
[ -f "$REF_FILE.fai" ] && echo "✓ SAMtools index (.fai)" || { echo "✗ Missing .fai"; files_ok=false; }
[ -f "$DICT_FILE" ] && echo "✓ GATK dictionary (.dict)" || { echo "✗ Missing .dict"; files_ok=false; }

echo
if [ "$files_ok" = true ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}ALL INDICES CREATED SUCCESSFULLY${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo "Reference is ready for analysis!"
    echo
    echo "Created files:"
    ls -lh resources/reference/
else
    echo -e "${RED}Some indices are missing!${NC}"
    exit 1
fi
