from eos import EOS
from ini_generator import INIGenerator
import matplotlib.pyplot as plt

eos_names = ['H4', 'MS1', 'WFF1']
mass_ratios = [1, 0.85, 0.65, 0.5]
SNRs = [15, 30]
encoding_methods = ['l1l2', 'binary_love', 'common_radius']

for eos_name in eos_names:
    for mass_ratio in mass_ratios:
        for SNR in SNRs:
            for encoding_method in encoding_methods:
                label = eos_name + '_massratio' + str(mass_ratio * 100) + '_SNR' + str(SNR) + '_' + encoding_method
                eos = EOS(eos_name=eos_name, m1=1, q=mass_ratio, SNR=SNR, encoding_method=encoding_method)
                ini_generator = INIGenerator(injectiondict=eos.injection_dict(), priordict=eos.prior_dict(),
                                             label=label)
                ini_generator.write_injection_dict(save=True)

# fig, ax = plt.subplots(1, 1)
# eos.plot_lambda_vs_m(ax=ax)
# plt.xscale('log')
# plt.yscale('log')
# plt.show()

