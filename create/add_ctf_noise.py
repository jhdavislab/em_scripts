'''
Corrupt particle images with structural noise, CTF, digital/shot noise
Written by Ellen Zhong, Emily Navarrete, and Joey Davis
'''

import argparse
import numpy as np
import sys, os
import pickle
from datetime import datetime as dt

from cryodrgn.ctf import compute_ctf_np as compute_ctf
import mrc
from cryodrgn import utils

log = utils.log

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('particles', help='Input MRC stack')
    parser.add_argument('--snr1', default=1.4, type=float, help='SNR for first pre-CTF application of noise (default: %(default)s)')
    parser.add_argument('--snr2', default=0.05, type=float, help='SNR for second post-CTF application of noise (default: %(default)s)')
    parser.add_argument('--s1', type=float, help='Override --snr1 with gaussian noise stdev')
    parser.add_argument('--s2', type=float, help='Override --snr2 with gaussian noise stdev')
    parser.add_argument('--seed', type=int, default=0, help='Random seed for sampling defocus values (default: %(default)s)')
    parser.add_argument('-o', required=True, type=os.path.abspath, help='Output .mrcs')
    parser.add_argument('--out-star', type=os.path.abspath, help='Output star file (default: [output mrcs filename].star)')
    parser.add_argument('--out-pkl', type=os.path.abspath, help='Output pkl file (default: [output mrcs filename].pkl)')
    parser.add_argument('--Nimg', type=int, default=None, help='Number of particle to use (should be <= number of particles in the input mrc stack')

    group = parser.add_argument_group('CTF parameters')
    group.add_argument('--Apix', type=float, help='Pixel size (A/pix)')
    group.add_argument('--ctf-pkl', metavar='pkl', help='Use ctf parameters from a cryodrgn ctf pkl')
    group.add_argument('--df-file', metavar='pkl', help='Use defocus parameters from a pkl file of a Nx2 np.array of values')
    group.add_argument('--kv', default=300, type=float, help='Microscope voltage (kV) (default: %(default)s)')
    group.add_argument('--dfu', default=15000, type=float, help='Defocus U (A) (default: %(default)s)')
    group.add_argument('--dfv', default=15000, type=float, help='Defocus V (A) (default: %(default)s)')
    group.add_argument('--ang', default=0, type=float, help='Astigmatism angle (deg) (default: %(default)s)')
    group.add_argument('--cs', default=2, type=float, help='Spherical aberration (mm) (default: %(default)s)')
    group.add_argument('--wgh', default=0.1, type=float, help='Amplitude constrast ratio (default: %(default)s)')
    group.add_argument('--ps', default=0, type=float, help='Phase shift (deg) (default: %(default)s)')
    group.add_argument('-b', default=100, type=float, help='B factor for Gaussian envelope (A^2) (default: %(default)s)')
    group.add_argument('--sample-df', type=float, help='Jiggle defocus per image with this stdev (default: None)')
    group.add_argument('--no-astigmatism', action='store_true', help='Keep dfu and dfv the same per particle')
    group.add_argument('--normalize', action='store_true', help='Normalize particle stack to have a mean 0 and std 1')
    group.add_argument('--noinvert', default=False, action='store_true', help='Do not invert the images. Default is to invert, which is common/correct for cryosparc')
    return parser

# todo - switch to cryodrgn starfile api
def write_starfile(out, mrc, Nimg, df, kv, wgh, cs, Apix, metadata=None):
    header = [ 
    'data_images',
    'loop_',
    '_rlnImageName',
    '_rlnDefocusU',
    '_rlnDefocusV',
    '_rlnDefocusAngle',
    '_rlnVoltage',
    '_rlnAmplitudeContrast',
    '_rlnSphericalAberration',
    '_rlnPhaseShift',
    '_rlnDetectorPixelSize']

    if metadata is not None:
        header.extend(['_rlnEuler1','_rlnEuler2','_rlnEuler3\n'])
        metadata = pickle.load(open(metadata,'rb'))
        assert len(metadata) == Nimg
    else:
        header[-1] += '\n'
    lines = []
    filename = os.path.basename(mrc)
    for i in range(Nimg):
        line = ['{:06d}@{}'.format(i+1,filename),
                '{:1f}'.format(df[i][0]),
                '{:1f}'.format(df[i][1]),
                '{:1f}'.format(df[i][2]),
                kv, wgh, cs,
                '{:1f}'.format(df[i][3]),
                Apix]
        if metadata is not None:
            line.extend(metadata[i])
        lines.append(' '.join([str(x) for x in line]))
    f = open(out, 'w')
    f.write('# Created {}\n'.format(dt.now()))
    f.write('\n'.join(header))
    f.write('\n'.join(lines))
    f.write('\n')



def add_noise(particles, D, sigma):
    particles += np.random.normal(0,sigma,particles.shape)
    return particles

def compute_full_ctf(D, Nimg, args):
    freqs = np.arange(-D/2,D/2)/(args.Apix*D)
    x0, x1 = np.meshgrid(freqs,freqs)
    freqs = np.stack([x0.ravel(),x1.ravel()],axis=1)
    if args.ctf_pkl: # todo: refator
        params = pickle.load(open(args.ctf_pkl,'rb'))
        try: 
            assert len(params) == Nimg
        except AssertionError:
            log('Note that the input ctf.pkl contains '+ str(len(params)) + ' particles, but that you have only chosen to output the first ' + str(Nimg) + ' particle')
            params = params[:Nimg]
        ctf = np.array([compute_ctf(freqs, *x[2:], args.b) for x in params])
        ctf = ctf.reshape((Nimg, D, D))
        df1 = np.array([x[2] for x in params])
        df2 = np.array([x[3] for x in params])
        dfa = np.array([x[4] for x in params])
        dfp = np.array([x[8] for x in params])
        df = np.stack([df1,df2, dfa, dfp], axis=1)
    elif args.df_file:
        raise NotImplementedError

#        df = pickle.load(open(args.df_file,'rb'))
#        try:
#            assert len(df) == Nimg
#        except AssertionError:
#            log('Note that the input df.pkl contains '+ str(len(df)) + ' particles, but that you have only chosen to output the first ' + str(Nimg) + ' particle')
#            df = df[:Nimg]
#        ctf = np.array([compute_ctf(freqs, i, i, args.ang, args.kv, args.cs, args.wgh, args.ps, args.b) \
#                for i in df])
#        ctf = ctf.reshape((Nimg, D, D))
#        df = np.stack([df,df], axis=1)
    elif args.sample_df:
        raise NotImplementedError
#
#        df1 = np.random.normal(args.dfu,args.sample_df,Nimg)
#        if args.no_astigmatism:
#            assert args.dfv == args.dfu, "--dfu and --dfv must be the same"
#            df2 = df1
#        else:
#            df2 = np.random.normal(args.dfv,args.sample_df,Nimg)
#        ctf = np.array([compute_ctf(freqs, i, j, args.ang, args.kv, args.cs, args.wgh, args.ps, args.b) \
#                for i, j in zip(df1, df2)])
#        ctf = ctf.reshape((Nimg, D, D))
#        df = np.stack([df1,df2], axis=1)
    else:
        ctf = compute_ctf(freqs, args.dfu, args.dfv, args.ang, args.kv, args.cs, args.wgh, args.ps, args.b)
        ctf = ctf.reshape((D,D))
        df = np.stack([np.ones(Nimg)*args.dfu, np.ones(Nimg)*args.dfv], np.ones(Nimg)*args.ang, np.ones(Nimg)*args.ps, axis=1)
    return ctf, df

def add_ctf(particles, ctf):
    assert len(particles) == len(ctf)
    particles = np.array([np.fft.fftshift(np.fft.fft2(np.fft.fftshift(x))) for x in particles])
    particles *= ctf
    del ctf
    particles = np.array([np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(x))).astype(np.float32) for x in particles])
    return particles

def normalize(particles):
    mu, std = np.mean(particles), np.std(particles)
    log('Shifting input images by {}'.format(mu))
    particles -= mu
    log('Scaling input images by {}'.format(std))
    particles /= std
    return particles

def invert(particles):
    particles *=-1
    return particles
 
def main(args):
    np.random.seed(args.seed)
    log('RUN CMD:\n'+' '.join(sys.argv))
    log('Arguments:\n'+str(args))
    if args.Nimg is None:
        log('Loading all particles')
        particles = mrc.parse_mrc(args.particles, lazy=False)[0]
        Nimg = len(particles)
    else:
        Nimg = args.Nimg
        log('Lazy loading ' + str(args.Nimg) + ' particles')
        particle_list = mrc.parse_mrc(args.particles, lazy=True, Nimg=Nimg)[0]
        particles = np.array([i.get() for i in particle_list])
    D, D2 = particles[0].shape
    assert D == D2, 'Images must be square'

    log('Loaded {} images'.format(Nimg))
    #if not args.rad: args.rad = D/2
    #x0, x1 = np.meshgrid(np.arange(-D/2,D/2),np.arange(-D/2,D/2))
    #mask = np.where((x0**2 + x1**2)**.5 < args.rad)

    if args.s1 is not None:
        assert args.s2 is not None, "Need to provide both --s1 and --s2"

    if args.s1 is None:
        Nstd = min(100,Nimg)
        mask = np.where(particles[:Nstd]>0)
        std = np.std(particles[mask])
        s1 = std/np.sqrt(args.snr1)
    else:
        s1 = args.s1
    if s1 > 0:
        log('Adding noise with stdev {}'.format(s1))
        particles = add_noise(particles, D, s1)
    
    log('Calculating the CTF')
    ctf, defocus_list = compute_full_ctf(D, Nimg, args)
    log('Applying the CTF')
    particles = add_ctf(particles, ctf)

    if args.s2 is None:
        std = np.std(particles[mask])
        # cascading of noise processes according to Frank and Al-Ali (1975) & Baxter (2009)
        snr2 = (1+1/args.snr1)/(1/args.snr2-1/args.snr1)
        log('SNR2 target {} for total snr of {}'.format(snr2, args.snr2))
        s2 = std/np.sqrt(snr2)
    else:
        s2 = args.s2
    if s2 > 0:
        log('Adding noise with stdev {}'.format(s2))
        particles = add_noise(particles, D, s2)
    
    if args.normalize:
        log('Normalizing particles')
        particles = normalize(particles)

    if not(args.noinvert):
        log('Inverting particles')
        particles = invert(particles)

    log('Writing image stack to {}'.format(args.o))
    mrc.write(args.o, particles.astype(np.float32))

    if args.out_star is None:
        args.out_star = f'{args.o}.star'
    log(f'Writing associated .star file to {args.out_star}')
    if args.ctf_pkl:
        params = pickle.load(open(args.ctf_pkl,'rb'))
        try:
            assert len(params) == Nimg
        except AssertionError:
            log('Note that the input ctf.pkl contains '+ str(len(params)) + ' particles, but that you have only chosen to output the first ' + str(Nimg) + ' particle')
            params = params[:Nimg]
        args.kv = params[0][5]
        args.cs = params[0][6]
        args.wgh = params[0][7]
        args.Apix = params[0][1]
    write_starfile(args.out_star, args.o, Nimg, defocus_list, args.kv, args.wgh, args.cs, args.Apix)

    if not args.ctf_pkl:
        if args.out_pkl is None:
            args.out_pkl = f'{args.o}.pkl'
        log(f'Writing CTF params pickle to {args.out_pkl}')
        params = np.ones((Nimg, 9), dtype=np.float32)
        params[:,0] = D
        params[:,1] = args.Apix
        params[:,2:4] = defocus_list
        params[:,4] = args.ang
        params[:,5] = args.kv
        params[:,6] = args.cs
        params[:,7] = args.wgh
        params[:,8] = args.ps
        log(params[0])
        with open(args.out_pkl,'wb') as f:
            pickle.dump(params,f)

if __name__ == '__main__':
    main(parse_args().parse_args())
