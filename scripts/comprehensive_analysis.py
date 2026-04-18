

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

print("="*80)
print("COMPREHENSIVE CANCER VARIANT ANALYSIS")
print("="*80)
print()

# Read VCF data
def run_bcftools(query_format, vcf_file):
    """Run bcftools query and return results"""
    result = subprocess.run(
        ['bcftools', 'query', '-f', query_format, vcf_file],
        capture_output=True, text=True
    )
    return result.stdout.strip().split('\n') if result.stdout else []

vcf_file = 'results/variants/somatic_filtered.vcf.gz'

# 1. VARIANT STATISTICS
print("1. VARIANT STATISTICS")
print("-" * 80)

variants = run_bcftools('%CHROM\\t%POS\\t%REF\\t%ALT\\t%FILTER\\n', vcf_file)
print(f"Total variants called: {len(variants)}")

# Variant types
types = run_bcftools('%TYPE\\n', vcf_file)
type_counts = Counter(types)
print("\nVariant types:")
for vtype, count in type_counts.items():
    print(f"  {vtype}: {count}")

# Filter status
filters = run_bcftools('%FILTER\\n', vcf_file)
filter_counts = Counter(filters)
print("\nFilter status:")
for filt, count in filter_counts.items():
    status = "PASS" if filt == "PASS" else "FILTERED"
    print(f"  {status}: {count}")

# 2. MUTATION SPECTRUM
print("\n2. MUTATION SPECTRUM (Substitution Types)")
print("-" * 80)

mutations = run_bcftools('%REF\\t%ALT\\n', vcf_file)
substitutions = []
for mut in mutations:
    if mut and '\t' in mut:
        ref, alt = mut.split('\t')
        if len(ref) == 1 and len(alt) == 1:
            substitutions.append(f"{ref}>{alt}")

sub_counts = Counter(substitutions)
print("\nSingle nucleotide substitutions:")
for sub, count in sorted(sub_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {sub}: {count}")

# C>T mutations (common in cancer)
ct_mutations = sum(1 for s in substitutions if s in ['C>T', 'G>A'])
print(f"\nC>T / G>A transitions (deamination signature): {ct_mutations} ({100*ct_mutations/len(substitutions):.1f}%)")

# 3. GENOMIC DISTRIBUTION
print("\n3. GENOMIC DISTRIBUTION")
print("-" * 80)

positions = [int(v.split('\t')[1]) for v in variants if v]
if positions:
    print(f"Region span: chr17:{min(positions):,} - {max(positions):,}")
    print(f"Range: {(max(positions) - min(positions)):,} bp")

# 4. COMPARISON TO TRUTH SET
print("\n4. COMPARISON TO TRUTH SET")
print("-" * 80)

truth = pd.read_csv('data/raw/true_variants.tsv', sep='\t')
called_pos = set(int(v.split('\t')[1]) for v in variants if v)
true_pos = set(truth['POS'].values)

true_positives = called_pos & true_pos
false_positives = called_pos - true_pos
false_negatives = true_pos - called_pos

print(f"True positives: {len(true_positives)}")
print(f"False positives: {len(false_positives)}")
print(f"False negatives: {len(false_negatives)}")

if len(called_pos) > 0:
    precision = len(true_positives) / len(called_pos)
    print(f"\nPrecision: {precision:.2%}")
if len(true_pos) > 0:
    sensitivity = len(true_positives) / len(true_pos)
    print(f"Sensitivity: {sensitivity:.2%}")

# 5. KEY FINDINGS
print("\n5. KEY FINDINGS & INTERPRETATION")
print("-" * 80)

print("\nClinical Significance:")
print("• High variant count suggests:")
print("  - Genomic instability (common in cancer)")
print("  - May need stricter filtering for clinical reporting")
print("  - Focus on known cancer genes (TP53, etc.)")

print("\nMutation Signatures:")
ct_percent = 100 * ct_mutations / len(substitutions) if substitutions else 0
if ct_percent > 30:
    print(f"• C>T enrichment ({ct_percent:.1f}%) suggests:")
    print("  - Age-related mutations")
    print("  - Possible APOBEC activity")
    print("  - Consistent with colorectal cancer")

print("\nRecommendations:")
print("• Apply additional filters:")
print("  - Minimum allele frequency (e.g., >5%)")
print("  - Minimum depth (e.g., >20 reads)")
print("  - Focus on coding regions")
print("• Validate key variants with orthogonal method")
print("• Check for known cancer genes")

print("\n" + "="*80)

# Save statistics
stats = {
    'total_variants': len(variants),
    'true_positives': len(true_positives),
    'false_positives': len(false_positives),
    'false_negatives': len(false_negatives),
    'precision': precision if len(called_pos) > 0 else 0,
    'sensitivity': sensitivity if len(true_pos) > 0 else 0,
}

with open('results/reports/variant_stats.txt', 'w') as f:
    f.write("Variant Calling Statistics\n")
    f.write("="*50 + "\n\n")
    for key, value in stats.items():
        if isinstance(value, float):
            f.write(f"{key}: {value:.3f}\n")
        else:
            f.write(f"{key}: {value}\n")

print("\n✓ Statistics saved to: results/reports/variant_stats.txt")
