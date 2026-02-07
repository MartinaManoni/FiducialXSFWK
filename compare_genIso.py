#!/usr/bin/env python3
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import argparse


def get_array(tree, branch, max_entries=None, pdgid_branch=None, pdgid_target=None):
    """Extract a numpy array from a TTree branch, optionally filtering by PDG ID."""
    arr = []
    n_entries = tree.GetEntries()
    for i, event in enumerate(tree):
        if max_entries and i >= max_entries:
            break
        try:
            val = getattr(event, branch)

            # Apply PDG ID selection if requested
            if pdgid_branch and pdgid_target is not None:
                pdg_vals = getattr(event, pdgid_branch)
                # Keep only entries where |pdgId| == target
                mask = [abs(pid) == pdgid_target for pid in pdg_vals]
                # Handle vector branches
                if hasattr(val, "__len__") and not isinstance(val, (float, int)):
                    selected = [v for v, keep in zip(val, mask) if keep]
                    arr.extend(selected)
                else:
                    # scalar branch — skip unless it matches
                    if mask and mask[0]:
                        arr.append(val)
            else:
                # No filtering
                if hasattr(val, "__len__") and not isinstance(val, (float, int)):
                    arr.extend(val)
                else:
                    arr.append(val)
        except Exception:
            pass
        if (i + 1) % 100000 == 0:
            print(f"  Processed {i+1}/{n_entries} entries...")
    return np.array(arr, dtype=float)


def plot_single(var, data, label, color="blue", nbins=50):
    """Draw a single variable distribution as a histogram, restricted to [0,1]."""
    plt.figure(figsize=(7, 5))

    # Keep only values between 0 and 1
    data = data[(data >= 0) & (data <= 1)]
    bins = np.linspace(0, 1, nbins + 1)

    counts, bins, patches = plt.hist(
        data, bins=bins, color=color, alpha=0.7, label=label,
        histtype='stepfilled', edgecolor='black'
    )

    plt.xlabel(var)
    plt.yscale("log")
    plt.ylabel("Entries")
    plt.xlim(0, 1)
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.tight_layout()

    out_name = f"{label.replace(' ', '_')}_{var}.png"
    plt.savefig(out_name)
    plt.close()
    print(f"→ Saved {out_name}")


def plot_comparison(var, data1, data2, label1, label2, nbins=50):
    """Plot comparison and ratio restricted to [0,1] range."""
    # Keep only data between 0 and 1
    data1 = data1[(data1 >= 0) & (data1 <= 1)]
    data2 = data2[(data2 >= 0) & (data2 <= 1)]

    if len(data1) == 0 or len(data2) == 0:
        print(f"Skipping {var}: no data in [0,1]")
        return

    bins = np.linspace(0, 1, nbins + 1)
    hist1, _ = np.histogram(data1, bins=bins)
    hist2, _ = np.histogram(data2, bins=bins)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    ratio = np.divide(hist1, hist2, out=np.zeros_like(hist1, dtype=float), where=hist2 != 0)

    fig, (ax, axr) = plt.subplots(2, 1, figsize=(7, 6), sharex=True,
                                  gridspec_kw={'height_ratios': [3, 1]})

    ax.hist(bin_centers, bins=bins, weights=hist1, histtype='step', color='blue', label=label1)
    ax.errorbar(bin_centers, hist2, yerr=np.sqrt(hist2), fmt='o', color='red', label=label2)

    ax.set_yscale("log")
    ax.set_ylabel("Entries")
    ax.set_xlim(0, 1)
    ax.legend()
    ax.grid(True, linestyle=":")

    axr.plot(bin_centers, ratio, 'ko', markersize=3)
    axr.axhline(1, color='gray', linestyle='--')
    axr.set_xlabel(var)
    axr.set_ylabel("Ratio")
    axr.set_ylim(0.5, 1.5)
    axr.set_xlim(0, 1)
    axr.grid(True, linestyle=":")

    plt.tight_layout()
    out_name = f"compare_{var}.png"
    plt.savefig(out_name)
    plt.close(fig)
    print(f"→ Saved {out_name}")


def main(file1, file2, var="GenPart_iso", treename="Events", max_entries=None):
    print(f"Opening files:\n  1) {file1}\n  2) {file2}")
    f1 = ROOT.TFile.Open(file1)
    f2 = ROOT.TFile.Open(file2)

    t1 = f1.Get(treename)
    t2 = f2.Get(treename)
    if not t1 or not t2:
        print(f"Error: could not find tree '{treename}' in one of the files.")
        return

    print(f"Reading variable '{var}' from both TTrees...")

    data1 = get_array(t1, var, max_entries, pdgid_branch="GenPart_pdgId", pdgid_target=13)
    data2 = get_array(t2, var, max_entries, pdgid_branch="GenPart_pdgId", pdgid_target=13)

    print(f"  → Entries: Private prod = {len(data1)}, Standard prod = {len(data2)}")

    if len(data1) == 0 or len(data2) == 0:
        print("No valid data found for plotting.")
        return

    label1 = "Private prod 2022 HIG-25-025"
    label2 = "Private prod 2022 HIG-24-013"

    # Individual plots
    plot_single(var, data1, label1, color="blue")
    plot_single(var, data2, label2, color="red")

    # Comparison plot
    plot_comparison(var, data1, data2, label1, label2)

    f1.Close()
    f2.Close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare GenPart_iso variable between two ROOT TTrees.")
    parser.add_argument("file1", help="Path to first ROOT file")
    parser.add_argument("file2", help="Path to second ROOT file")
    parser.add_argument("--tree", default="Events", help="TTree name (default: Events)")
    parser.add_argument("--var", default="GenPart_iso", help="Variable to compare")
    parser.add_argument("--max", type=int, default=None, help="Max entries (optional)")
    args = parser.parse_args()
    main(args.file1, args.file2, args.var, args.tree, args.max)


