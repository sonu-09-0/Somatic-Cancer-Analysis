
# Download known variant databases for chr17

set -euo pipefail

echo "DOWNLOADING VARIANT DATABASES"

echo

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

DB_DIR="resources/known_sites"
mkdir -p $DB_DIR

echo -e "${YELLOW}Note: Full databases are large (GBs)${NC}"
echo -e "${YELLOW}We'll download chr17-specific subsets${NC}"
echo

# dbSNP (common variants)

echo "Downloading dbSNP (chr17)..."


DBSNP_URL="https://ftp.ncbi.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/00-All.vcf.gz"
DBSNP_FILE="$DB_DIR/dbsnp_chr17.vcf.gz"

if [ ! -f "$DBSNP_FILE" ]; then
    echo "Downloading and filtering for chr17..."
    echo -e "${BLUE}This may take 10-20 minutes (large file)...${NC}"

    # Download full file, then extract chr17
    wget -O "$DB_DIR/dbsnp_temp.vcf.gz" "$DBSNP_URL"

    # Extract chr17 only
    bcftools view -r chr17 "$DB_DIR/dbsnp_temp.vcf.gz" -Oz -o "$DBSNP_FILE"
    bcftools index -t "$DBSNP_FILE"

    # Cleanup
    rm "$DB_DIR/dbsnp_temp.vcf.gz"

    echo -e "${GREEN}✓ dbSNP downloaded and indexed${NC}"
else
    echo -e "${GREEN}✓ dbSNP already exists${NC}"
fi

echo
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}DATABASE DOWNLOAD OPTIONS${NC}"
echo -e "${YELLOW}========================================${NC}"
echo
echo "For full tutorial, you would also download:"
echo "- COSMIC (requires registration)"
echo "- ClinVar (free, from NCBI)"
echo "- gnomAD (large, ~100GB for genome)"
echo
echo "For this learning project, dbSNP is sufficient!"
echo "We can add others later if needed."
echo

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}DATABASE SETUP COMPLETE${NC}"
echo -e "${GREEN}========================================${NC}"
