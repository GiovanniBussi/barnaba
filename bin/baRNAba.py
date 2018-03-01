#!/usr/bin/env python

#   This is baRNAba, a tool for analysis of nucleic acid 3d structure
#   Copyright (C) 2014 Sandro Bottaro (sbottaro@sissa.it)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License V3 as published by
#   the Free Software Foundation, 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
import sys
import glob
import os
import argparse
import barnaba as bb
import itertools as its

def parse():

    parser = argparse.ArgumentParser(description='This is baRNAba')
    subparsers = parser.add_subparsers(title="Subcommands",dest='subparser_name')
    subparsers.required = True
    
    # ERMSD PARSER
    parser_01 = subparsers.add_parser('ERMSD', help='calculate eRMSD')
    parser_01.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_01.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",required=False,default=None)
    parser_01.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_01.add_argument("--top", dest="top",help="Topology file",required=False)
    
    parser_01.add_argument("--ref", dest="reference",help="Reference PDB file",required=True)
    parser_01.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff (default=2.4)",default=2.4,type=float)

    
    # RMSD parser
    parser_01a = subparsers.add_parser('RMSD', help='calculate RMSD')
    parser_01a.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_01a.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",required=False,default=None)
    parser_01a.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_01a.add_argument("--top", dest="top",help="Topology file",required=False)    
    parser_01a.add_argument("--ref", dest="reference",help="Reference PDB file",required=True)
    parser_01a.add_argument("--dump", dest="dump",help="Write aligned PDB/TRJ",action='store_true',default=False)

    
    # ESCORE PARSER 
    parser_02 = subparsers.add_parser('ESCORE', help='Calculate eSCORE')
    parser_02.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_02.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",required=False,default=None)
    parser_02.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_02.add_argument("--top", dest="top",help="Topology file",required=False)

    parser_02.add_argument("--ff", dest="reference",help="Force-field PDB file",required=True)
    parser_02.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff (default=1.58)",default=1.58,type=float)

    # SEARCH SINGLE STRANDED MOTIFS - OK
    parser_03 = subparsers.add_parser('SS_MOTIF', help='Search single stranded (hairpin loop) RNA motif ')
    parser_03.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_03.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_03.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_03.add_argument("--top", dest="top",help="Topology file",required=False)

    parser_03.add_argument("--query", dest="query",help="Query PDB file",required=True)
    parser_03.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff",default=2.4,type=float)    
    parser_03.add_argument("--threshold", dest="threshold",help="ERMSD threshold",default=0.7,type=float)    
    parser_03.add_argument("--bulges", dest="bulges",help="Number of allowed bulged nucleotides",default=0,type=int)   
    parser_03.add_argument("--sequence", dest="seq",help="Sequence Accepts ACGU/NRY/ format. Default = any",required=False,default=None)
    parser_03.add_argument("--dump", dest="dump",help="Write pdb files",action='store_true',default=False)

    # SEARCH DOUBLE STRANDED MOTIFS - OK
    parser_04 = subparsers.add_parser('DS_MOTIF', help='Search double stranded RNA motifs ')
    parser_04.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_04.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_04.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_04.add_argument("--top", dest="top",help="Topology file",required=False)

    parser_04.add_argument("--query", dest="query",help="Reference PDB file",required=True)
    parser_04.add_argument("--l1", dest="l1",help="Length of first strand",required=True,type=int)    
    parser_04.add_argument("--l2", dest="l2",help="Lenght of second strand",required=True,type=int)    

    parser_04.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff",default=2.4,type=float)    
    parser_04.add_argument("--threshold", dest="threshold",help="ERMSD threshold",default=0.7,type=float)    
    parser_04.add_argument("--bulges", dest="bulges",help="Number of allowed bulged nucleotides",default=0,type=int)   
    parser_04.add_argument("--sequence", dest="seq",help="Sequence Accepts ACGU/NRY/ format. Default = any",required=False,default=None)
    parser_04.add_argument("--dump", dest="dump",help="Write pdb files",action='store_true',default=False)
    
    # ANNOTATE
    parser_05 = subparsers.add_parser('ANNOTATE', help='Annotate RNA structure')
    parser_05.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_05.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_05.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_05.add_argument("--top", dest="top",help="Topology file",required=False)
    parser_05.add_argument("--dotbracket", dest="dotbr",help="write dot-bracket annotation",action='store_true',default=False)


    # SEC_STRUCTURE
    parser_11 = subparsers.add_parser('SEC_STRUCTURE', help='Draw secondary structure from annotation')
    parser_11.add_argument("-o", dest="name", help="output_name",default=None,required=False)
    parser_11.add_argument("-s", dest="sequence", help="One-letter nucleic acid sequence", required=True, default=None)
    parser_11.add_argument("--ann", dest="f_anns", help="Annotation file(s) ([pairing and/or stacking] or dotbracket)", nargs="+",default=None,required=True)
    parser_11.add_argument("--draw_interm", dest="draw_interm", help="Draw intermediate structures (int)", default=0)
    parser_11.add_argument("--first_id", dest="first_id", help="First residue ID in sequence (int)", default=1)
    parser_11.add_argument("--missing", dest="missing", help="Missing residue IDs in sequence", nargs="+", default=None, required=False)
    parser_11.add_argument("--template", dest="template", help="SVG template structure (VARNA, RNAstructure etc.) ", default=None, required=False)
    parser_11.add_argument("-T", dest="T_init", help="Initial temperature for annealing", default=0)
    parser_11.add_argument("--nsteps", dest="nsteps", help="Number of steps for geometry optimization", default=1000)
    parser_11.add_argument("--no_tertiary_contacts", dest="tertiary_contacts", help="Do not use tertiary contacts in geometry optimization", action='store_false', default=True)
    parser_11.add_argument("--output_ids", dest="output_ids", help="Print residue IDs instead of letters",action='store_true',default=False)
    parser_11.add_argument("--dotbracket", dest="dotbracket", help="Use dotbracket annotation to draw (needs --ann file.ANNOTATE.dotbracket.out)", action='store_true',default=False)

    
    # DUMP
    parser_06 = subparsers.add_parser('DUMP', help='DUMP structural parameters')
    parser_06.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_06.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_06.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_06.add_argument("--top", dest="top",help="Topology file",required=False)

    parser_06.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff (default=2.4)",default=2.4,type=float)
    parser_06.add_argument("--dumpG", dest="dumpG",help="Write G vectors on .gvec file",action='store_true',default=False)
    parser_06.add_argument("--dumpR", dest="dumpR",help="Write R vectors on .rvec file",action='store_true',default=False)
    

    # CALCULATE TORSION ANGLES
    parser_08 = subparsers.add_parser('TORSION', help='Calculate dihedral angles')
    parser_08.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_08.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_08.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_08.add_argument("--top", dest="top",help="Topology file",required=False)

    parser_08.add_argument("--backbone", dest="backbone",help="calculate backbone (a,b,g,d,e,z) and chi torsion angle",action='store_true',default=False)
    parser_08.add_argument("--sugar", dest="sugar",help="calculate sugar torsion angles (v0...v5)",action='store_true',default=False)
    parser_08.add_argument("--pucker", dest="pucker",help="calculate sugar pucker angles (amplitude, phase)",action='store_true',default=False)
    parser_08.add_argument("--res", dest="res",help="Calculate torsion angle for specific residues",required=False,nargs="+",default=None)
    

    # CALCULATE TORSION ANGLES - J COUPLINGS OK
    parser_09 = subparsers.add_parser('JCOUPLING', help='Calculate J couplings.')
    parser_09.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_09.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    parser_09.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    parser_09.add_argument("--top", dest="top",help="Topology file",required=False)
    parser_09.add_argument("--res", dest="res",help="Calculate couplings for specific residues",required=False,nargs="+",default=None)
    parser_09.add_argument("--raw",dest="raw",help="print raw angles for j3",action="store_true",default=False)

    # CREATE FRAGMENTS
    parser_07 = subparsers.add_parser('SNIPPET', help='SPLIT structure in multiple PDB')
    parser_07.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_07.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=True)
    parser_07.add_argument("--seq", dest="seq",help="Sequence type. Accepts ACGU/NRY format",required=True)
    parser_07.add_argument("--outdir", dest="outdir",help="outdir",required=False,default=None)

    # CALCULATE ENM
    parser_10 = subparsers.add_parser('ENM', help='Calculate ENM')
    parser_10.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    parser_10.add_argument("--pdb", dest="pdbs",help="PDB file",default=None,required=True)

    parser_10.add_argument("--cutoff", dest="cutoff",help="Cutoff distance in nm (default=0.9)",default=0.9,type=float)
    parser_10.add_argument("--type", dest="type",default='SBP',choices=['P','S','B','SB','SP','BP','SBP','AA'], help='Type of ENM (default=SBP)')    
    parser_10.add_argument("--ntop", dest="ntop",help="Number of top eigenvectors to write (default=10)",default=10,type=int)
    parser_10.add_argument("--sparse", dest="sparse",help="Use sparse matrix diagonalization algorithm. Recomended for large matrices.",action='store_true',default=False)

    parser_10.add_argument("--shape", dest="shape",help="calculate C2/C2 fluctuations",action='store_true',default=False)

    
    # CLUSTERING
    #parser_13 = subparsers.add_parser('CLUSTER', help="Clustering")
    #parser_13.add_argument("-o", dest="name",help="output_name",default=None,required=False)
    #parser_13.add_argument("--pdb", dest="pdbs",help="PDB file(s)",nargs="+",default=None,required=False)
    #parser_13.add_argument("--trj", dest="trj",help="Trajectory",required=False,default=None)
    #parser_13.add_argument("--top", dest="top",help="Topology file",required=False)
    #parser_13.add_argument("--cutoff", dest="cutoff",help="Ellipsoidal cutoff (default=2.4)",default=2.4,type=float)
    
    #parser_13.add_argument("--alg", dest="alg",required=False,default="DBSCAN",choices=["DBSCAN"])
    #parser_13.add_argument("--eps", dest="eps",help="epsilon used for DBSCAN clustering. default=0.7",default=0.7,type=float)
    #parser_13.add_argument("--mins", dest="mins",help="minsample for DBSCAN clustering, Default=50",default=50,type=float)
    
    args = parser.parse_args()

    # CLUSTER
    
    return args


####################### ERMSD ########################

def ermsd(args):

    if(args.top==None):
        dd = [bb.ermsd(args.reference,pdb,cutoff=args.cutoff) for pdb in args.pdbs]
    else:
        dd = bb.ermsd(args.reference,args.trj,topology=args.top,cutoff=args.cutoff)
        
    fh = open(args.name + ".out",'w')
    fh.write("# %s \n" % (" ".join(sys.argv[:])))
    fh.write("#%10s   %10s\n" % ("Frame","eRMSD"))
    fh.write("".join([ " %10d   %10.4e \n" % (i,d) for i,d in enumerate(dd)]))
    fh.close()

####################### RMSD ########################

def rmsd(args):


    if(args.top==None):
        if(args.dump==True):
            dd = [bb.rmsd(args.reference,pdb,out="%s_%06d.pdb" % (args.name,i)) for i,pdb in enumerate(args.pdbs)]
        else:
            dd = [bb.rmsd(args.reference,pdb) for i,pdb in enumerate(args.pdbs)]
    else:
        if(args.dump==True):
            out = "%s.%s" % (args.name, (args.trj).split(".")[-1])
            dd = bb.rmsd(args.reference,args.trj,topology=args.top,out=out)
        else:
            dd = bb.rmsd(args.reference,args.trj,topology=args.top)

    fh = open(args.name + ".out",'w')
    fh.write("# %s \n" % (" ".join(sys.argv[:])))
    fh.write("#%10s   %10s\n" % ("Frame","RMSD"))
    fh.write("".join([ " %10d   %10.4e \n" % (i,d) for i,d in enumerate(dd)]))
    fh.close()

####################### ESCORE ########################
        
def score(args):
    
    import barnaba.escore as escore
    # set "force-field"
    ee = escore.Escore([args.reference],cutoff=args.cutoff)
    if(args.top==None):
        dd = [ee.score(pdb)[0] for pdb in args.pdbs]
    else:
        dd = ee.score(args.trj,topology=args.top)

    # Write to file
    fh = open(args.name + ".out",'w')
    fh.write("# %s \n" % (" ".join(sys.argv[:])))
    fh.write("#%10s   %10s\n" % ("Frame","ESCORE"))
    fh.write("".join([ " %10d   %10.4e \n" % (i,d) for i,d in enumerate(dd)]))
    fh.close()


####################### SS_MOTIF ########################

def ss_motif(args):

    out = None
    if(args.dump==True):out = args.name

    stri = "# %s \n" % (" ".join(sys.argv[:]))
    if(args.top==None):
        stri += "#%-20s %10s %s \n" % ("PDB","eRMSD","Sequence")
        for i in range(len(args.pdbs)):
            try:
                dd = bb.ss_motif(args.query,args.pdbs[i],out=out,bulges=args.bulges,threshold=args.threshold,sequence=args.seq,cutoff=args.cutoff)
                stri += "".join([" %-20s %10.4e %s \n" % (args.pdbs[i].split("/")[-1],dd[j][1],"-".join(dd[j][2])) for j in range(len(dd))])
            except:
                print("# not able to load %s" % args.pdbs[i])
                continue
    else:
        dd = bb.ss_motif(args.query,args.trj,topology=args.top,out=out,bulges=args.bulges,threshold=args.threshold,sequence=args.seq,cutoff=args.cutoff)
        stri += "".join([" %-20d %10.4e %s \n" % (j,dd[j][1],"-".join(dd[j][2])) for j in range(len(dd))])

    fh = open(args.name + ".out",'w')
    fh.write(stri)
    fh.close()


####################### DS_MOTIF ########################

def ds_motif(args):

    out = None
    if(args.dump==True):out = args.name

    stri = "# %s \n" % (" ".join(sys.argv[:]))
    if(args.top==None):
        stri += "#%-20s %10s %s \n" % ("PDB","eRMSD","Sequence")
        for i in range(len(args.pdbs)):
            dd = bb.ds_motif(args.query,args.pdbs[i],out=out,l1=args.l1,l2=args.l2,\
                             bulges=args.bulges,threshold=args.threshold,sequence=args.seq,cutoff=args.cutoff)
            stri += "".join([" %-20s %10.4e %s \n" % (args.pdbs[i].split("/")[-1],dd[j][1],"-".join(dd[j][2])) for j in range(len(dd))])
    else:
        stri += "#%20s %10s %s \n" % ("frame","eRMSD","Sequence")
        dd = bb.ss_motif(args.query,args.trj,topology=args.top,out=out,l1=args.l1,l2=args.l2,\
                         bulges=args.bulges,threshold=args.threshold,sequence=args.seq,cutoff=args.cutoff)
        stri += "".join([" %-20d %10.4e %s \n" % (j,dd[j][1],"-".join(dd[j][2])) for j in range(len(dd))])

    fh = open(args.name + ".out",'w')
    fh.write(stri)
    fh.close()


####################### ANNOTATE ########################

def annotate(args):

    stri_p = "# %s \n" % (" ".join(sys.argv[:]))
    stri_p += "#%-10s %-10s %4s \n" % ("RES1","RES2","ANNO")
    
    stri_s = "# %s \n" % (" ".join(sys.argv[:]))
    stri_s += "#%-10s %-10s %4s \n" % ("RES1","RES2","ANNO")

    stri_dot = "# %s \n" % (" ".join(sys.argv[:]))

    if(args.top==None):
        for i in range(len(args.pdbs)):
            st, pair, res = bb.annotate(args.pdbs[i])
            stri_p += "# PDB %s \n" % args.pdbs[i].split("/")[-1]
            stri_p += "".join([ "%-10s %-10s %4s \n" % (res[pair[0][0][e][0]],res[pair[0][0][e][1]],pair[0][1][e]) for e in range(len(pair[0][0]))])
            
            stri_s += "# PDB %s \n" % args.pdbs[i].split("/")[-1]
            stri_s += "".join([ "%-10s %-10s %4s \n" % (res[st[0][0][e][0]],res[st[0][0][e][1]],st[0][1][e]) for e in range(len(st[0][0]))])

            if(args.dotbr):
                dotbr = bb.dot_bracket(pair,res)
                stri_dot += "%-20s %s\n" %(args.pdbs[i].split("/")[-1],dotbr[0])

            
    else:
        st,pair,res = bb.annotate(args.trj,topology=args.top)
        if(args.dotbr):
            dotbr = bb.dot_bracket(pair,res)
            stri_dot += "".join(["%-10d %s\n" %(k,dotbr[k]) for k in range(len(pair))])
            
        for k in range(len(st)):
            stri_p += "# Frame %d \n" % k
            stri_p += "".join([ "%-10s %-10s %4s \n" % (res[pair[k][0][e][0]],res[pair[k][0][e][1]],pair[k][1][e]) for e in range(len(pair[k][0]))])
        
            stri_s += "# Frame %d \n" % k
            stri_s += "".join([ "%-10s %-10s %4s \n" % (res[st[k][0][e][0]],res[st[k][0][e][1]],st[k][1][e]) for e in range(len(st[k][0]))])
            
            
        
    fh1 = open(args.name + ".pairing.out",'w')
    fh1.write(stri_p)
    fh1.close()
    
    fh2 = open(args.name + ".stacking.out",'w')
    fh2.write(stri_s)
    fh2.close()

    if(args.dotbr):
        fh3 = open(args.name + ".dotbracket.out",'w')
        fh3.write(stri_dot)
        fh3.close()


####################### SEC_STRUCTURE #####################

def sec_structure(args):

    from numpy import unravel_index
    import barnaba.sec_str_svg as sesvg
    import barnaba.sec_str_ff as seff
    import barnaba.sec_str_constants as secon
#    from barnaba.sec_str_ff import *
#    from barnaba.sec_str_constants import *

    output = "# %s \n" % (" ".join(sys.argv[:]))

    if args.missing:
        missing_index = [int(i) for i in args.missing]
        residue_numbers = []
        args.first_id = int(args.first_id)
        j = args.first_id
        for i in args.sequence:
            while j in missing_index:
                j +=1 
            residue_numbers.append(j)    
            j += 1
    else:
        residue_numbers = range(int(args.first_id), int(args.first_id)+len(args.sequence))
    nucleotide = {}
    for key, i in enumerate(residue_numbers):
        nucleotide[i] = args.sequence[key]

    ann_lists = []
    ann_list = {}
    chains = []
    pairs_list = []
    n_frames = 0
    for f in args.f_anns:
        if args.dotbracket:
            if f.endswith("ANNOTATE.dotbracket.out"):
                chains, ann_lists, pairs, n_frames = bb.parse_dotbracket(f, len(args.sequence))
                pairs_list = pairs 
            if len(args.f_anns) > 1:
                print("Using input file %s, ignoring other annotation file(s)" % f)
            break
        else:    
            i_chains, i_ann_lists, i_pairs, i_n_frames = bb.parse_annotations(f, residue_numbers, nucleotide)
        if len(ann_lists) == 0:
            ann_lists = list(i_ann_lists)
        else:
            for c, ann_list in enumerate(ann_lists):
                ann_list.update(i_ann_lists[c])
        if len(pairs_list) == 0:
            pairs_list = i_pairs
        else:
            for c, p in enumerate(i_pairs):
                for pi in p:
                    if pi not in pairs_list[c]:
                        pairs_list[c].append(pi)
        if n_frames == 0:
            n_frames = i_n_frames
        else:
            if n_frames != i_n_frames:
                sys.exit("Annotations files %s have different numbers of frames" % options["ann"])
        if len(chains) == 0:
            chains = i_chains
        elif chains != i_chains:
            sys.exit("Different chains in files.")
    if len(ann_lists) == 0:
        sys.exit("No ANNOTATE.dotbracket.out file given")


    for c, ann_list in enumerate(ann_lists):
        pairs = pairs_list[c]
        n = len(args.sequence)
        param, param_wc_ds, sorted_params, param_angle = bb.parameters(pairs, ann_list, n, args.tertiary_contacts)     
        dimensions = secon.d_seq*(n-1)*.7
        length = n*secon.d_seq
        import numpy as np
        angle = 2*np.pi/n
        start = np.zeros((n, 2))
        min_pair = []
        max_pair = []
        i_min = n-1
        i_max = 0
        for p in sorted_params:
            if p[1] < i_min or p[2] < i_min: 
                if p[1] < i_min: i_min = p[1]
                if p[2] < i_min: i_min = p[2]
                min_pair = [p]
            elif p[1] == i_min or p[2] == i_min:
                min_pair.append(p)
            if p[1] > i_max or p[2] > i_max: 
                if p[1] < i_max: i_max = p[1]
                if p[2] < i_max: i_max = p[2]
                max_pair = [p]
            elif p[1] == i_min or p[2] == i_min:
                max_pair.append(p)
        print(min_pair, max_pair)
        circle = False
        cotranscript = True
        for p in min_pair:
            if p in max_pair:
                circle = True
                cotranscript = False
                break
        if cotranscript:
            print("Co-transcriptional folding")
        if not circle:
            print("Start on almost straight line")
        else:    
            print("Start on circle")
        for i in range(n):
            if not circle:
           # start on straight slightly perturbed line 
                start[i][0] = i*secon.d_seq
                start[i][1] = .1*(-1)**i + dimensions/2 
            else:    
           # start as circle
                start[i][0] = -length * 0.5/np.pi * np.sin(i*angle + .5*angle) + dimensions * 0.5
                start[i][1] = length * 0.5/np.pi * np.cos(i*angle + .5*angle) + dimensions * 0.5
           # start on half circle
           # start[i][0] = length * 1./np.pi * np.sin(i*angle*.5 + .5*angle) + dimensions * 0.5
           # start[i][1] = length * 1./np.pi * np.cos(i*angle*.5 + .5*angle) + dimensions * 0.5
        pos = start
        h = 2
        print_snapshots = min([int(args.nsteps), int(args.draw_interm)])
        print_energy = 20    
        print_energy = min([int(args.nsteps), print_energy])
        ds = int(float(args.nsteps)/print_energy)
        if print_snapshots > 0:
            ds_draw = int(float(args.nsteps)/print_snapshots)
        else:
            ds_draw = 0    
        dt = float(args.T_init)/int(args.nsteps)*3/2
        T = float(args.T_init)
        if len(chains) > 1:
            output += "------------------\nChain %d\n" % c
            print("------------------\nChain %d\n" % c)
            
        output += "%8s%10s%10s%6s%10s%8s\n" % ("Step", "energy", "F_max", "T", "h", "res(max_F)") 
        print("%8s%10s%10s%6s%10s%8s" % ("Step", "energy", "F_max", "T", "h", "res(max_F)")) 
        ki = 0
        added_ang = False
        write_force = False
        i_wcds = 0
       # param += param_angle
   #     if len(param_wc_ds) > 0:
   #         print("Adding largest double strand")
   #         param += param_wc_ds[0]
   #         i_wcds += 1
        i_pair = 0
       # print(param)
        if cotranscript:   
            print("Cotranscriptional folding")
            print("Added ", sorted_params[i_pair])
            param.append(sorted_params[i_pair])
        else:
            param += sorted_params
            param += param_angle
            print("Added all pair interactions and angle (90deg) potential")
        i_pair += 1
        wait = True
        t_wait = 20
        i_wait = 0
        for i in range(int(args.nsteps)+1):
            i_wait += 1
            if i_wait == t_wait:
                wait = False
            if cotranscript:    
                if  i % t_wait == 0 and not wait:
                    if i_pair < len(sorted_params):
                       # t_wait = 50
                        param.append(sorted_params[i_pair])
                        print(i, " Added ", sorted_params[i_pair])
                        if sum(sorted_params[i_pair]) != sum(sorted_params[i_pair-1]):
                            wait = True
                            i_wait = 0
                        i_pair += 1
                    elif i_pair == len(sorted_params):
                        param += param_angle
                        print(i, " Added 90 degree angles")
                        wait = True
            E, E_array = seff.energy(pos, param)
            F = seff.force(pos, param, write_force)
            max_F = abs(F).max()
            if i % ds == 0:
                r_i = unravel_index(F.argmax(), F.shape)
                print("%8d%10.3e%10.3e%6.1f%10.2e%8s" % (i, E, max_F, T, h,  r_i))
                output += "%8d%10.2e%10.2e%6.1f%10.2e%8s\n" % (i, E, max_F, T, h, r_i) 
                write_force = False
                if T > 0: 
                    T -= ds*dt
                    if T < 0: T = 0 
                j = i/ds

            else:
                write_force = False
            if ds_draw > 0 and i % ds_draw == 0:
                output_svg = sesvg.draw_structure(pos, pairs, ann_list, args.sequence, residue_numbers, dimensions, args.output_ids)
                if len(chains) > 1:
                    fh1 = open(args.name + "_%d_%03d.svg" % (c, i),'w')
                else:
                    fh1 = open(args.name + "_%03d.svg" % i,'w')
                fh1.write(output_svg)
                fh1.close()
                
            if h < 1e-4: # or (h < .5 and i_wcds < len(param_wc_ds)):
              #  if i_wcds < len(param_wc_ds):
              #      param += param_wc_ds[i_wcds]
              #      i_wcds += 1
              #      print("Adding double strand")
              #      h = 2
              #  else:
                output += "Converged at %d steps. You can play with the temperature (-T).\n" % i
                print("Converged at %d steps. You can play with the temperature (-T).\n" % i)
                break
            if i == int(args.nsteps):
                output += "Reached maximum number of %d steps\n" % i
                print("Reached maximum number of %d steps\n" % i)
                break

            if T > 0:
                r = np.array([[np.random.random()*2-1, np.random.random()*2-1] for j in pos])
               # new_pos = pos + F/max_F * h + r * T
                if i > 0:
                    v = (new_pos - pos)*T
                else: 
                    v = np.array([[np.random.random()*2-1, np.random.random()*2-1] for j in pos]) * T
              #  v += r * T
                new_pos = pos + F/max_F * h + v
            else:
                new_pos = pos + F/max_F * h
            
            new_E, new_E_array = seff.energy(new_pos, param)
            if new_E < E:
                pos = new_pos
                h *= 1.2
                if h > 2:
                    h = 2
            else:
                h *= 0.2
        E, E_array = seff.energy(pos, param, False) 
        F = seff.force(pos, param, write_force)
        r_i = unravel_index(F.argmax(), F.shape)
        for p in param:
            if p[0] != 2 and r_i[0] in p[1:3] or (p[0] == 2 and r_i[0] in p[1:4]):
                print(p)
        p_max_E = E_array.index(max(E_array))
        print(p_max_E)
        print(param[p_max_E], max(E_array))
        print("%8d%10.2e%10.2e%6.1f%10.2e%8s" % (i, E, max_F, T, h, r_i))
        output += "%8d%10.2e%10.2e%6.1f%.2e%8s\n" % (i, E, max_F, T, h, r_i) 
        print( i, " steps of minmization")    
        output += "%d steps of minmization\n" % (i)
        output_svg = sesvg.draw_structure(pos, pairs, ann_list, args.sequence, residue_numbers, dimensions, args.output_ids)
        if len(chains) > 1:
            fh1 = open(args.name + "_%d_%dsteps.svg" % (c, i),'w')
        else:
            fh1 = open(args.name + "_%dsteps.svg" % (i),'w')
        fh1.write(output_svg)
        fh1.close()


    fh2 = open(args.name + ".out",'w')
    fh2.write(output)
    fh2.close()

    
                     



##################### DUMP #######################

def dump(args):

    assert args.dumpR or args.dumpG, "# ERROR. choose --dumpR and/or --dumpG"
    

    if(args.dumpR):
        stri_r = "# %s \n" % (" ".join(sys.argv[:]))
        stri_r += "#%15s %15s %11s %11s %11s \n" % ("RES1","RES2","x","y","z")

        if(args.top==None):
            for i in range(len(args.pdbs)):
                rvecs,resi = bb.dump_rvec(args.pdbs[i],cutoff=args.cutoff)
                idxs = its.permutations(range(len(resi)), 2)
                stri_r += "# PDB %s \n" % args.pdbs[i].split("/")[-1]
                stri_r += "".join([" %15s %15s %11.4e %11.4e %11.4e \n" % (resi[i1],resi[i2],rvecs[0,i1,i2,0],rvecs[0,i1,i2,1],rvecs[0,i1,i2,2]) for i1,i2 in idxs if(sum(rvecs[0,i1,i2]**2)> 1.E-05)])
        else:
            rvecs,resi = bb.dump_rvec(args.trj,topology=args.top,cutoff=args.cutoff)
            idxs = its.permutations(range(len(resi)), 2)
            for i in range(len(rvecs)):
                stri_r += "# Frame %d \n" % i
                stri_r += "".join([" %15s %15s %11.4e %11.4e %11.4e \n" % (resi[i1],resi[i2],rvecs[i,i1,i2,0],rvecs[i,i1,i2,1],rvecs[i,i1,i2,2]) for i1,i2 in idxs if(sum(rvecs[i,i1,i2]**2)> 1.E-05)])
                
        fh = open(args.name + ".rvec.out",'w')
        fh.write(stri_r)
        fh.close()
        
    if(args.dumpG):
        
        stri_g = "# %s \n" % (" ".join(sys.argv[:]))
        stri_g += "#%15s %15s %11s %11s %11s %11s \n" % ("RES1","RES2","G0","G1","G2","G3")
        
        if(args.top==None):
            for i in range(len(args.pdbs)):
                rvecs,resi = bb.dump_gvec(args.pdbs[i],cutoff=args.cutoff)
                idxs = its.permutations(range(len(resi)), 2)
                stri_g += "# PDB %s \n" % args.pdbs[i].split("/")[-1]
                stri_g += "".join([" %15s %15s %11.4e %11.4e %11.4e %11.4e \n" % (resi[i1],resi[i2],rvecs[0,i1,i2,0],rvecs[0,i1,i2,1],rvecs[0,i1,i2,2],rvecs[0,i1,i2,3]) for i1,i2 in idxs if(sum(rvecs[0,i1,i2]**2)> 1.E-05)])
        else:
            rvecs,resi = bb.dump_rvec(args.trj,topology=args.top,cutoff=args.cutoff)
            idxs = its.permutations(range(len(resi)), 2)
            for i in range(len(rvecs)):
                stri_g += "# Frame %d \n" % i
                stri_g += "".join([" %15s %15s %11.4e %11.4e %11.4e %11.4e \n" % (resi[i1],resi[i2],rvecs[i,i1,i2,0],rvecs[i,i1,i2,1],rvecs[i,i1,i2,2],rvecs[i,i1,i2,3]) for i1,i2 in idxs if(sum(rvecs[i,i1,i2]**2)> 1.E-05)])
                
        fh = open(args.name + ".gvec.out",'w')
        fh.write(stri_g)
        fh.close()
        

##################### CALCULATE TORSION ANGLES #######################
    
def torsion(args):
    
    assert args.backbone or args.sugar or args.pucker, "# ERROR. choose --backbone/sugar/pucker"
    
    if(args.backbone):
        
        stri_b = "# %s \n" % (" ".join(sys.argv[:]))        
        stri_b += "#%-12s  %11s %11s %11s %11s %11s %11s %11s\n" % ("RESIDUE","alpha","beta","gamma","delta","eps","zeta","chi")

        if(args.top==None):
            for i in range(len(args.pdbs)):
                stri_b += "# PDB %s \n" % args.pdbs[i].split("/")[-1]                
                angles_b,rr = bb.backbone_angles(args.pdbs[i],residues=args.res)
                stri_b += "".join([" %-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[0,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
        else:
            
            angles_b,rr = bb.backbone_angles(args.trj,topology=args.top,residues=args.res)
            for i in range(angles_b.shape[0]):
                stri_b += "# Frame %d \n" % i
                stri_b += "".join([" %-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[i,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
            
            
        fh = open(args.name + ".backbone.out",'w')
        fh.write(stri_b)
        fh.close()

    if(args.sugar):
        
        stri_b = "# %s \n" % (" ".join(sys.argv[:]))        
        stri_b += "#%-12s  %11s %11s %11s %11s %11s \n" % ("RESIDUE","nu0","nu1","nu2","nu3","nu4")

        if(args.top==None):
            for i in range(len(args.pdbs)):
                stri_b += "# PDB %s \n" % args.pdbs[i].split("/")[-1]                
                angles_b,rr = bb.sugar_angles(args.pdbs[i],residues=args.res)
                stri_b += "".join([" %-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[0,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
        else:
            
            angles_b,rr = bb.sugar_angles(args.trj,topology=args.top,residues=args.res)
            for i in range(angles_b.shape[0]):
                stri_b += "# Frame %d \n" % i
                stri_b += "".join([" %-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[i,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
            
            
        fh = open(args.name + ".sugar.out",'w')
        fh.write(stri_b)
        fh.close()

    if(args.pucker):
        
        stri_b = "# %s \n" % (" ".join(sys.argv[:]))        
        stri_b += "#%-12s  %11s %11s \n" % ("RESIDUE","Phase","Amplitude")

        if(args.top==None):
            for i in range(len(args.pdbs)):
                stri_b += "# PDB %s \n" % args.pdbs[i].split("/")[-1]                
                angles_b,rr = bb.pucker_angles(args.pdbs[i],residues=args.res)
                stri_b += "".join(["%-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[0,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
        else:
            
            angles_b,rr = bb.pucker_angles(args.trj,topology=args.top,residues=args.res)
            for i in range(angles_b.shape[0]):
                stri_b += "# Frame %d \n" % i
                stri_b += "".join(["%-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[i,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
                        
        fh = open(args.name + ".pucker.out",'w')
        fh.write(stri_b)
        fh.close()
      

def couplings(args):

    from  barnaba import definitions
    stri = "# %s \n" % (" ".join(sys.argv[:]))
    stri += "#%-12s %s\n" % ("RESIDUE","".join([" %11s" % (k) for k in  definitions.couplings_idx.keys()]))
    
    if(args.top==None):
        for i in range(len(args.pdbs)):
            stri += "# PDB %s \n" % args.pdbs[i].split("/")[-1]                
            angles_b,rr = bb.jcouplings(args.pdbs[i],residues=args.res,raw=args.raw)
            stri += "".join(["%-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[0,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])
    else:
        angles_b,rr = bb.jcouplings(args.trj,topology=args.top,residues=args.res,raw=args.raw)
        for i in range(angles_b.shape[0]):
            stri += "# Frame %d \n" % i
            stri += "".join([" %-12s %s \n" % (rr[e], "".join([" %11.3e" % angles_b[i,e,k] for k in range(angles_b.shape[2])])) for e in range(angles_b.shape[1])])

    fh = open(args.name + ".couplings.out",'w')
    fh.write(stri)
    fh.close()

    

####################  SNIPPET #######################

def snippet(args):

    for pdb in args.pdbs:
        bb.snippet(pdb,args.seq,outdir=args.outdir)


####################  ENM  #######################

def enm(args):
    
    import barnaba.enm as enm
    
    if(args.type=="AA"):
        sele = "AA"
    else:
        sele = []
        sele.append("CA")
        if("P" in args.type):
            sele.append("P")
        if("S" in args.type):
            sele.append("C1\'")
        if("B" in args.type):
            sele.append("C2")
        if(args.type=="SBP"):
            sele.append("CB")

    net = enm.Enm(args.pdbs,sele_atoms=sele,sparse=args.sparse,ntop=args.ntop,cutoff=args.cutoff)

    # print eigenvectors 
    eigvecs = net.print_evec(args.ntop)
    fh = open(args.name + ".eigvecs.out",'w')
    fh.write(eigvecs)
    fh.close()

    # print eigenvalues 
    eigvals = net.print_eval()
    fh = open(args.name + ".eigvals.out",'w')
    fh.write(eigvals)
    fh.close()

    if(args.shape):
        
        fluc,res =  net.c2_fluctuations()
        stri = "# %19s %s \n" % ("Residues","Fluctuations")
        stri +=  "".join(["%10s/%-10s %.6e \n" % (res[i],res[i+1],fluc[i]) for i in range(len(fluc)) ])
        fh = open(args.name + ".shape.out",'w')
        fh.write(stri)
        fh.close()





####################### MAIN #########################

def main():

    def filename(args):
        # create output filename
        if(args.name == None):
            outfile = 'outfile.' + args.subparser_name 
        else:
            outfile = args.name + "." + args.subparser_name
        args.name = outfile
        print("# your output will be written to files with prefix %s" % outfile)

    # Parse options
    args = parse()

    # create filename
    if(args.subparser_name!="SNIPPET"):
        outfile = filename(args)

    # check
    if(args.subparser_name!="SEC_STRUCTURE"):
        if(args.pdbs==None):
            assert args.trj != None, "# Specify either pdbs (--pdb) or a trajectory file (--trj)"
            assert args.top != None, "# Please provide a topology file"
        else:
            if(args.subparser_name != "ENM" and args.subparser_name!="SNIPPET"):
                assert args.trj == None, "# Specify either pdbs (--pdb) or a trajectory+topology files, not both"
            
    
    # call appropriate function
    options = {'ERMSD' : ermsd,\
               'RMSD' : rmsd,\
               'ESCORE' : score,\
               'SS_MOTIF' : ss_motif,\
               'DS_MOTIF' : ds_motif,\
               'ANNOTATE' : annotate,\
               'SEC_STRUCTURE' : sec_structure,\
               'DUMP' : dump,\
               'TORSION':torsion,\
               'JCOUPLING':couplings,\
               'ENM':enm,\
               'SNIPPET' : snippet}

    options[args.subparser_name](args)
    
####################### MAIN ########################    


if __name__ == "__main__":
    main()
