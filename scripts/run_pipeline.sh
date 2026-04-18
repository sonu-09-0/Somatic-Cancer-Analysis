
# Run the complete cancer genomics pipeline

set -euo pipefail


echo "CANCER SOMATIC VARIANT PIPELINE"

echo
echo "Starting: $(date)"
echo

# Configuration
CORES=$(nproc)  # Use all available cores
MAX_CORES=8     # Cap at 8 to avoid overload

if [ $CORES -gt $MAX_CORES ]; then
    CORES=$MAX_CORES
fi

echo "Using $CORES CPU cores"
echo

# Create output directories
mkdir -p results/{qc,alignment,variants,annotation,reports}
mkdir -p logs benchmarks

# Run Snakemake
snakemake \
    --cores $CORES \
    --printshellcmds \
    --reason \
    --keep-going \
    --rerun-incomplete \
    2>&1 | tee logs/pipeline_$(date +%Y%m%d_%H%M%S).log

echo

echo "PIPELINE COMPLETED"

echo "Finished: $(date)"
echo
echo "Check results in:"
echo "  - results/qc/multiqc_report.html"
echo "  - results/variants/somatic_filtered.vcf.gz"
echo "  - results/reports/analysis_summary.txt"
