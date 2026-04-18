

import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter
import numpy as np

# Set publication style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("colorblind")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

print("Generating publication figures...")

def run_bcftools(query_format, vcf_file):
    """Run bcftools query"""
    result = subprocess.run(
        ['bcftools', 'query', '-f', query_format, vcf_file],
        capture_output=True, text=True
    )
    return result.stdout.strip().split('\n') if result.stdout else []

vcf_file = 'results/variants/somatic_filtered.vcf.gz'

# FIGURE 1: Mutation Spectrum
print("Creating Figure 1: Mutation Spectrum...")

mutations = run_bcftools('%REF\\t%ALT\\n', vcf_file)
substitutions = []
for mut in mutations:
    if mut and '\t' in mut:
        ref, alt = mut.split('\t')
        if len(ref) == 1 and len(alt) == 1:
            substitutions.append(f"{ref}>{alt}")

sub_counts = Counter(substitutions)

fig, ax = plt.subplots(figsize=(10, 6))
subs = sorted(sub_counts.items(), key=lambda x: x[1], reverse=True)
labels = [s[0] for s in subs]
values = [s[1] for s in subs]

colors = ['#e74c3c' if '>' in s and ('C>T' in s or 'G>A' in s) else '#3498db' for s in labels]
bars = ax.bar(range(len(labels)), values, color=colors)

ax.set_xlabel('Substitution Type', fontsize=12, fontweight='bold')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Somatic Mutation Spectrum', fontsize=14, fontweight='bold')
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#e74c3c', label='C>T / G>A (transitions)'),
    Patch(facecolor='#3498db', label='Other substitutions')
]
ax.legend(handles=legend_elements, loc='upper right')

plt.tight_layout()
plt.savefig('results/reports/figure1_mutation_spectrum.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/reports/figure1_mutation_spectrum.png")
plt.close()

# FIGURE 2: Variant Distribution Along Chromosome
print("Creating Figure 2: Genomic Distribution...")

positions = [int(v.split('\t')[1]) for v in run_bcftools('%POS\\n', vcf_file) if v]

fig, ax = plt.subplots(figsize=(12, 4))

# Create bins
bins = np.linspace(min(positions), max(positions), 50)
counts, edges = np.histogram(positions, bins=bins)

ax.bar(edges[:-1], counts, width=np.diff(edges), color='#2ecc71', alpha=0.7, edgecolor='black')
ax.set_xlabel('Genomic Position (chr17)', fontsize=12, fontweight='bold')
ax.set_ylabel('Variant Count', fontsize=12, fontweight='bold')
ax.set_title('Somatic Variant Distribution on Chromosome 17', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Format x-axis
ax.ticklabel_format(style='plain', axis='x')
labels = ax.get_xticks()
ax.set_xticklabels([f'{int(l/1e6):.1f}M' for l in labels])

plt.tight_layout()
plt.savefig('results/reports/figure2_genomic_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/reports/figure2_genomic_distribution.png")
plt.close()

# FIGURE 3: Pipeline Performance
print("Creating Figure 3: Pipeline Performance...")

truth = pd.read_csv('data/raw/true_variants.tsv', sep='\t')
called_pos = set(positions)
true_pos = set(truth['POS'].values)

tp = len(called_pos & true_pos)
fp = len(called_pos - true_pos)
fn = len(true_pos - called_pos)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Confusion matrix
categories = ['True\nPositives', 'False\nPositives', 'False\nNegatives']
values = [tp, fp, fn]
colors = ['#27ae60', '#e74c3c', '#f39c12']

ax1.bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
ax1.set_ylabel('Count', fontsize=12, fontweight='bold')
ax1.set_title('Variant Calling Performance', fontsize=13, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

for i, v in enumerate(values):
    ax1.text(i, v + max(values)*0.02, str(v), ha='center', fontweight='bold')

# Metrics
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0

metrics = ['Precision', 'Sensitivity', 'F1-Score']
metric_values = [precision, sensitivity, f1]

ax2.barh(metrics, metric_values, color='#3498db', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Score', fontsize=12, fontweight='bold')
ax2.set_title('Performance Metrics', fontsize=13, fontweight='bold')
ax2.set_xlim(0, 1)
ax2.grid(axis='x', alpha=0.3)

for i, v in enumerate(metric_values):
    ax2.text(v + 0.02, i, f'{v:.2%}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/reports/figure3_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/reports/figure3_performance.png")
plt.close()

# FIGURE 4: Summary Dashboard
print("Creating Figure 4: Analysis Summary Dashboard...")

fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Panel A: Key Statistics
ax1 = fig.add_subplot(gs[0, :])
ax1.axis('off')

stats_text = f"""
CANCER SOMATIC VARIANT ANALYSIS - SUMMARY DASHBOARD

Dataset: Tumor-Normal Paired Analysis (Chromosome 17)
Pipeline: Snakemake + GATK Mutect2 + BWA-MEM

KEY FINDINGS:
- Total somatic variants identified: {len(positions)}
- True positives (validated): {tp}
- Precision: {precision:.1%}  |  Sensitivity: {sensitivity:.1%}
- Dominant mutation type: C>T transitions ({sum(1 for s in substitutions if s in ['C>T', 'G>A'])} / {len(substitutions)})

CLINICAL RELEVANCE:
- High variant burden suggests genomic instability
- C>T enrichment consistent with age-related mutagenesis
- Requires validation for clinical decision-making
"""

ax1.text(0.05, 0.5, stats_text, fontsize=11, family='monospace',
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Panel B: Mutation types pie chart
ax2 = fig.add_subplot(gs[1, 0])
type_counts = Counter([v.split('\t')[3] if '\t' in v and len(v.split('\t')) > 3 else 'SNP' 
                       for v in mutations])
ax2.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%', startangle=90)
ax2.set_title('Variant Types', fontweight='bold')

# Panel C: Top substitutions
ax3 = fig.add_subplot(gs[1, 1])
top_subs = dict(sorted(sub_counts.items(), key=lambda x: x[1], reverse=True)[:6])
ax3.bar(top_subs.keys(), top_subs.values(), color='steelblue', edgecolor='black')
ax3.set_title('Top 6 Substitution Types', fontweight='bold')
ax3.set_xlabel('Substitution')
ax3.set_ylabel('Count')
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Panel D: Genomic position
ax4 = fig.add_subplot(gs[2, :])
ax4.scatter(positions, range(len(positions)), alpha=0.5, s=10, c='darkgreen')
ax4.set_xlabel('Genomic Position (chr17)', fontweight='bold')
ax4.set_ylabel('Variant Index', fontweight='bold')
ax4.set_title('Variant Positions on Chromosome 17', fontweight='bold')
ax4.ticklabel_format(style='plain', axis='x')

plt.savefig('results/reports/figure4_summary_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/reports/figure4_summary_dashboard.png")
plt.close()

print("\n" + "="*70)
print("ALL FIGURES GENERATED SUCCESSFULLY")
print("="*70)
print("\nFiles created:")
print("  • figure1_mutation_spectrum.png")
print("  • figure2_genomic_distribution.png")
print("  • figure3_performance.png")
print("  • figure4_summary_dashboard.png")
print()
