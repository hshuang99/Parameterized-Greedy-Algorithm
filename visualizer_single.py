import sys
import re
import os
import matplotlib.pyplot as plt

def parse_file(filepath):
    pattern = re.compile(
        r'CNOT:\s*(\d+),\s*depth:\s*(\d+)\s+and\s+cost\s+function:\s*(\S+)(?:\s+with\s+(\S+))?\s+occurs\s+in\s+(\d+)',
        re.IGNORECASE
    )
    records = []
    with open(filepath, 'r') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                records.append({
                    'cnot':         int(m.group(1)),
                    'depth':        int(m.group(2)),
                    'cost':         m.group(3),
                    'norm':         m.group(4) or 'N/A',
                    'occurs':       int(m.group(5)),
                })
    return records

def plot(records, filepath):
    occurs = [r['occurs'] for r in records]
    depths = [r['depth']  for r in records]
    cnots  = [r['cnot']   for r in records]
    labels = [f"{r['cost']}/{r['norm']}" for r in records]

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    filename = os.path.basename(filepath)
    filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
    fig.suptitle(f'{filename_no_ext}', fontsize=13, fontweight='bold')

    # --- Plot 1: occurs vs depth ---
    sc = axes[0].scatter(occurs, depths, c=cnots, cmap='plasma', s=80, edgecolors='k', linewidths=0.5)
    cb = fig.colorbar(sc, ax=axes[0])
    cb.set_label('CNOT count')
    axes[0].set_xlabel('Occurs In (iteration)')
    axes[0].set_ylabel('Depth')
    axes[0].set_title('Occurs In vs Depth  (color = CNOT count)')
    axes[0].grid(True, linestyle='--', alpha=0.4)

    for i, (x, y, lbl) in enumerate(zip(occurs, depths, labels)):
        axes[0].annotate(lbl, (x, y), textcoords='offset points',
                         xytext=(4, 4), fontsize=7, alpha=0.75)

    # --- Plot 2: occurs vs CNOT ---
    axes[1].scatter(occurs, cnots, c=depths, cmap='viridis', s=80, edgecolors='k', linewidths=0.5)
    cb2 = fig.colorbar(axes[1].collections[0], ax=axes[1])
    cb2.set_label('Depth')
    axes[1].set_xlabel('Occurs In (iteration)')
    axes[1].set_ylabel('CNOT Count')
    axes[1].set_title('Occurs In vs CNOT Count  (color = depth)')
    axes[1].grid(True, linestyle='--', alpha=0.4)

    plt.tight_layout()
    out = filepath + '_plot.png'
    plt.savefig(out, dpi=150)
    print(f"Saved: {out}")
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <results_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    records  = parse_file(filepath)

    if not records:
        print("No records found. Check the file format.")
        sys.exit(1)

    print(f"Parsed {len(records)} records.")
    plot(records, filepath)
