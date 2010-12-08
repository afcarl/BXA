#!/usr/bin/env python


from sherpa.astro.ui import *
from pyblocxs import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import numpy as np

def splot(x, y, z, xlabel="", ylabel="", zlabel="", color='r'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    tstart = time.time()
    for ii in xrange(len(x)-2):
        
        linecolor = 'b'
        if ii == 0:
            linecolor = 'g'

        ax.plot(x[ii:ii+2],y[ii:ii+2],z[ii:ii+2], c=linecolor)
        ax.scatter([x[ii]], [y[ii]], [z[ii]], c='b',marker='x')

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)

        plt.draw()

    print 'FPS: %f' % (100 / (time.time()-tstart))


def setup():

    load_pha("3c273.pi")

    set_stat('cash')
    set_method('neldermead')

    set_source(xsphabs.abs1*powlaw1d.p1)
    p1.gamma = 2.66
    p1.ampl = .7
    p1.integrate=False
    abs1.nh = 0.06

    notice(0.1,6.0)

    tt = time.time()
    fit()
    print("fit in %s s" % (time.time() - tt))

    tt = time.time()
    covar()
    print("covar in %s s" % (time.time() - tt))


if __name__ == '__main__':

    setup()

    tt = time.time()
    set_sampler('MetropolisMH')
    set_sampler('MH')
    set_sampler_opt('log', [1,0,0])
    stats, accept, params = get_draws(niter=1e2)
    print("'%s' in %s secs" % (get_sampler_name(), time.time() - tt))

    splot(params[0],params[1],stats, "abs.nH", "p1.gamma", "statistic")

    raw_input("Press Return for the next plot...")

    splot(params[1],params[2],stats, "p1.gamma", "p1.ampl", "statistic")

    raw_input("Press Return for the next plot...")

    splot(params[2],params[0],stats, "p1.ampl", "abs1.nH", "statistic")

    raw_input("Press Return to exit")
