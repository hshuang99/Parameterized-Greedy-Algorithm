import sys
import re
import os
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_file(filepath):
    pattern = re.compile(
        r'CNOT:\s*(\d+),\s*depth:\s*(\d+)\s+and\s+cost\s+function:\s*(\S+)(?:\s+with\s+(\S+))?\s+occurs\s+in\s+(\d+)',
        re.IGNORECASE
    )
    records = []
    filename = os.path.basename(filepath)

    # e.g. "Col_AES-32-block_norm_Layer_Results"
    #        [0]  [1]            [-3] [-2][-1]
    parts       = filename.split('_')
    greedy_name = parts[0]  # "Col"
    matrix_name = parts[1]  # "AES-32-block"

    with open(filepath, 'r') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                records.append({
                    'cnot':   int(m.group(1)),
                    'depth':  int(m.group(2)),
                    'cost':   m.group(3),
                    'norm':   m.group(4) or 'N/A',
                    'occurs': int(m.group(5)),
                    'greedy': greedy_name,
                    'matrix': matrix_name,
                })
    return records

def plot_by_greedy(all_records):
    # Group by cost function → then by greedy algorithm
    by_cost = defaultdict(lambda: defaultdict(list))
    for r in all_records:
        cost_key = f"{r['cost']}/{r['norm']} [{r['matrix']}]"
        by_cost[cost_key][r['greedy']].append(r)

    colors  = ['#e63946', '#2a9d8f', '#f4a261', '#6a4c93']
    markers = ['o', 's', '^', 'D']

    GREEDY_ORDER = ['Row', 'Col', 'LocalMinima', 'Parallel']

    for cost_key, greedy_dict in by_cost.items():
        greedy_items = sorted(greedy_dict.items(), key=lambda x: GREEDY_ORDER.index(x[0]) if x[0] in GREEDY_ORDER else 99)  # list of (greedy_name, records)

        # 2x2 grid — one subplot per greedy algorithm
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Cost Function: {cost_key}', fontsize=14, fontweight='bold')
        axes_flat = axes.flatten()  # [top-left, top-right, bottom-left, bottom-right]

        for idx, (greedy_name, records) in enumerate(greedy_items):
            ax = axes_flat[idx]

            records_sorted = sorted(records, key=lambda r: r['occurs'])
            x = [r['occurs'] for r in records_sorted]
            y = [r['depth']  for r in records_sorted]

            ax.plot(x, y,
                    color=colors[idx % len(colors)],
                    marker=markers[idx % len(markers)],
                    linewidth=2,
                    markersize=7,
                    markeredgecolor='black',
                    markeredgewidth=0.5)

            ax.set_title(greedy_name, fontsize=12, fontweight='bold',
                         color=colors[idx % len(colors)])
            ax.set_xlabel('Occurs In (iteration)', fontsize=10)
            ax.set_ylabel('Depth', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.4)

        # Hide any unused subplots if fewer than 4 greedy algorithms
        for idx in range(len(greedy_items), 4):
            axes_flat[idx].set_visible(False)

        plt.tight_layout()

        safe_cost = cost_key.replace('/', '_').replace(' ', '').replace('[', '').replace(']', '')
        out = f'plot_{safe_cost}.png'
        plt.savefig(out, dpi=150)
        print(f"Saved: {out}")
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <file1> <file2> <file3> <file4>")
        print(f"   Or: python3 {sys.argv[0]} Results/*_Layer_Results")
        sys.exit(1)

    all_records = []
    for filepath in sys.argv[1:]:
        records = parse_file(filepath)
        greedy = records[0]['greedy'] if records else '?'
        print(f"  {os.path.basename(filepath)}: {len(records)} records  (greedy={greedy})")
        all_records.extend(records)

    if not all_records:
        print("No records found. Check file format.")
        sys.exit(1)

    print(f"\nTotal: {len(all_records)} records across {len(sys.argv)-1} files")
    plot_by_greedy(all_records)
