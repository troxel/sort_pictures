#!/usr/bin/python

import os
import sys
import re
import pprint
import argparse
import exifread
from subprocess import Popen,PIPE
import shutil

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Sort jpgs')
parser.add_argument('dir_src', type=str, help='source directory')
parser.add_argument('dir_dest', type=str, help='destination directory')
parser.add_argument('-r', '--recursive', action='store_true', help='search dir_src recursively')
parser.add_argument('-c', '--copy', action='store_true', help='copy files instead of move')
parser.add_argument('-s', '--silent', action='store_true', help='don\'t display parsing details.')
parser.add_argument('-t', '--test', action='store_true', help='run a test.  files will not be moved/copied\ninstead you will just a list of would happen')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose')
parser.add_argument('-ym', '--yyyymm', action='store_true', help='Layout YYYY/MM')
parser.add_argument('-ymd','--yyyymmdd', action='store_true', default=True, help='Layout YYYY/MM_DD')

args = parser.parse_args()

# -------------------------------------------
def gettags_exifread(fspec):
    
    # Open image file for reading (binary mode)
    fid = open(fspec, 'rb')

    tags = exifread.process_file(fid, details=False)
    if not bool(tags): 
        return None
        
    if 'EXIF DateTimeOriginal' in tags:
        tags['Date/Time'] = str(tags['EXIF DateTimeOriginal'])
    elif 'EXIF DateTimeDigitized' in tags:
        tags['Date/Time'] = str(tags['EXIF DateTimeOriginal'])
    else: 
        print fspec, " No EXIF"
        return None

    #: (0x9004) ASCII=2005:10:19 14:35:18 @ 599,
    #: (0x9003) ASCII=2005:10:19 14:35:18 @ 578,
    
    return tags  
    
# -------------------------------------------
def gettags_fhead(fspec):
  
    proc = Popen(["jhead",fspec], stdout=PIPE, stderr=PIPE, )
    rtn_str = proc.stdout.read()
    #stderr = proc.stderr.read()
    
    if rtn_str == '': return None      
    
    rtn_lst = rtn_str.strip().split("\n")
    tags_fhead={}
    for line in rtn_lst:
       pair = line.split(":")
       tags_fhead[pair[0].strip()] = pair[1].strip()

    #pp.pprint(tags_fhead)
      
    return tags_fhead   

      
# ----------------------------        
# Main 
for dirpath, dnames, fnames in os.walk(args.dir_src):
    for file_name in fnames:
        file_root, file_extension = os.path.splitext(file_name)
        #print file_extension
        if bool( re.match('.jpg', file_extension, re.I) ):
            fspec_src = os.path.join(dirpath, file_name)
            
            tags = gettags_exifread(fspec_src)    
            if not bool(tags): continue

            #pp.pprint(tags) 
            
            #tags = gettags_fhead(fspec)    
            #if not bool(tags): continue

            #'Date/Time': '2003:12:18 09:03:57',
            date_str,time_str = tags['Date/Time'].split();
            yyyy,mm,dd = date_str.split(":")
                                 
            if not (yyyy or mm or dd): continue                     
              
            dir_dest = os.path.join(args.dir_dest, yyyy)
                        
            if ( args.yyyymm ): dir_dest = os.path.join(dir_dest,mm)
            else:               dir_dest = os.path.join(dir_dest,mm + "_" + dd)
                                    
            if not os.path.exists(dir_dest): os.makedirs(dir_dest)
            
            fspec_dest = os.path.join(dir_dest,file_name)
            
            if not os.path.exists(fspec_dest):
                print "cp {0:s} {1:s}".format(fspec_src, fspec_dest)
                shutil.copy(fspec_src,fspec_dest)
            else: print >> sys.stderr, "File Exists", fspec_src
            #pp.pprint(tags)
                            



