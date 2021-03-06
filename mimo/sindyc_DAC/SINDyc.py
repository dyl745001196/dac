import warnings
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
from collections import Counter

import pdb

class SINDyc:
    def __init__(self,data,x_dim,u_dim,
                 polyorder=2,usesine=False,sineorder=5,cutoff=0.025,iter_lim=10):

        self._t         = data[:,0]
        self._x         = data[:,1:x_dim+1]
        self._u         = data[:,x_dim+1:]
        self._dx        = []
        self._xdim      = x_dim
        self._udim      = u_dim
        self._polyorder = polyorder
        self._usesine   = usesine
        self._sineorder = sineorder
        self._cutoff    = cutoff
        self._iter_lim  = iter_lim
        self._theta     = []
        self._xi        = []
        self._rx        = []

        print "Initiated a class for Sparse Identification from Numerical Dynamics"

    def ComputeDerivatives(self):
        if self._dx == []:
            print "Write numerical computation of derivatives and set it to self._dx"

            print "no derivative data provided..."
            print "computing derivatives using ... method..."

    def ComputeTheta(self):
        self._theta = self.PoolData(self._x,self._u)
        print "**** Candidate functions library has been created ****"

    def PolyConvolve(self, data1, data2, initialrun=False):

        if (np.shape(data1)[0] != np.shape(data2)[0]):
            warnings.warn("Data dimension mismatch.")

        if not initialrun:
            data1 = data1[:,1:]

        row = []
        res = []

        for n in xrange(np.shape(data1)[0]):
            a, b = data1[n], data2[n]
            for i in xrange(len(a)):
                for j in xrange(min(i,len(b)-1),len(b)):
                    row.append(a[i]*b[j])
            res.append(row)
            row = []

        return np.array(res)

    def PoolData(self,x,u):
        yout = np.ones((np.shape(x)[0],1))
        initialrun = True
        for i in xrange(self._polyorder):
            yout = np.append(yout,self.PolyConvolve(yout,x,initialrun=initialrun),axis=1)
            initialrun = False
        if self._usesine:
            for k in xrange(1,self._sineorder):
                yout = np.append(np.append(yout, np.sin(k*x),axis=1),np.cos(k*x),axis=1)

        yout = np.append(yout, u, axis=1)

        return yout

    def RunSINDyc(self,simulate=False):

        self.ComputeDerivatives()
        self.ComputeTheta()
        self.SparsifyDynamics()
        if simulate:
            self.SimulateSINDy()

    def SetDerivative(self,derdata):
        self._dx = derdata[:,1:]
        print "**** Derivative Set ****"

    def SimulateSINDy(self):
        print "Deprecated, update to include control"
        return

        print "**** Identification is complete. We now use it to simulate the system. ****"
        dt = np.diff(self._t[0:2])[0]
        t0 = self._t[0]
        te = self._t[-1]
        r = ode(self.SparseGalerkin).set_integrator('dopri5', nsteps=1000)
        r.set_initial_value(np.mean(self._x[0:int(0.1/dt)],axis=0), t0)

        while r.successful() and r.t < te-2*dt: #TODO: figure out a better way to do this.
            self._rx.append(np.insert(r.integrate(r.t+dt),0,r.t+dt))

        self._rx = np.array(self._rx)

    def SINDyPlot(self, fignum=1, statesymbols=[],datacolors=[],simcolors=[]):
        print "Deprecated, update to include control"
        return

        if len(statesymbols) != self._dim:
            warnings.warn("The number of state symbols don't match the state dimension.")
            statesymbols = np.arange(self._dim)+1
        if len(datacolors) != self._dim:
            warnings.warn("The number of color specs don't match the state dimension.")
            datacolors = ['b','r','g']

        plt.figure(fignum)
        for i in xrange(self._dim):
            ps = plt.plot(self._t,self._x[:,i],label="{}".format(statesymbols[i]))
            plt.setp(ps, 'Color', datacolors[i], 'linewidth', 3)
            if self._rx != []:
                ps = plt.plot(self._rx[:,0],self._rx[:,i+1],'--')
                plt.setp(ps, 'Color', simcolors[i], 'linewidth', 3,)

        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=3, mode="expand", borderaxespad=0.)
        plt.grid(True)
        plt.show()

    def SparseGalerkin(self,t,y):
        yy = np.array(y).reshape((1,self._xdim+self._udim))
        yPool = self.PoolData(yy)
        return np.dot(yPool,self._xi)

    def SparsifyDynamics(self):
        print "**** Performing regression. Please wait... ****"
        #self._xi = np.dot(np.linalg.pinv(self._theta),self._dx)
        self._xi = np.linalg.lstsq(self._theta,self._dx)[0]
        print "Iteration in progress: ",
        for k in xrange(self._iter_lim):
            # print "{},".format(k+1),
            smallinds = np.abs(self._xi)<self._cutoff
            self._xi[smallinds] = 0
            for ind in range(self._xdim):
                biginds = ~smallinds[:,ind]
                #self._xi[biginds,ind] = np.dot(np.linalg.pinv(self._theta[:,biginds]),self._dx[:,ind])
                self._xi[biginds,ind] = np.linalg.lstsq(self._theta[:,biginds],self._dx[:,ind])[0]
        print ""

    def StringConvolve(self,l1,l2):
        res = []
        for i in xrange(len(l1)):
            for j in xrange(min(i,len(l2)-1),len(l2)):
                if l1[i] == "1":
                    res.append(l2[j])
                else:
                    res.append(l1[i]+l2[j])
        return res

    def StringMultFormat(self,str):
        sortedStr = sorted(str)
        availablesVars = list(set(sortedStr))
        counts = Counter(sortedStr)

        rs = ''

        for i in range(len(availablesVars)):
            power = counts[availablesVars[i]]
            if power == 1:
                rs = rs + availablesVars[i] + " "
            else:
                rs = rs + availablesVars[i]+"^{} ".format(power)
        return rs

    def StringTerms(self,strlist):
        terms = []
        s1 = "1"
        for i in self._polyorder:
            terms.join(self.StringConvolve(s1,strlist))
            s1 = terms

    def StringModelView(self,StateVariables=[], ControlVariables=[]):
        terms = []
        s1 = ["1"]
        for i in range(self._polyorder):
            terms += self.StringConvolve(s1,StateVariables)
            s1 = terms

        if self._usesine:
            for k in xrange(1,self._sineorder):
                for var in StateVariables:
                    terms += ["sin({0}*{1})".format(k, var)]
                for var in StateVariables:
                    terms += ["cos({0}*{1})".format(k, var)]

        terms += ControlVariables

        terms = ["1"] + terms

        for i in xrange(len(StateVariables)):
            if abs(self._xi[0,i]) > 1e-3:
                row = "d"+StateVariables[i]+"/dt = " + "{: 2.3f}".format(self._xi[0,i])
                sp = " + "
            else:
                row = "d"+StateVariables[i]+"/dt = "
                sp = ""

            for j in xrange(1,len(self._xi)):
                ss = "{: 2.2f}".format(self._xi[j,i])
                if abs(self._xi[j,i]) > 1e-3:
                    # if not terms[j] in StateVariables:
                        # row = row + sp + \
                            # "{: 2.3f}".format(self._xi[j,i])+" "+self.StringMultFormat(terms[j])
                    # else:
                    row = row + sp + \
                        "{: 2.3f}".format(self._xi[j,i])+" "+terms[j]
                    sp = " + "
            print row


if __name__ == "__main__":

    # from SIR import *

    '''
        Simulate Data
    '''
    # sir = SIR(tstart=0.001, tend=10, dt=.01, beta=3, gamma=2, N=1)
    # sir.Initialize(S0=0.9, I0=0.1, R0=0);
    # sir.Simulate();

    '''
        Load in data via CSV
    '''
    x_dim = 2
    u_dim = 2

    full_data = np.loadtxt("data/mimo_data_for_sindy1.csv", delimiter=",") # [x, u, x_dot]
    data = full_data[0:500,:x_dim+u_dim]
    ddata = full_data[0:500,x_dim+u_dim:]

    '''
        Add noise to my data
    '''
    eps    = 0.05
    noise  = eps*np.random.randn(data.shape[0],x_dim+u_dim)
    dnoise = eps*np.random.randn(ddata.shape[0],x_dim)
    data += noise
    ddata += dnoise

    '''
        Add time to data
    '''
    data = np.c_[np.asarray([i for i in range(data.shape[0])]), data]
    ddata = np.c_[np.asarray([i for i in range(ddata.shape[0])]), ddata]




    '''
        Run SINDy
    '''
    sin = SINDyc(data=data,
                 x_dim=x_dim,
                 u_dim=u_dim,
                 polyorder=5,
                 sineorder=5,
                 usesine=True,
                 cutoff=.1,
                 iter_lim=500)

    sin.SetDerivative(ddata)
    sin.RunSINDyc(simulate=False)
    # sin.SINDycPlot(statesymbols=["X1","X2"],
              # datacolors=[[0.8, 0.8, 1.0],[1.0, 0.8, 0.8]],
              # simcolors =[[0.0, 0.0, 1.0],[1.0, 0.0, 0.0]])

    sin.StringModelView(["x1","x2"],["u1","u2"])
