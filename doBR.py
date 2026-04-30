import numpy as np

# Mass points                                                                                                                                                                                                                          
m1 = 125.3
m2 = 125.4
m_target = 125.38

# Input data                                                                                                                                                                                                                           
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR#Higgs_2_gauge_bosons                                                                                                                                          
data_125p3 = {
    "value": 2.692E-02,
    "thu_pos": 0.98,
    "thu_neg": 0.98,
    "pumq_pos": 0.99,
    "pumq_neg": 0.96,
    "puas_pos": 0.63,
    "puas_neg": 0.62,
}

data_125p4 = {
    "value": 2.716E-02,
    "thu_pos": 0.98,
    "thu_neg": 0.98,
    "pumq_pos": 0.97,
    "pumq_neg": 0.97,
    "puas_pos": 0.63,
    "puas_neg": 0.63,
}

def interp(x1, x2, y1, y2, x):
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

# Interpolate central value                                                                                                                                                                                                            
value = interp(m1, m2, data_125p3["value"], data_125p4["value"], m_target)

# Interpolate relative uncertainties (%)                                                                                                                                                                                               
thu_pos = interp(m1, m2, data_125p3["thu_pos"],  data_125p4["thu_pos"],  m_target)
thu_neg = interp(m1, m2, data_125p3["thu_neg"],  data_125p4["thu_neg"],  m_target)

pumq_pos = interp(m1, m2, data_125p3["pumq_pos"], data_125p4["pumq_pos"], m_target)
pumq_neg = interp(m1, m2, data_125p3["pumq_neg"], data_125p4["pumq_neg"], m_target)

puas_pos = interp(m1, m2, data_125p3["puas_pos"], data_125p4["puas_pos"], m_target)
puas_neg = interp(m1, m2, data_125p3["puas_neg"], data_125p4["puas_neg"], m_target)

# Total relative uncertainty (%) in quadrature                                                                                                                                                                                         
tot_pos_pct = np.sqrt(thu_pos**2 + pumq_pos**2 + puas_pos**2)
tot_neg_pct = np.sqrt(thu_neg**2 + pumq_neg**2 + puas_neg**2)

# Absolute uncertainties                                                                                                                                                                                                               
tot_pos_abs = value * tot_pos_pct / 100.0
tot_neg_abs = value * tot_neg_pct / 100.0

print(f"Mass = {m_target:.2f} GeV")
print(f"H->ZZ BR = {value:.6E}")
print()
print("Interpolated component uncertainties (%)")
print(f"  THU   : +{thu_pos:.3f}  -{thu_neg:.3f}")
print(f"  PU(mq): +{pumq_pos:.3f}  -{pumq_neg:.3f}")
print(f"  PU(as): +{puas_pos:.3f}  -{puas_neg:.3f}")
print()
print("Total uncertainty")
print(f"  Relative : +{tot_pos_pct:.4f}%  -{tot_neg_pct:.4f}%")
print(f"  Absolute : +{tot_pos_abs:.6E}  -{tot_neg_abs:.6E}")
print()
print(f"Final H->ZZ BR = {value:.6E}  +{tot_pos_abs:.6E}  -{tot_neg_abs:.6E}")

# PDG: https://pdg.lbl.gov/2024/listings/rpp2024-list-z-boson.pdf
# Z -> ll inputs
br_zee = 3.3632e-2
br_zmumu = 3.3662e-2

# absolute uncertainties on Z branching ratios
unc_zee_abs = 0.0042e-2
unc_zmumu_abs = 0.0066e-2

# relative uncertainties (%)
unc_zee_pct = unc_zee_abs / br_zee * 100.0
unc_zmumu_pct = unc_zmumu_abs / br_zmumu * 100.0

# Final-state branching ratios
br_4e = value * br_zee**2
br_4mu = value * br_zmumu**2
br_2e2mu = value * 2.0 * br_zee * br_zmumu

# Total relative uncertainties (%)
# 4e: H->ZZ and two factors of Z->ee
rel_4e_pos = np.sqrt(tot_pos_pct**2 + (2.0 * unc_zee_pct)**2)
rel_4e_neg = np.sqrt(tot_neg_pct**2 + (2.0 * unc_zee_pct)**2)

# 4mu: H->ZZ and two factors of Z->mumu
rel_4mu_pos = np.sqrt(tot_pos_pct**2 + (2.0 * unc_zmumu_pct)**2)
rel_4mu_neg = np.sqrt(tot_neg_pct**2 + (2.0 * unc_zmumu_pct)**2)

# 2e2mu: H->ZZ, one Z->ee, one Z->mumu
rel_2e2mu_pos = np.sqrt(tot_pos_pct**2 + unc_zee_pct**2 + unc_zmumu_pct**2)
rel_2e2mu_neg = np.sqrt(tot_neg_pct**2 + unc_zee_pct**2 + unc_zmumu_pct**2)

# Absolute uncertainties
unc_4e_pos = br_4e * rel_4e_pos / 100.0
unc_4e_neg = br_4e * rel_4e_neg / 100.0

unc_4mu_pos = br_4mu * rel_4mu_pos / 100.0
unc_4mu_neg = br_4mu * rel_4mu_neg / 100.0

unc_2e2mu_pos = br_2e2mu * rel_2e2mu_pos / 100.0
unc_2e2mu_neg = br_2e2mu * rel_2e2mu_neg / 100.0

print()
print("Z branching ratios")
print(f"  Z->ee   = {br_zee:.6E} +/- {unc_zee_abs:.6E} ({unc_zee_pct:.4f}%)")
print(f"  Z->mumu = {br_zmumu:.6E} +/- {unc_zmumu_abs:.6E} ({unc_zmumu_pct:.4f}%)")

print()
print("Final state branching ratios")
print(f"  H->ZZ->4e     = {br_4e:.6E}  +{unc_4e_pos:.6E}  -{unc_4e_neg:.6E}    (+{rel_4e_pos:.4f}%  -{rel_4e_neg:.4f}%)")
print(f"  H->ZZ->4mu    = {br_4mu:.6E}  +{unc_4mu_pos:.6E}  -{unc_4mu_neg:.6E}    (+{rel_4mu_pos:.4f}%  -{rel_4mu_neg:.4f}%)")
print(f"  H->ZZ->2e2mu  = {br_2e2mu:.6E}  +{unc_2e2mu_pos:.6E}  -{unc_2e2mu_neg:.6E}    (+{rel_2e2mu_pos:.4f}%  -{rel_2e2mu_neg:.4f}%)")

# Total H -> 4l (e,mu)
br_4l = br_4e + br_4mu + br_2e2mu

# --- Relative uncertainties (propagated with correlations) ---

# H->ZZ part (fully correlated across all channels)
rel_4l_pos_hzz = tot_pos_pct
rel_4l_neg_hzz = tot_neg_pct

# Z->ee contribution
# appears twice in 4e and once in 2e2mu
coeff_zee = (2*br_4e + br_2e2mu) / br_4l
rel_4l_zee = coeff_zee * unc_zee_pct

# Z->mumu contribution
# appears twice in 4mu and once in 2e2mu
coeff_zmumu = (2*br_4mu + br_2e2mu) / br_4l
rel_4l_zmumu = coeff_zmumu * unc_zmumu_pct

# Total relative uncertainties
rel_4l_pos = np.sqrt(rel_4l_pos_hzz**2 + rel_4l_zee**2 + rel_4l_zmumu**2)
rel_4l_neg = np.sqrt(rel_4l_neg_hzz**2 + rel_4l_zee**2 + rel_4l_zmumu**2)

# Absolute uncertainties
unc_4l_pos = br_4l * rel_4l_pos / 100.0
unc_4l_neg = br_4l * rel_4l_neg / 100.0

print()
print(f"  H->ZZ->4l (e,mu) = {br_4l:.6E}  +{unc_4l_pos:.6E}  -{unc_4l_neg:.6E}    (+{rel_4l_pos:.4f}%  -{rel_4l_neg:.4f}%)")