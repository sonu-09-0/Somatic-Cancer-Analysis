
# Create minimal test variant databases

echo "Creating test variant databases..."

DB_DIR="resources/known_sites"
mkdir -p $DB_DIR

# Create minimal dbSNP VCF (just header + few variants)
cat > $DB_DIR/dbsnp_chr17.vcf << 'VCF'
##fileformat=VCFv4.2
##contig=<ID=chr17,length=83257441>
##INFO=<ID=RS,Number=1,Type=Integer,Description="dbSNP ID">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr17	7577094	rs28934576	C	T	.	PASS	RS=28934576
chr17	7577120	rs28934577	G	A	.	PASS	RS=28934577
chr17	7577538	rs1042522	C	G	.	PASS	RS=1042522
VCF

# Compress and index
bgzip -f $DB_DIR/dbsnp_chr17.vcf
tabix -p vcf $DB_DIR/dbsnp_chr17.vcf.gz

echo "✓ Created test dbSNP database"
echo "✓ Location: $DB_DIR/dbsnp_chr17.vcf.gz"
