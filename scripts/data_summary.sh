
# Generate data summary report


echo "DATA SUMMARY REPORT"

echo

echo "PROJECT: Cancer Somatic Variant Pipeline"
echo "DATE: $(date)"
echo


echo "REFERENCE GENOME"
grep "^>" resources/reference/chr17.fa | head -n1
du -h resources/reference/chr17.fa
echo "Indices: $(ls resources/reference/ | wc -l) files"
echo


echo "SAMPLE DATA"

echo "Tumor Sample:"
echo "  R1: $(du -h data/raw/tumor_R1.fastq.gz | cut -f1)"
echo "  R2: $(du -h data/raw/tumor_R2.fastq.gz | cut -f1)"
echo "  Total reads: $(zcat data/raw/tumor_R1.fastq.gz | wc -l | awk '{print $1/4}')"

echo
echo "Normal Sample:"
echo "  R1: $(du -h data/raw/normal_R1.fastq.gz | cut -f1)"
echo "  R2: $(du -h data/raw/normal_R2.fastq.gz | cut -f1)"
echo "  Total reads: $(zcat data/raw/normal_R1.fastq.gz | wc -l | awk '{print $1/4}')"

echo

echo "VARIANT DATABASES"

ls -lh resources/known_sites/

echo

echo "STORAGE USAGE"

du -sh resources/
du -sh data/

echo
echo "STATUS: Ready for Analysis"

