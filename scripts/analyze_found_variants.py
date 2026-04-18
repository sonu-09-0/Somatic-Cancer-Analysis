

import pandas as pd

# Read truth set
truth = pd.read_csv('data/raw/true_variants.tsv', sep='\t')
print("="*70)
print("VARIANT CALLING ANALYSIS")
print("="*70)
print()

print(f"True variants: {len(truth)}")
print(f"  - COSMIC hotspots: {len(truth[truth['SOURCE']=='COSMIC'])}")
print(f"  - Background: {len(truth[truth['SOURCE']=='random'])}")
print()

# Read called variants
import subprocess
result = subprocess.run(
    ['bcftools', 'query', '-f', '%POS\\t%REF\\t%ALT\\n',
     'results/variants/somatic_filtered.vcf.gz'],
    capture_output=True, text=True
)

if result.stdout:
    called_lines = result.stdout.strip().split('\n')
    called_positions = set()
    for line in called_lines:
        if line:
            pos = int(line.split('\t')[0])
            called_positions.add(pos)

    print(f"Variants called: {len(called_positions)}")
    print()

    # Check COSMIC hotspots
    cosmic = truth[truth['SOURCE'] == 'COSMIC']
    print("COSMIC Hotspot Detection:")
    print("-" * 70)
    for _, var in cosmic.iterrows():
        found = var['POS'] in called_positions
        status = "✓ FOUND" if found else "✗ MISSED"
        print(f"{status}  {var['GENE']} {var['AA_CHANGE']}: "
              f"chr17:{var['POS']} {var['REF']}>{var['ALT']}")

    found_cosmic = sum(1 for _, v in cosmic.iterrows() if v['POS'] in called_positions)
    print()
    print(f"Sensitivity for COSMIC hotspots: {found_cosmic}/{len(cosmic)} "
          f"({100*found_cosmic/len(cosmic):.1f}%)")

else:
    print("No variants called!")

print()

