#~ Photographic Sorter Script ~#
#
# Have you literally thousands of photographs in all manner of USB devices, disks etc..?
# Most likely you have.  This script will given a directory go through them recursively
# and create a directory structure of YEAR // MONTH // DAY and copy the photographs into it
# I have found this useful as I have nearly 3 thousand photographs.  Simple but useful.
#
# Author: Simon Wilkinson
#
# 22/10/2010 Version 1.0

import sys
import os, os.path
import shutil
import time
from datetime import date
import EXIF
import hashlib

# Get the script to copy the files into a directory ordered by year and month

timenow = time.strftime("%d%m%Y", time.localtime(time.time()))
formattedtime = time.strftime("%d%m%Y_%H%M%S", time.localtime(time.time()))

alldirs = {}

dump = True
createdirs = True

path = 'E:\\AllPictures\\photosviao\\' # Set the SOURCE directory here
outdir = 'E:\\OUTPUT\\'    # Set the DESTINATION directory here

def getdate(datedata):
    print datedata
    data = str(datedata)
    year = data[:4]
    month = data[5:7]
    day = data[8:10]    
    return day+month+year

def md5(fileName, excludeLine="", includeLine=""):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        print "Unable to open the file in readmode:", filename
        return
    try:
        content = fd.readlines()
    except:
        content = []

    fd.close()
    for eachLine in content:
        if excludeLine and eachLine.startswith(excludeLine):
            continue
        m.update(eachLine)
    m.update(includeLine)
    return m.hexdigest()


startDir = path

copyfiletypes = '.JPG'

directories = [startDir]
while len(directories)>0:
    directory = directories.pop()
    for name in os.listdir(directory):
        fullpath = os.path.join(directory,name)
        if os.path.isfile(fullpath):
            
            f = open(fullpath,'rb')
            print fullpath
            print "-------------------------"
            print "Destination hash :",md5(fullpath)
            hashout = md5(fullpath)
            extension = fullpath[-4:]
            hashlabel = str(hashout)+str(extension)
            
            try:
                tags = EXIF.process_file(f)
            except:
                tags = {}
            
            try:
                dateprod = tags['Image DateTime']
            except:
                dateprod = ''

            data = str(dateprod)
            year = data[:4]
            month = data[5:7]
            day = data[8:10]  
            if createdirs:
                try:
                    os.mkdir(outdir+'\\'+year)
                except:
                    pass

                try:
                    os.mkdir(outdir+'\\'+year+'\\'+month)
                except:
                    pass

                try:
                    os.mkdir(outdir+'\\'+year+'\\'+month+'\\'+day)
                except:
                    pass

            outd = outdir+'\\'+year+'\\'+month+'\\'+day

            dest = os.path.join(outd,hashlabel)

            print "Destination :", dest
            
            if outdir.find(copyfiletypes):
                if (dateprod != ""):
                    try:
                        shutil.copy(fullpath,dest)
                        if (fullpath != ''):
                            print "Source hash :",md5(fullpath)
                            print "Source :",fullpath
                    except:
                        print "File error"
                
        elif os.path.isdir(fullpath):
            directories.append(fullpath)  



