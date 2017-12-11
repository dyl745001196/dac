import numpy as np
import math
import matplotlib.pylab as plt

'''
Structure for this System class modified from and inspired by:
    https://github.com/sahandha/SINDy
'''

class System:
    '''
    Simple template for defining systems.
    '''
    def __init__(self, t_start, t_end, dt):

        self._t_start = t_start;
        self._dt     = dt;
        self._t_end   = t_end;

        # INSERT STATE VARIABLE INIT HERE

    def Update(self):
        '''
        Update state variables here according to system dynamics
        '''

        # WRITE SYSTEM UPDATES HERE
        pass

    def Initialize(self):

        # INSERT SYSTEM SIMULATION INITIALIZATION HERE

        self._Time = np.arange(self._t_start,self._t_end,self._dt);

        self._SS   = np.zeros(len(self._Time));
        self._II   = np.zeros(len(self._Time));
        self._RR   = np.zeros(len(self._Time));

        self._dSS  = np.zeros(len(self._Time));
        self._dII  = np.zeros(len(self._Time));
        self._dRR  = np.zeros(len(self._Time));

    def Simulate(self):
        for ii in range(len(self._Time)):
            self._SS[ii] = self._S;
            self._II[ii] = self._I;
            self._RR[ii] = self._R;

            self._dSS[ii] = self._dS;
            self._dII[ii] = self._dI;
            self._dRR[ii] = self._dR;

            self.Update();

    def PlotSIR(self, num):
        plt.figure(num)
        ps = plt.plot(self._Time,self._SS,label="Susceptible");
        plt.setp(ps, 'Color', 'b', 'linewidth', 3)
        pi = plt.plot(self._Time,self._II,label="Infected");
        plt.setp(pi, 'Color', 'r', 'linewidth', 3)
        pr = plt.plot(self._Time,self._RR,label="Recovered");
        plt.setp(pr, 'Color', 'g', 'linewidth', 3)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
        plt.grid(True)

    def PlotDSIR(self, num):
        plt.figure(num)
        ps = plt.plot(self._Time,self._dSS,label="Susceptible");
        plt.setp(ps, 'Color', 'b', 'linewidth', 3)
        pi = plt.plot(self._Time,self._dII,label="Infected");
        plt.setp(pi, 'Color', 'r', 'linewidth', 3)
        pr = plt.plot(self._Time,self._dRR,label="Recovered");
        plt.setp(pr, 'Color', 'g', 'linewidth', 3)
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
        plt.grid(True)


if __name__ == "__main__":
    sir = SIR(0,8,.01,.8,1.2,100);
    sir.Initialize(999,1,0);
    sir.Simulate();
    sir.PlotSIR(1)
    plt.show()
