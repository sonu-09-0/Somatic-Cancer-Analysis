
# Quick variant analysis

VCF="results/variants/somatic_filtered.vcf.gz"


echo "SOMATIC VARIANT ANALYSIS"

echo

echo "Total variants called:"
bcftools view -H $VCF | wc -l

echo
echo "Variants by type:"
bcftools query -f '%TYPE\n' $VCF | sort | uniq -c

echo
echo "Variants by chromosome:"
bcftools query -f '%CHROM\n' $VCF | sort | uniq -c

echo
echo "Filter status:"
bcftools query -f '%FILTER\n' $VCF | sort | uniq -c

echo
echo "First 10 variants:"
echo "CHROM  POS      REF  ALT  FILTER"
bcftools query -f '%CHROM\t%POS\t%REF\t%ALT\t%FILTER\n' $VCF | head -n 10

echo


