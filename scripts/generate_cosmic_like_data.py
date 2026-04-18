

import random
import gzip
import sys
from pathlib import Path

# COSMIC-like mutation hotspots on chr17

COSMIC_HOTSPOTS = [
    {'pos': 7577094, 'ref': 'C', 'alt': 'T', 'gene': 'TP53', 'aa': 'R175H'},
    {'pos': 7577120, 'ref': 'G', 'alt': 'A', 'gene': 'TP53', 'aa': 'R248Q'},
    {'pos': 7577538, 'ref': 'C', 'alt': 'T', 'gene': 'TP53', 'aa': 'R273H'},
    {'pos': 7578190, 'ref': 'C', 'alt': 'T', 'gene': 'TP53', 'aa': 'R282W'},
    {'pos': 7578263, 'ref': 'G', 'alt': 'T', 'gene': 'TP53', 'aa': 'R248L'},
]

def read_reference(ref_file, region_start=0, region_end=10_000_000):
    """Read chr17 reference sequence"""
    print(f"Reading reference: {ref_file}")
    print(f"Region: {region_start:,} - {region_end:,}")

    seq = ""
    with open(ref_file) as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq += line.strip().upper()

    # Take subset
    seq = seq[region_start:region_end]
    print(f"Loaded sequence length: {len(seq):,} bp")
    return seq

def introduce_cosmic_mutations(seq, region_start=0):
    """
    Introduce COSMIC hotspot mutations plus random background mutations
    """
    seq_list = list(seq)
    variants = []
    bases = ['A', 'T', 'G', 'C']

    # Add COSMIC hotspots
    print("\nIntroducing COSMIC hotspot mutations...")
    for hotspot in COSMIC_HOTSPOTS:
        pos = hotspot['pos'] - region_start

        if 0 <= pos < len(seq_list):
            original = seq_list[pos]
            if original == hotspot['ref']:
                seq_list[pos] = hotspot['alt']
                variants.append({
                    'pos': pos + region_start,
                    'ref': hotspot['ref'],
                    'alt': hotspot['alt'],
                    'type': 'SNV',
                    'gene': hotspot['gene'],
                    'aa_change': hotspot['aa'],
                    'source': 'COSMIC'
                })
                print(f"  {hotspot['gene']} {hotspot['aa']}: chr17:{hotspot['pos']} {hotspot['ref']}>{hotspot['alt']}")

    # Add random background mutations
    print("\nAdding background somatic mutations...")
    num_background = 50
    for _ in range(num_background):
        pos = random.randint(1000, len(seq) - 1000)
        original = seq_list[pos]

        # Skip if position already mutated
        if any(v['pos'] == pos + region_start for v in variants):
            continue

        new_base = random.choice([b for b in bases if b != original])
        seq_list[pos] = new_base

        variants.append({
            'pos': pos + region_start,
            'ref': original,
            'alt': new_base,
            'type': 'SNV',
            'gene': 'background',
            'aa_change': 'unknown',
            'source': 'random'
        })

    print(f"Total variants introduced: {len(variants)}")
    return ''.join(seq_list), variants

def generate_reads(sequence, num_reads, read_length=150, region_start=0):
    """
    Simulate Illumina sequencing reads
    """
    reads = []
    positions = []  # Track where reads came from
    seq_len = len(sequence)

    for i in range(num_reads):
        # Random start position
        start = random.randint(0, seq_len - read_length - 1)

        # Extract read
        read = sequence[start:start + read_length]

        # Add realistic sequencing errors (~0.5%)
        read_list = list(read)
        for j in range(len(read_list)):
            if random.random() < 0.005:  # 0.5% error
                bases = ['A', 'T', 'G', 'C', 'N']
                read_list[j] = random.choice(bases)

        reads.append(''.join(read_list))
        positions.append(start + region_start)

        if (i + 1) % 10000 == 0:
            print(f"  Generated {i+1:,} reads...")

    return reads, positions

def write_fastq(reads, output_prefix, sample_name):
    """Write reads to FASTQ with realistic quality scores"""

    print(f"\nWriting {len(reads):,} reads to {output_prefix}...")

    # Realistic quality scores (mostly high, some variation)
    def generate_quality(length):
        """Generate realistic quality string"""
        quals = []
        for i in range(length):
            # Higher quality at read start, lower at end
            if i < 50:
                qual = random.randint(35, 40)  # High quality
            elif i < 100:
                qual = random.randint(30, 38)  # Good quality
            else:
                qual = random.randint(25, 35)  # Moderate quality
            quals.append(chr(qual + 33))
        return ''.join(quals)

    with gzip.open(f"{output_prefix}_R1.fastq.gz", 'wt') as f1, \
         gzip.open(f"{output_prefix}_R2.fastq.gz", 'wt') as f2:

        for i, read in enumerate(reads):
            read_id = f"@{sample_name}_{i+1}"
            qual = generate_quality(len(read))

            # R1 (forward)
            f1.write(f"{read_id}/1\n{read}\n+\n{qual}\n")

            # R2 (reverse complement)
            complement = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
            rc = ''.join([complement.get(b, 'N') for b in reversed(read)])
            qual_rc = qual[::-1]  # Reverse quality too
            f2.write(f"{read_id}/2\n{rc}\n+\n{qual_rc}\n")

    print(f"✓ Written: {output_prefix}_R1.fastq.gz and _R2.fastq.gz")

def main():
    ref_file = "resources/reference/chr17.fa"

    # Configuration - focus on TP53 region (7.5 - 8 million)
    region_start = 7_000_000
    region_end = 8_000_000  # 1 MB region containing TP53

    num_reads_tumor = 100_000   # 100K reads = ~150x coverage
    num_reads_normal = 100_000  # 100K reads

    print("="*70)
    print("REALISTIC CANCER DATA GENERATOR")
    print("COSMIC-like mutations + TP53 hotspots")
    print("="*70)
    print()

    # Check reference exists
    if not Path(ref_file).exists():
        print(f"ERROR: Reference file not found: {ref_file}")
        print("Please ensure chr17.fa exists in resources/reference/")
        sys.exit(1)

    # Read reference
    ref_seq = read_reference(ref_file, region_start, region_end)

    # Create tumor with COSMIC mutations
    print("\n" + "="*70)
    print("CREATING TUMOR SAMPLE")
    print("="*70)
    tumor_seq, variants = introduce_cosmic_mutations(ref_seq, region_start)

    # Save variant truth set
    truth_file = "data/raw/true_variants.tsv"
    with open(truth_file, 'w') as f:
        f.write("CHROM\tPOS\tREF\tALT\tGENE\tAA_CHANGE\tSOURCE\n")
        for v in variants:
            f.write(f"chr17\t{v['pos']}\t{v['ref']}\t{v['alt']}\t{v['gene']}\t{v['aa_change']}\t{v['source']}\n")
    print(f"\n✓ Saved {len(variants)} true variants to: {truth_file}")

    # Generate tumor reads
    print("\n" + "="*70)
    print("GENERATING TUMOR READS")
    print("="*70)
    tumor_reads, _ = generate_reads(tumor_seq, num_reads_tumor, region_start=region_start)
    write_fastq(tumor_reads, "data/raw/tumor", "TUMOR")

    # Generate normal reads (from original reference)
    print("\n" + "="*70)
    print("GENERATING NORMAL READS")
    print("="*70)
    normal_reads, _ = generate_reads(ref_seq, num_reads_normal, region_start=region_start)
    write_fastq(normal_reads, "data/raw/normal", "NORMAL")

    print("\n" + "="*70)
    print("DATA GENERATION COMPLETE")
    print("="*70)
    print("\nFiles created:")
    print("  • data/raw/tumor_R1.fastq.gz")
    print("  • data/raw/tumor_R2.fastq.gz")
    print("  • data/raw/normal_R1.fastq.gz")
    print("  • data/raw/normal_R2.fastq.gz")
    print(f"  • {truth_file}")
    print()
    print(f"Expected variants to find: {len([v for v in variants if v['source']=='COSMIC'])} COSMIC hotspots")
    print(f"Background mutations: {len([v for v in variants if v['source']=='random'])}")
    print()
    print("Key mutations included:")
    for v in variants:
        if v['source'] == 'COSMIC':
            print(f"  • {v['gene']} {v['aa_change']}: chr17:{v['pos']} {v['ref']}>{v['alt']}")
    print()

if __name__ == "__main__":
    main()

