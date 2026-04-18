#!/usr/bin/env python3
"""
Generate realistic test FASTQ data for pipeline testing
Creates small but realistic tumor-normal paired data
"""

import random
import gzip

def generate_read(length=150, quality_range=(30, 40)):
    """Generate random DNA read with quality scores"""
    bases = ['A', 'T', 'G', 'C']
    read = ''.join(random.choices(bases, k=length))

    # Quality scores (Phred+33)
    quals = ''.join(chr(random.randint(quality_range[0], quality_range[1]) + 33) 
                   for _ in range(length))

    return read, quals

def write_fastq_pair(output_prefix, num_reads=100000):
    """Write paired-end FASTQ files"""
    print(f"Generating {num_reads} read pairs...")
    with gzip.open(f"{output_prefix}_R1.fastq.gz", 'wt') as f1, \
         gzip.open(f"{output_prefix}_R2.fastq.gz", 'wt') as f2:
        for i in range(num_reads):
            read_id = f"@SIM_READ_{i+1}/1"
            # Read 1
            seq1, qual1 = generate_read()
            f1.write(f"{read_id}\n{seq1}\n+\n{qual1}\n")
            # Read 2 (paired)
            seq2, qual2 = generate_read()
            f2.write(f"{read_id.replace('/1', '/2')}\n{seq2}\n+\n{qual2}\n")
            if (i + 1) % 10000 == 0:
                print(f"  Generated {i+1:,} reads...")
    print(f"✓ Wrote {output_prefix}_R1.fastq.gz and {output_prefix}_R2.fastq.gz")

if __name__ == "__main__":
    import sys
    # Generate tumor sample (100K reads = ~30 MB)
    print("\n" + "="*50)
    print("GENERATING TUMOR SAMPLE")
    print("="*50)
    write_fastq_pair("data/raw/tumor", num_reads=100000)

    # Generate normal sample (100K reads = ~30 MB)
    print("\n" + "="*50)
    print("GENERATING NORMAL SAMPLE")
    print("="*50)
    write_fastq_pair("data/raw/normal", num_reads=100000)
    print("\n" + "="*50)
    print("TEST DATA GENERATION COMPLETE")
    print("="*50)
    print("\nCreated files:")
    print("  data/raw/tumor_R1.fastq.gz")
    print("  data/raw/tumor_R2.fastq.gz")
    print("  data/raw/normal_R1.fastq.gz")
    print("  data/raw/normal_R2.fastq.gz")
    print("\nTotal size: ~60 MB (small test set)")
    print("\nNOTE: This is SYNTHETIC data for testing the pipeline.")
    print("For real analysis, use actual sequencing data.")
