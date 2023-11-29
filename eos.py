import numpy as np
import scipy as sp

from data_loader import DataLoader

class EOS:
    def __init__(self, eos_name, q, SNR, encoding_method):
        self.eos_name = eos_name
        self.chirp_mass = 1.17 # solar masses
        self.q = q
        self.m1 = self.chirp_mass * ((1 + self.q) / self.q**3) ** (1 / 5)
        self.encoding_method = encoding_method

        # data = DataLoader('data/' + self.eos_name + '_LAL.dat')
        data = DataLoader('data/' + self.eos_name + '_LAL.tovseq.h5')

        self.ms = data.ms
        self.lambdas = data.lambdas

        self.m2 = self.m1 * self.q

        self.luminosity_distance = self.convert_SNR_to_luminosity_distance(SNR)

    def convert_SNR_to_luminosity_distance(self, SNR):
        luminosity_distance = (30/SNR) * 75
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
              '  "lambda_2": ' + str(self._call(self.m2)) + '\n' +
              '}')

    def prior_dict(self):
        if self.encoding_method == 'l1l2':
            priordict = str('prior-dict={'
                            '  chirp_mass = Gaussian(name="chirp_mass", mu=1.215, sigma=0.1), \n'
                            '  symmetric_mass_ratio = Uniform(name="symmetric_mass_ratio", minimum=0.1, maximum=0.25), \n'
                            '  lambda_tilde = Uniform(name="lambda_tilde", minimum=0, maximum=5000), \n'
                            '  delta_lambda = Uniform(name="delta_lambda", minimum=-500, maximum=1000), \n'
                            '  lambda_1 = Constraint(name="lambda_1", minimum=0, maximum=10000), \n'
                            '  lambda_2 = Constraint(name="lambda_2", minimum=0, maximum=10000), \n'
                            '  chi_1 = 0, \n'
                            '  chi_2 = 0, \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(name="luminosity_distance", minimum=1e2, maximum=8e3, unit="Mpc"), \n'
                            '  dec = -1.2108, \n'
                            '  ra = 1.375, \n'
                            '  theta_jn = 0.4, \n'
                            '  psi = 2.659, \n'
                            '  phase = 1.3 \n'
                            '}')
        elif self.encoding_method == 'binary_love':
            priordict = str('prior-dict={ \n'
                            '  chirp_mass = 1.21504, \n'
                            '  symmetric_mass_ratio = Uniform(name="symmetric_mass_ratio", minimum=0.1, maximum=0.25), \n'
                            '  mass_1 = Constraint(name="mass_1", \n'
                            '  minimum=1,maximum=3), \n'
                            '  mass_2 = Constraint(name="mass_2", minimum=1,maximum=3), \n'
                            '  lambda_symmetric = Uniform(0, 5000, name="lambda_symmetric"), \n'
                            '  binary_love_uniform = Uniform(0.0, 1.0, name="binary_love_uniform"), \n'
                            '  lambda_1 = Constraint(name="lambda_1", minimum=0, maximum=10000), \n'
                            '  lambda_2 = Constraint(name="lambda_2", minimum=0, maximum=10000), \n'
                            '  lambda_antisymmetric = Constraint(name="lambda_antisymmetric", minimum=0,maximum=10000), \n'
                            '  chi_1 = 0, \n'
                            '  chi_2 = 0, \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(name="luminosity_distance", minimum=1e2, maximum=8e3, unit="Mpc"), \n'
                            '  dec = -1.2108, \n'
                            '  ra = 1.375, \n'
                            '  theta_jn = 0.4, \n'
                            '  psi = 2.659, \n'
                            '  phase = 1.3 \n'
                            '}')
        elif self.encoding_method == 'common_radius':
            priordict = str('prior-dict={ \n'
                            '  chirp_mass = bilby.gw.prior.UniformInComponentsChirpMass(name="chirp_mass", minimum=1.485, maximum=1.49, unit="$M_{\odot}$"), \n'
                            '  mass_ratio = bilby.gw.prior.UniformInComponentsMassRatio(name="mass_ratio", minimum=0.125, maximum=1.0), \n'
                            '  mass_1 = Constraint(name="mass_1", minimum=1.001398, maximum=5.31215532473869), \n'
                            '  mass_2 = Constraint(name="mass_2", minimum=1.001398, maximum=5.31215532473869), \n'
                            '  a_1 = 0, \n'
                            '  a_2 = 0, \n'
                            '  tilt_1 = Sine(name="tilt_1"), \n'
                            '  tilt_2 = Sine(name="tilt_2"), \n'
                            '  phi_12 = Uniform(name="phi_12", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  phi_jl = Uniform(name="phi_jl", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  luminosity_distance = bilby.gw.prior.UniformSourceFrame(name="luminosity_distance", minimum=5, maximum=300), \n'
                            '  dec =  Cosine(name="dec"), \n'
                            '  ra =  Uniform(name="ra", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  theta_jn =  Sine(name="theta_jn"), \n'
                            '  psi =  Uniform(name="psi", minimum=0, maximum=np.pi, boundary="periodic"), \n'
                            '  phase = Uniform(name="phase", minimum=0, maximum=2 * np.pi, boundary="periodic"), \n'
                            '  common_radius_uniform = Uniform(0.0, 1.0, name="common_radius_uniform", latex_label="$\mathrm{CR}_{uni}$"), \n'
                            '  lambda_1 = Constraint(name="lambda_1", minimum=0.001,maximum=5000), \n'
                            '  lambda_2 = Uniform(name="lambda_2", minimum=0.001, maximum=5000, latex_label="$\Lambda_2$"), \n'
                            '  lambda_tilde = Constraint(name="lambda_tilde", minimum=0,maximum=5000, latex_label="$\tilde{\Lambda}$") \n'
                            '}')

        return priordict

    def print_injection_dict(self):
        print(self.injection_dict())

    def print_prior_dict(self):
        print(self.prior_dict())