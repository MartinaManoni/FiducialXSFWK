#!/usr/bin/env python3
import ROOT
import numpy as np
import matplotlib.pyplot as plt

def get_branch_names(tree):
    """Return a list of branch names in a TTree."""
    return [b.GetName() for b in tree.GetListOfBranches()]

def get_array(tree, branch, max_entries=None):
    """Extract a numpy array from a TTree branch."""
    arr = []
    for i, event in enumerate(tree):
        if max_entries and i >= max_entries:
            break
        arr.append(getattr(event, branch))
    return np.array(arr)

def plot_comparison(var, data1, data2, file1_label, file2_label, nbins=50):
    """Plot comparison and ratio for one variable."""
    minv = min(np.min(data1), np.min(data2))
    maxv = max(np.max(data1), np.max(data2))
    if minv == maxv:
        print(f"  Skipping {var}: constant values")
        return

    hist1, bins = np.histogram(data1, bins=nbins, range=(minv, maxv))
    hist2, _ = np.histogram(data2, bins=bins)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    n1 = len(data1)
    n2 = len(data2)
    print(f"  {var}: {file1_label} entries = {n1}, {file2_label} entries = {n2}")

    ratio = np.divide(hist1, hist2, out=np.zeros_like(hist1, dtype=float), where=hist2 != 0)

    fig, (ax, axr) = plt.subplots(2, 1, figsize=(7,6), sharex=True,
                                  gridspec_kw={'height_ratios':[3,1]})
    ax.hist(bin_centers, bins=bins, weights=hist1, histtype='step', color='blue', label=file1_label)
    ax.errorbar(bin_centers, hist2, yerr=np.sqrt(hist2), fmt='o', color='red', label=file2_label)
    ax.set_ylabel("Entries")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, linestyle=":")

    axr.plot(bin_centers, ratio, 'ko', markersize=3)
    axr.axhline(1, color='gray', linestyle='--')
    axr.set_xlabel(var)
    axr.set_ylabel("Ratio")
    axr.set_ylim(0.5, 1.5)
    axr.grid(True, linestyle=":")
    plt.tight_layout()
    plt.savefig(f"compare_{var}.png")
    plt.close(fig)
    print(f"  → Saved compare_{var}.png")

def main(file1, file2, treename="ZZTree/candTree", variables=None, max_entries=None):
    f1 = ROOT.TFile.Open(file1)
    f2 = ROOT.TFile.Open(file2)
    t1 = f1.Get(treename)
    t2 = f2.Get(treename)

    all_vars1 = set(get_branch_names(t1))
    all_vars2 = set(get_branch_names(t2))
    common_vars = sorted(list(all_vars1 & all_vars2))

    if variables:
        vars_to_compare = [v for v in variables if v in common_vars]
        missing = [v for v in variables if v not in common_vars]
        if missing:
            print(f"⚠️ Warning: these variables not found in both trees: {', '.join(missing)}")
    else:
        vars_to_compare = common_vars[:5]  # fallback

    print(f"Comparing {len(vars_to_compare)} variables:")
    print(", ".join(vars_to_compare))

    for var in vars_to_compare:
        try:
            data1 = get_array(t1, var, max_entries)
            data2 = get_array(t2, var, max_entries)
            if len(data1) == 0 or len(data2) == 0:
                print(f"  Skipping {var} (empty arrays)")
                continue
            plot_comparison(var, data1, data2, "Private prod", "Standard prod")
        except Exception as e:
            print(f"  Skipping {var}: {e}")

    f1.Close()
    f2.Close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compare selected variables between two ROOT TTrees.")
    parser.add_argument("file1")
    parser.add_argument("file2")
    parser.add_argument("--tree", default="ZZTree/candTree", help="Path to TTree (default: ZZTree/candTree)")
    parser.add_argument("--vars", nargs="+", help="Variables to compare (space-separated)")
    parser.add_argument("--max", type=int, default=None, help="Max entries to read (for testing)")
    args = parser.parse_args()
    main(args.file1, args.file2, args.tree, args.vars, args.max)


