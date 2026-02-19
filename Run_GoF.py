import subprocess
import sys


infile = "combine_files/higgsCombine_mass4l_r_smH_0.MultiDimFit.mH125.38.root"
mass   = "125.38"
ntotal  = 500
nsplit = 10
snapshot = "MultiDimFit"
algo = "saturated"


def run(cmd):
    print("\n>>>", cmd)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Command failed!")
        sys.exit(1)


# 1) GOF on data                                                                                                                                                                                                    
run(f"""combine -M GoodnessOfFit {infile} -m {mass} --algo {algo} --snapshotName {snapshot} -n .obs""")


# 2) GOF toys                                                                                                                                                                                                      
for i in range(0,nsplit):
    ntoys = str(ntotal//nsplit)
    run(f"""combine -M GoodnessOfFit {infile} -m {mass} --algo {algo} --snapshotName {snapshot} --toysFrequentist -t {ntoys} -s -1 -n .toys""")


# 3) Collect                                                                                                                                                                                                        
run(f"""combineTool.py -M CollectGoodnessOfFit --input higgsCombine.obs.GoodnessOfFit.mH{mass}.root higgsCombine.toys.GoodnessOfFit.mH{mass}.*.root -m {mass} -o gof.json""")


# 4) Plot                                                                                                                                                                                                          
#run(f"""plotGof.py gof.json --statistic {algo} --mass {mass}.0 -o gof_postfit""")


print("DONE")