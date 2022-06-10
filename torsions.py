from __future__ import print_function
import mdtraj as md
import numpy as np
import sys
import subprocess
import math
from scipy.stats import circmean
from scipy.stats import circstd

def torsions(traj):
    topology = traj.topology
    nres=traj.n_residues
    h,w = 250000, 540;
    dih0=np.zeros((h, w)) # 
    dih1=np.zeros((h, w))
    dih2=np.zeros((h, w))
    k0=-1
    k1=-1
    k2=-1
    nchref=-1
    kref=-1

    fileout0=open('dih_NbO4pC3pO2p_ave_fluc.dat','w')
    fileout1=open('dih_NbC1pC3pO2p_ave_fluc.dat','w')
    fileout2=open('dih_NbC1pC4pO2p_ave_fluc.dat','w')

    
    for ii,rr in enumerate(topology.residues):
        
        bb1='%4d' % rr.index
        bb2='%4d' % rr.chain.index
        #print(ii,rr)
        idxs = [[0,0,0,0] for x in range(15)]
        if(nchref !=rr.chain.index):
            nchref=rr.chain.index
            kref=0
        else:
            kref=kref+1
        if(rr.name =='U' or rr.name =='C'):
            try:
                idxs[0] =([rr.atom("N1").index, rr.atom("O4'").index, rr.atom("C3'").index, rr.atom("O2'").index])
                k0=k0+1

               
                
            except:
                sys.exit("Error in the file dihedral N1 O4' C3' O2'")                

        else:
            try:
                idxs[0] =([rr.atom("N9").index, rr.atom("O4'").index, rr.atom("C3'").index, rr.atom("O2'").index])
                k0=k0+1
            except:
                sys.exit("Error in the file dihedral N9 O4' C3' O2'")
                                   
        ang=md.compute_dihedrals(traj,[idxs[0]],periodic=False)
#        print(ang)
        #print(ang[1])
        nsize=ang.size
        
        for ll in range(0,nsize):
            dih0[ll][k0]=ang[ll]

        aares='%5d' % (ii+1)
        aname=rr.name
        aaave='%8.3f' %(circmean(dih0[0:ll+1,k0],low=-math.pi,high=math.pi)*180/math.pi)
        aastd='%8.3f' %(circstd(dih0[0:ll+1,k0],low=-math.pi,high=math.pi)*180/math.pi)
        stringa=aares+' '+aname+' '+aaave+' '+aastd
        fileout0.write(stringa+'\n')
          
        if(rr.name =='U' or rr.name =='C'):
            try:
                idxs[1] =([rr.atom("N1").index, rr.atom("C1'").index, rr.atom("C3'").index, rr.atom("O2'").index])
                k1=k1+1
            except:
                sys.exit("Error in the file dihedral N1 C1' C3' O2'")
                
        else:
            try:
                idxs[1] =([rr.atom("N9").index, rr.atom("C1'").index, rr.atom("C3'").index, rr.atom("O2'").index])
                k1=k1+1
            except:
                sys.exit("Error in the file dihedral N9 C1' C3' O2'")
                
        ang1=md.compute_dihedrals(traj,[idxs[1]],periodic=False)
        #        print(ang)
        #print(ang[1])
        nsize1=ang1.size
        
        for ll in range(0,nsize1):
            dih1[ll][k1]=ang1[ll]

        
        aares='%5d'% (ii+1)
        aname=rr.name
        aaave='%8.3f' %(circmean(dih0[0:ll+1,k1],low=-math.pi,high=math.pi)*180/math.pi)
        aastd='%8.3f' %(circstd(dih0[0:ll+1,k1],low=-math.pi,high=math.pi)*180/math.pi)
        stringa=aares+' '+aname+' '+aaave+' '+aastd
        fileout1.write(stringa+'\n')
            
        if(rr.name =='U' or rr.name =='C'):
            try:
                idxs[2] =([rr.atom("N1").index, rr.atom("C1'").index, rr.atom("C4'").index, rr.atom("O2'").index])
                k2=k2+1
            except:
                sys.exit("Error in the file dihedral N1 C1' C4' O2'")
            
        else:
            try:
                idxs[2] =([rr.atom("N9").index, rr.atom("C1'").index, rr.atom("C4'").index, rr.atom("O2'").index])
                k2=k2+1
            except:
                sys.exit("Error in the file dihedral N9 C1' C4' O2'")
                
        ang2=md.compute_dihedrals(traj,[idxs[2]],periodic=False)
        #        print(ang)
        #print(ang[1])
        nsize2=ang2.size
    
        for ll in range(0,nsize2):
            dih2[ll][k2]=ang2[ll]

        
        aares='%5d'% (ii+1)
        aname=rr.name
        aaave='%8.3f' %(circmean(dih2[0:ll+1,k2],low=-math.pi,high=math.pi)*180/math.pi)
        aastd='%8.3f' %(circstd(dih2[0:ll+1,k2],low=-math.pi,high=math.pi)*180/math.pi)
        stringa=aares+' '+aname+' '+aaave+' '+aastd
        fileout2.write(stringa+'\n')
        conv=180.0/math.pi
        
        np.savetxt('dih_NbO4pC3pO2p_trj.dat',dih0[0:ll+1,0:k0+1]*conv,fmt='%4.2f')
        np.savetxt('dih_NbC1pC3pO2p_trj.dat',dih1[0:ll+1,0:k1+1]*conv,fmt='%4.2f')
        np.savetxt('dih_NbC1pC4pO2p_trj.dat',dih2[0:ll+1,0:k2+1]*conv,fmt='%4.2f')
