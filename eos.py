import numpy as np
import scipy as sp

from data_loader import DataLoader

class EOS:
    def __init__(self, eos_name, m1, q, SNR, encoding_method):
        self.eos_name = eos_name
        self.m1 = m1
        self.q = q
        self.encoding_method = encoding_method

        data = DataLoader('data/' + self.eos_name + '_LAL.dat')
        # data = DataLoader('data/' + eos_name + '_LAL.tovseq.h5')

        self.ms = data.ms
        self.lambdas = data.lambdas

        self.m2 = self.m1 * self.q

        self.luminosity_distance = self.convert_SNR_to_luminosity_distance(SNR)

    def convert_SNR_to_luminosity_distance(self, SNR):
        luminosity_distance = (30/SNR) * 100
        return luminosity_distance
    def _call(self, m):
        lambda_f = sp.interpolate.interp1d(x=self.ms, y=self.lambdas)
        return lambda_f(m)

    def __call__(self, m):
        return np.vectorize(self._call)(m)

    def plot_lambda_vs_m(self, ax, **kwargs):
        ax.plot(self.ms, self.lambdas, **kwargs)

    def injection_dict(self):
        return str('injection-dict={'
              '  "mass_1": ' + str(self.m1) + ', \n' +
              '  "mass_2": ' + str(self.m2) + ', \n' +
              '  "theta_jn": 0.4, \n'
              '  "luminosity_distance": ' + str(self.luminosity_distance) + ', \n' +
              '  "psi": 2.659, \n'
              '  "ra": 1.375, \n'
              '  "dec": -1.2108, \n'
              '  "phase": 1.3, \n'
              '  "geocent_time": 1126259642.413, \n'
              '  "reference_frequency": 50, \n'
              '  "chi_1": 0.0, \n'
              '  "chi_2": 0.0,  \n'
              '  "lambda_1": ' + str(self._call(self.m1)) + ', \n' +
              '  "lambda_2": ' + str(self._call(self.m2)) + ', \n' +
              '}')

    def prior_dict(self):
        if self.encoding_method == 'l1l2':
            priordict = str('prior-dict={'
                            '  chirp_mass = Gaussian(eos_name="chirp_mass", mu=1.215, sigma=0.1), \n'
                            '  symmetric_mass_ratio = Uniform(eos_name="symmetric_mass_ratio", minimum=0.1, maximum=0.25), \n'
                            '  lambda_tilde = Uniform(eos_name="lambda_tilde", minimum=0, maximum=5000), \n'
                            '  delta_lambda = Uniform(eos_name="delta_lambda", minimum=-500, maximum=1000), \n'
                            '  lambda_1 = Constraint(eos_name="lambda_1", minimum=0, maximum=10000), \n'
                            '  lambda_2 = Constraint(eos_name="lambda_2", minimum=0, maximum=10000), \n'
                            '  chi_1 = 0.02, \n'
                            '  chi_2 = 0.02, \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(eos_name="luminosity_distance", minimum=1e2, maximum=8e3, unit="Mpc"), \n'
                            '  dec = -1.2108, \n'
                            '  ra = 1.375, \n'
                            '  theta_jn = 0.4, \n'
                            '  psi = 2.659, \n'
                            '  phase = 1.3 \n'
                            '}')
        elif self.encoding_method == 'binary_love':
            priordict = str('prior-dict={ \n'
                            '  chirp_mass = 1.21504, \n'
                            '  symmetric_mass_ratio = Uniform(eos_name="symmetric_mass_ratio", minimum=0.1, maximum=0.25), \n'
                            '  mass_1 = Constraint(eos_name="mass_1", \n'
                            '  minimum=1,maximum=3), \n'
                            '  mass_2 = Constraint(eos_name="mass_2", minimum=1,maximum=3), \n'
                            '  lambda_symmetric = Uniform(0, 5000, eos_name="lambda_symmetric"), \n'
                            '  binary_love_uniform = Uniform(0.0, 1.0, eos_name="binary_love_uniform"), \n'
                            '  lambda_1 = Constraint(eos_name="lambda_1", minimum=0, maximum=10000), \n'
                            '  lambda_2 = Constraint(eos_name="lambda_2", minimum=0, maximum=10000), \n'
                            '  lambda_antisymmetric = Constraint(eos_name="lambda_antisymmetric", minimum=0,maximum=10000), \n'
                            '  chi_1 = 0, \n'
                            '  chi_2 = 0, \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(eos_name="luminosity_distance", minimum=1e2, maximum=8e3, unit="Mpc"), \n'
                            '  dec = -1.2108, \n'
                            '  ra = 1.375, \n'
                            '  theta_jn = 0.4, \n'
                            '  psi = 2.659, \n'
                            '  phase = 1.3 \n'
                            '}')
        elif self.encoding_method == 'common_radius':
            priordict = str('prior-dict={ \n'
                            '  chirp_mass = bilby.gw.prior.UniformInComponentsChirpMass(eos_name="chirp_mass", minimum=1.485, maximum=1.49, unit="$M_{\odot}$"), \n'
                            '  mass_ratio = bilby.gw.prior.UniformInComponentsMassRatio(eos_name="mass_ratio", minimum=0.125, maximum=1.0), \n'
                            '  mass_1 = Constraint(eos_name="mass_1", minimum=1.001398, maximum=5.31215532473869), \n'
                            '  mass_2 = Constraint(eos_name="mass_2", minimum=1.001398, maximum=5.31215532473869), \n'
                            '  a_1 = 0, \n'
                            '  a_2 = 0, \n'
                            '  tilt_1 = Sine(eos_name="tilt_1"), \n'
                            '  tilt_2 = Sine(eos_name="tilt_2"), \n'
                            '  phi_12 = Uniform(eos_name="phi_12", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  phi_jl = Uniform(eos_name="phi_jl", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(eos_name="luminosity_distance", minimum=5, maximum=300), \n'
                            '  dec =  Cosine(eos_name="dec"), \n'
                            '  ra =  Uniform(eos_name="ra", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  theta_jn =  Sine(eos_name="theta_jn"), \n'
                            '  psi =  Uniform(eos_name="psi", minimum=0, maximum=np.pi, boundary="periodic"), \n'
                            '  phase = Uniform(eos_name="phase", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  common_radius_uniform = Uniform(0.0, 1.0, eos_name="common_radius_uniform", latex_label="$\mathrm{CR}_{uni}$"), \n'
                            '  lambda_1 = Constraint(eos_name="lambda_1", minimum=0.001,maximum=5000), \n'
                            '  lambda_2 = Uniform(eos_name="lambda_2", minimum=0.001, maximum=5000, latex_label="$\Lambda_2$"), \n'
                            '  lambda_tilde = Constraint(eos_name="lambda_tilde", minimum=0,maximum=5000, latex_label="$\tilde{\Lambda}$") \n'
                            '}')

        return priordict

    def print_injection_dict(self):
        print(self.injection_dict())

    def print_prior_dict(self):
        print(self.prior_dict())