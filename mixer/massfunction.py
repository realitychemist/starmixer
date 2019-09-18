import scipy.integrate as integrate
import math

class L3:
    # Default L3 IMF values are defined in https://arxiv.org/pdf/1212.0939.pdf, except for the normalization factor.
    # The normalization factor was derived by integrating the L3 IMF over the range [0,1] and setting this equal to 1.
    def __init__(self, alpha = 2.3, beta = 1.4,
                 mu = 0.2, normal = 2.723881205):
        self.alpha = alpha
        self.beta = beta
        self.mu = mu
        self.normal = normal

    def pdf(self, x):
        return (self.normal
                * (x/self.mu)**(-1*self.alpha)
                * (1+(x/self.mu)**(1-self.alpha))**(-1*self.beta))

    # This method is used to set self.normal automatically, in case parameters or bounds of integration are changed.
    def renomalize(self, min, max):
        total_prob = integrate.quad(lambda x: self.normal
                        * (x/self.mu)**(-1*self.alpha)
                        * (1+(x/self.mu)**(1-self.alpha))**(-1*self.beta),
                        min, max)[0]
        if math.isclose(1, total_prob):
            pass
        else:
            integrated = total_prob/self.normal
            self.normal = 1/integrated
