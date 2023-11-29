from eos import EOS
from ini_generator import INIGenerator
import matplotlib.pyplot as plt

eos_names = ['H4', 'MS1', 'WFF1']
mass_ratios = [1, 0.85, 0.65, 0.5]
SNRs = [15, 30]
encoding_methods = ['l1l2', 'binary_love', 'common_radius']

bash_script = open('ini_files_to_recreate_plots/launch_ini_files.sh', 'w')

bash_script.write('# to make script an executable: run \'chmod +x launch_ini_files.sh\', then execute using \'bash launch_ini_files.sh\' \n')

for eos_name in eos_names:
    for mass_ratio in mass_ratios:
        for SNR in SNRs:
            for encoding_method in encoding_methods:
                label = eos_name + '_massratio' + str(int(mass_ratio * 100)) + '_SNR' + str(SNR) + '_' + encoding_method
                eos = EOS(eos_name=eos_name, q=mass_ratio, SNR=SNR, encoding_method=encoding_method)
                ini_generator = INIGenerator(injectiondict=eos.injection_dict(), priordict=eos.prior_dict(),
                                             label=label)
                ini_generator.write_changes(save=True)

                bash_script.write('bilby_pipe /home/kyle.wong/ini_files_to_recreate_plots/' + label + '.ini --submit' + '\n')


print('done')

# eos = EOS(eos_name=eos_names[0], q=mass_ratios[3], SNR=SNRs[0], encoding_method=encoding_methods[0])
#
# print(eos.m1, eos.m2)
#
# fig, ax = plt.subplots(1, 1)
# eos.plot_lambda_vs_m(ax=ax)
# plt.yscale('log')
# plt.show()