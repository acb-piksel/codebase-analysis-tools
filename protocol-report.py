#!/usr/bin/python

import sys
import commands
import os.path
import re

if len(sys.argv)<2:
    sys.exit("usage: %s path"%sys.argv[0])


# protocol implementers: protocol name -> [ class names ]
implementers = {}
# classes: a list of all classes defined in the codebase
classes = []
# subclasses: class -> [subclasses]
subclasses = {}
# superclasses: class -> superclass
superclasses = {}

def visitdir(arg, dirname, fnames):
    for fname in fnames:
        visitfile(os.path.join(dirname,fname))

re_class = re.compile("^@interface ([^ <]+) *: *([A-Za-z0-9_]+) *(<([^>]*)>)?")
re_protocol = re.compile("^@protocol ([A-Za-z0-9_]*) *(<([^>]*)>)?")
def visitfile(path):
    global implementers, subclasses, superclasses, classes
    if not os.path.isfile(path):
        return
    for line in open(path):
        classmatch = re_class.match(line)
        protomatch = re_protocol.match(line)
        if classmatch:
            # handle class here
            classname, superclass = classmatch.group(1), classmatch.group(2)
            classes.append(classname)
            protocols = [s for s in (classmatch.group(4) or '').split(",") if s]
            for proto in protocols:
                implementers.setdefault(proto, []).append(classname)
            subclasses.setdefault(superclass,[]).append(classname)
            superclasses[classname] = superclass
        if protomatch:
            # handle protocol here
            #print "found protocol: %s"%protomatch.group(1)
            pass


os.path.walk(sys.argv[1], visitdir, None)

# -----  make the report here

# class hierarchy

topclasses = [c for c in classes if not superclasses.get(c) in classes]
topclasses.sort()

def printSubclassesOf(cl, level=0):
    scs = subclasses.get(cl, [])
    for sc in scs:
        print ("  "*level)+"+-> %s"%sc

for cl in topclasses:
    print "@class %s"%cl
    printSubclassesOf(cl)
    print ""

# protocols

protos = implementers.items()
protos.sort(key = lambda a:a[0])
for (proto, items) in protos:
    print "@protocol %s"%proto
    for cl in items:
        print " - implemented by %s"%cl
    print ""
