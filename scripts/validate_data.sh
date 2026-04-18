
# Validate all downloaded data

set -euo pipefail


echo "DATA VALIDATION"

echo

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

all_ok=true

# Check reference
echo -e "${BLUE}Checking reference genome...${NC}"
if [ -f "resources/reference/chr17.fa" ]; then
    SIZE=$(du -h resources/reference/chr17.fa | cut -f1)
    echo "✓ chr17.fa exists ($SIZE)"

    # Check indices
    [ -f "resources/reference/chr17.fa.fai" ] && echo "✓ SAMtools index exists" || { echo "✗ Missing .fai"; all_ok=false; }
    [ -f "resources/reference/chr17.fa.bwt" ] && echo "✓ BWA index exists" || { echo "✗ Missing BWA index"; all_ok=false; }
    [ -f "resources/reference/chr17.dict" ] && echo "✓ GATK dict exists" || { echo "✗ Missing .dict"; all_ok=false; }
else
    echo -e "${RED}✗ Reference genome missing${NC}"
    all_ok=false
fi

echo

# Check samples
echo -e "${BLUE}Checking sample data...${NC}"
for sample in tumor normal; do
    for read in R1 R2; do
        file="data/raw/${sample}_${read}.fastq.gz"
        if [ -f "$file" ]; then
            SIZE=$(du -h $file | cut -f1)
            READS=$(zcat $file | wc -l)
            READS=$((READS / 4))
            echo "✓ $file ($SIZE, ${READS} reads)"
        else
            echo -e "${RED}✗ Missing: $file${NC}"
            all_ok=false
        fi
    done
done

echo

# Check databases
echo -e "${BLUE}Checking variant databases...${NC}"
if [ -f "resources/known_sites/dbsnp_chr17.vcf.gz" ]; then
    SIZE=$(du -h resources/known_sites/dbsnp_chr17.vcf.gz | cut -f1)
    echo "✓ dbSNP database exists ($SIZE)"
    [ -f "resources/known_sites/dbsnp_chr17.vcf.gz.tbi" ] && echo "✓ dbSNP index exists" || { echo "✗ Missing .tbi index"; all_ok=false; }
else
    echo -e "${RED}✗ dbSNP database missing${NC}"
    all_ok=false
fi

echo


if [ "$all_ok" = true ]; then
    echo -e "${GREEN}✓ ALL DATA VALIDATED${NC}"

    echo
    echo "Ready to proceed with Phase 3!"
    exit 0
else
    echo -e "${RED}✗ VALIDATION FAILED${NC}"

    echo "Some files are missing. Please check above."
    exit 1
fi
