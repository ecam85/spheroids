"""

ecam Mar20

naive kmeans

"""

import background as bg
import time
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt

def get_pixel_list(imlist):
    return np.vstack( [ np.concatenate([ bg.get_ared_crop(im) for im in imlist ]), np.concatenate( [ bg.get_agreen_crop(im) for im in imlist ] ) ] )

def cluster(pixels, means, res):
    for i in xrange(pixels.shape[1]):
        d = [ np.linalg.norm( pixels[:,i] - m ) for m in means ]
        res[i] = np.argmin(d)

def dist(a):
    p = a[0]
    means = a[1]
    d = [ np.linalg.norm( p - m ) for m in means ]
    return np.argmin(d)

def cluster_mp(pixels,means,_):
    pool = mp.Pool(8)

    res = pool.map(dist,[ [pixels[:,i],means] for i in xrange(pixels.shape[1]) ] )

    pool.close()
    pool.join()

    return res

def new_means(pixels,categories,k):
    sums = np.zeros((k,2))
    means = np.zeros((k,2))
    counts = np.zeros(k)

    for i,c in enumerate(categories):
        sums[int(c),:] = sums[int(c),:] + pixels[:,i]
        counts[c] = counts[c] + 1. 

    means[:,0] = sums[:,0] / counts    
    means[:,1] = sums[:,1] / counts

    return means

def iteration(pixels,means,res,k):
    cluster(pixels,means,res)
    return  new_means(pixels,res,k)

def iteration_mp(pixels,means,res,k):
    res = cluster_mp(pixels,means,res)
    return  new_means(pixels,res,k)

def do_iterations(imlist,it=10,verbose=False):
    pixels = get_pixel_list(imlist)
    res = np.empty(pixels.shape[1],dtype=int)
    means = np.array( [ [0,0], [128,128], [256,0] ] )

    for _ in xrange(it):
        if verbose:
            startT = time.time()
        means = iteration(pixels,means,res, means.shape[0] )
       
        if verbose:
            print "Iteration completed in {}s. New mean: {}.".format(time.time()-startT,means)

    return means 

def do_iterations_mp(imlist,means,it=10,verbose=False):
    pixels = get_pixel_list(imlist)
    res = np.empty(pixels.shape[1],dtype=int)

    for _ in xrange(it):
        if verbose:
            startT = time.time()
        means = iteration_mp(pixels,means,res, means.shape[0] )
       
        if verbose:
            print "Iteration completed in {}s. New mean: {}.".format(time.time()-startT,means)

    return means 

def split_pixels(imlist,means):
    pixels = get_pixel_list(imlist)
    res = cluster_mp(pixels,means,0)

    reds = [ [] for _ in xrange(means.shape[0]) ]
    greens = [ [] for _ in xrange(means.shape[0]) ]
    

    for i,c in enumerate(res):
        reds[int(c)].append(pixels[0,i])
        greens[int(c)].append(pixels[1,i])
       
    return reds,greens

def get_neighbouring_cats(i,cats,w):
    row = i / 1024
    col = i % 1024

    indices = []

    minrow = row - w
    maxrow = row + w
    mincol = col - w
    maxcol = col + w

    if minrow < 0:
        minrow = 0
    if maxrow > 998:
        maxrow = 998

    if mincol < 0:
        mincol = 0
    if maxcol > 1024:
        maxcol = 1024

    for rr in xrange(minrow,maxrow):
        for cc in xrange(mincol,maxcol):
            indices.append( [ rr,cc] )

    return [ cats[p[0]*1024+p[1]] for p in indices ] 

def count_cats(cats):
    d = {}
    for c in cats:
        if c not in d:
            d[c] = 0
        d[c] = d[c] + 1

    return [ d[c] for c in sorted(d.keys()) ]

#Category of the surrounding area
def cat_surr(im,km,w=5):
    pixels = get_pixel_list([im])
    r = np.zeros( (4,4) )
    res = cluster_mp(pixels,km,0)

    for i,c in enumerate(res):
        c_surr = np.argmax(count_cats(get_neighbouring_cats(i,res,w)))
        r[int(c),int(c_surr)] = r[int(c),int(c_surr)] + 1

    return r 
  
#Different measures of trafficking 
def my_trafficking(im,km):
    rr = kmeans.cat_surr(im,km,5)

    cancer_cancer = rr[2,2]+rr[1,1]+rr[1,2]+rr[2,1]+rr[2,0]+rr[1,0]
    tcell_cancer = rr[3,2]+rr[3,1]

    return cancer_cancer/(cancer_cancer+tcell_cancer),tcell_cancer/(cancer_cancer+tcell_cancer)


