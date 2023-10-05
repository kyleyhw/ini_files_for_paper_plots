from eos import EOS
import numpy as np

class INIGenerator:
    def __init__(self, injectiondict, priordict, label):
        self.injectiondict = injectiondict
        self.priordict = priordict
        self.label = label

        filename = 'template.ini'

        with open(filename) as f:
            self.lines = f.read().split('\n')

    def _find_index(self, parameter):
        string = str(parameter + '=')
        index = np.nonzero([line[:len(string)] == string for line in self.lines])[0][0]
        return index

    def _change_label(self, label):
        label_index = self._find_index('label')
        self.lines[label_index] = label

    def _change_outdir(self, outdir):
        outdir_index = self._find_index('outdir')
        self.lines[outdir_index] = outdir

    def _change_injection_dict(self, injectiondict):
        injectiondict_index = self._find_index('injection-dict')
        self.lines[injectiondict_index] = injectiondict

    def _change_prior_dict(self, priordict):
        priordict_index = self._find_index('prior-dict')
        self.lines[priordict_index] = priordict

    def write_injection_dict(self, save=False):
        self._change_label(self.label)
        self._change_outdir(self.label)
        self._change_injection_dict(self.injectiondict)
        self._change_prior_dict(self.priordict)
        if save:
            file = open(str('ini_files/' + self.label + '.ini'), 'w')
            for line in self.lines:
                file.write(line + '\n')
            file.close()