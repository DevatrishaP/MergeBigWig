import pyBigWig
import numpy as np

# Ask user for input file paths
file1_path = input("Enter path to first bigWig file: ").strip()
file2_path = input("Enter path to second bigWig file: ").strip()
output_path = input("Enter path for merged output bigWig (e.g., merged.bw): ").strip()

# Open bigWig files
bw1 = pyBigWig.open(file1_path)
bw2 = pyBigWig.open(file2_path)

chroms = bw1.chroms()

# Create output file
out = pyBigWig.open(output_path, "w")
out.addHeader(list(chroms.items()))

# Merge signal chromosome by chromosome
for chrom in chroms:
    len_chrom = chroms[chrom]
    
    # Get values from both files
    vals1 = bw1.values(chrom, 0, len_chrom, numpy=True)
    vals2 = bw2.values(chrom, 0, len_chrom, numpy=True)
    
    # Add signal values, treating NaNs as 0
    merged_vals = np.nan_to_num(vals1) + np.nan_to_num(vals2)
    
    # Write in chunks to save memory
    step = 1000000
    for i in range(0, len_chrom, step):
        end = min(i + step, len_chrom)
        out.addEntries([chrom] * (end - i),
                       list(range(i, end)),
                       ends=list(range(i + 1, end + 1)),
                       values=merged_vals[i:end].tolist())

# Close files
bw1.close()
bw2.close()
out.close()

print(f"\n✅ Merged bigWig saved to: {output_path}")

