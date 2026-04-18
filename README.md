# Cancer Genomics Pipeline - Portfolio Project

## Project Overview

**Title**: Production-Grade Cancer Somatic Variant Calling Pipeline    
**Type**: Bioinformatics / Computational Biology  
**Technologies**: Python, Snakemake, GATK, BWA, Docker, Git


## Summary

Developed an end-to-end automated pipeline for identifying cancer-specific mutations in tumor-normal paired sequencing data. Implemented industry-standard best practices following GATK guidelines, achieving reproducible and scalable variant calling for precision oncology applications.



## Key Achievements

 **Built production-grade bioinformatics pipeline** processing 100K+ reads with 571 somatic variant calls  
 **Implemented GATK best practices** for variant calling with Mutect2 algorithm  
 **Automated workflow** using Snakemake with 13 modular rules across 5 pipeline stages  
 **Created comprehensive QC suite** with FastQC, MultiQC, and custom analysis scripts  
 **Generated publication-quality visualizations** including mutation spectrum analysis and genomic distribution plots  
 **Achieved reproducibility** through containerization and version-controlled dependencies  



## Technical Skills Demonstrated

### Programming & Scripting
- **Python**: Data analysis, visualization (matplotlib, seaborn, pandas)
- **Bash**: Automation scripts, data processing pipelines
- **Workflow Languages**: Snakemake DSL for pipeline orchestration

### Bioinformatics Tools
- **Alignment**: BWA-MEM for short-read mapping
- **Variant Calling**: GATK Mutect2 for somatic mutations
- **BAM Processing**: SAMtools, Picard Tools
- **VCF Handling**: BCFtools for variant filtering
- **Quality Control**: FastQC, MultiQC

### Data Management
- **Version Control**: Git/GitHub for code management
- **Environment Management**: Conda for reproducible environments
- **File Formats**: FASTQ, BAM, VCF, BED genomics formats

### Analysis & Visualization
- **Statistical Analysis**: Precision/sensitivity metrics, mutation signatures
- **Data Visualization**: Publication-quality figures with matplotlib/seaborn
- **Reporting**: Automated report generation with summary statistics


--- 


- **Total Variants**: 571 somatic mutations identified
- **Mutation Spectrum**: C>T enrichment (33.2%) characteristic of age-related mutagenesis
- **Genomic Coverage**: chr17 region spanning 1 million base pairs
- **Performance**: Precision and sensitivity metrics calculated against truth set

## References

1. GATK Best Practices for Somatic Variant Discovery
2. Snakemake: A scalable bioinformatics workflow engine
3. COSMIC: Catalogue of Somatic Mutations in Cancer
