#!/usr/bin/env python3

import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import itertools as it
import re

matplotlib.rc('font', family='sans-serif', size=11)
matplotlib.rc('axes', titlesize='medium', labelsize='medium')
matplotlib.rc('xtick', labelsize='small')
matplotlib.rc('ytick', labelsize='small')

def getresults(path):
    with open(path) as f:
        v = np.fromiter(it.chain.from_iterable(
            re.match(r'(\d+) (\d+) = (\d+) (\d+) (\d+) (\d+)', line).groups()
            for line in f), np.uint64)
        v.shape = v.shape[0]//6,6

    v.shape = 13,11,6
    return v

def plotall(vs, n, name):
    Xs = [np.log2(v[:,:,0]) for v in vs]
    Ys = [np.log2(v[:,:,1]) for v in vs]
    Zs = [np.log2(v[:,:,n+2]) for v in vs]

    ax = fig.add_subplot(gs[0,n], projection='3d')
    ax.set_title(name, y=1.06)

    for i,(X,Y,Z) in enumerate(zip(Xs,Ys,Zs)):
        ax.plot_surface(X, Y, Z, color='C%d'%i, alpha=0.25)
        ax.plot_wireframe(X, Y, Z, color='C%d'%i)

    ax.view_init(None, 345)

    ax.set_xlabel('file count')
    ax.set_xlim(0, 12)
    ax.set_ylabel('file size')
    ax.set_ylim(2, 12)
    #ax.set_zlabel('multiplicative cost')
    ax.set_zlim(0, None)
    ax.set_xticklabels(['$2^{%d}$' % i for i in range(0,14,2)])
    ax.set_yticklabels(['$2^{%d}$' % i for i in range(2,14,2)])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax = fig.add_subplot(gs[1,n])
    #ax.set_title('File storage cost')

    #ax.plot(v[0][:,0], v[0][:,5])

    for i,(X,Y,Z) in enumerate(zip(Xs,Ys,Zs)):
        ax.plot(X[:,0], np.mean(Z, axis=1), color='C%d'%i)



    #ax.set_xlabel('file count')
    ax.set_xlim(0, 12)
    #ax.set_ylabel('multiplicative cost')
    ax.set_ylim(0, None)
    ax.set_xticklabels(['$2^{%d}$' % i for i in range(0,14,2)])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


    ###
    ax = fig.add_subplot(gs[2,n])
    #ax.set_title('File storage cost')

    #ax.plot(v[0][:,0], v[0][:,5])

    for i,(X,Y,Z) in enumerate(zip(Xs,Ys,Zs)):
        ax.plot(Y[0,:], np.mean(Z, axis=0), color='C%d'%i)

    #ax.set_xlabel('file size')
    ax.set_xlim(2, 12)
    #ax.set_ylabel('multiplicative cost')
    ax.set_ylim(0, None)
    ax.set_xticklabels(['$2^{%d}$' % i for i in range(2,14,2)])

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)







v1 = getresults('v1.results')
v2 = getresults('v2.results')

gs = gridspec.GridSpec(nrows=3, ncols=4,
        wspace=0.25, hspace=0.25)

fig = plt.figure(figsize=(4*6/1.5,3*3.5/1.5))

#ax.plot(v[0][:,0], v[0][:,5])
v1[:,:,2] = v1[:,:,2] / (v1[:,:,0]*v1[:,:,1])
v2[:,:,2] = v2[:,:,2] / (v2[:,:,0]*v2[:,:,1])
v1[:,:,3] = v1[:,:,3] / (v1[:,:,0]*v1[:,:,1])
v2[:,:,3] = v2[:,:,3] / (v2[:,:,0]*v2[:,:,1])
v1[:,:,4] = v1[:,:,4] / (v1[:,:,0]*v1[:,:,1])
v2[:,:,4] = v2[:,:,4] / (v2[:,:,0]*v2[:,:,1])
v1[:,:,5] = v1[:,:,5] / (v1[:,:,0]*v1[:,:,1])
v2[:,:,5] = v2[:,:,5] / (v2[:,:,0]*v2[:,:,1])

for i, name in enumerate(['read cost', 'prog cost', 'erase cost', 'storage cost']):
    plotall([v1, v2], i, name)

fig.suptitle('littlefs comparison - simulated NOR flash', x=0.10, y=0.98, ha='left')
fig.text(0.10, 0.934, 'read_size=1, prog_size=1, block_size=4096', ha='left')
fig.text(0.085, 0.36, 'multiplicative cost', ha='center', va='center', rotation='vertical')
fig.text(0.5, 0.335, 'file count', ha='center', va='center')
fig.text(0.5, 0.06, 'file size', ha='center', va='center')
fig.legend(handles=[
        Line2D([0], [0], color='C0', label='v1'),
        Line2D([0], [0], color='C1', label='v2')],
    labels=['v1', 'v2'], loc='upper right',
    bbox_to_anchor=[0.843, 0.965], frameon=False)


#
#X1, Y1, Z1 = np.log2(v1[:,:,0]), np.log2(v1[:,:,1]), v1[:,:,2]
#X2, Y2, Z2 = np.log2(v2[:,:,0]), np.log2(v2[:,:,1]), v2[:,:,2]
#ax.plot_surface(X1, Y1, Z1, color='C0', alpha=0.25)
#ax.plot_surface(X2, Y2, Z2, color='C1', alpha=0.25)
#ax.plot_wireframe(X1, Y1, Z1, color='C0')
#ax.plot_wireframe(X2, Y2, Z2, color='C1')
#
##ax.view_init(None, 340)
#
#ax.set_xlabel('file size')
#ax.set_xlim(0, None)
#ax.set_ylabel('multiplicative cost')
#ax.set_ylim(0, None)
#ax.set_zlabel('multiplicative cost')
#ax.set_zlim(0, None)
##
##xticks = np.arange(0, 80+1, 16)
##ax.set_xticks(xticks)
##ax.set_xticklabels(['%dKiB' % ((t*(4096/16))/1024) for t in xticks])
##yticks = np.arange(0, 6+1, 2)
##ax.set_yticks(yticks)
##ax.set_yticklabels(['%dx' % t for t in yticks])
#
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#
####
#
#ax = fig.add_subplot(gs[1,0])
##ax.set_title('File storage cost')
#
##ax.plot(v[0][:,0], v[0][:,5])
#
#X1, Y1 = np.log2(v1[:,0,0]), np.mean(v1[:,:,2], axis=0)
#X2, Y2 = np.log2(v2[:,0,0]), np.mean(v2[:,:,2], axis=0)
#ax.plot(X1, Y1, color='C0')
#ax.plot(X2, Y2, color='C1')
#
#
#ax.set_xlabel('file size')
##ax.set_xlim(0, 80)
#ax.set_ylabel('multiplicative cost')
##ax.set_ylim(0, 6)
##
##xticks = np.arange(0, 80+1, 16)
##ax.set_xticks(xticks)
##ax.set_xticklabels(['%dKiB' % ((t*(4096/16))/1024) for t in xticks])
##yticks = np.arange(0, 6+1, 2)
##ax.set_yticks(yticks)
##ax.set_yticklabels(['%dx' % t for t in yticks])
#
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#
#
####
#ax = fig.add_subplot(gs[2,0])
##ax.set_title('File storage cost')
#
##ax.plot(v[0][:,0], v[0][:,5])
#
#X1, Y1 = np.log2(v1[0,:,1]), np.mean(v1[:,:,2], axis=1)
#X2, Y2 = np.log2(v2[0,:,1]), np.mean(v2[:,:,2], axis=1)
#ax.plot(X1, Y1, color='C0')
#ax.plot(X2, Y2, color='C1')
#
#
#ax.set_xlabel('file size')
##ax.set_xlim(0, 80)
#ax.set_ylabel('multiplicative cost')
##ax.set_ylim(0, 6)
##
##xticks = np.arange(0, 80+1, 16)
##ax.set_xticks(xticks)
##ax.set_xticklabels(['%dKiB' % ((t*(4096/16))/1024) for t in xticks])
##yticks = np.arange(0, 6+1, 2)
##ax.set_yticks(yticks)
##ax.set_yticklabels(['%dx' % t for t in yticks])
#
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)

#fig.tight_layout()
plt.savefig('comparison.svg', bbox_inches="tight")

