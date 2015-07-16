# codebase-analysis-tools

Some quick and dirty tools for getting overviews of Objective C (and eventually Swift) codebases. They currently are:


* protocol-report.py

Scan a code tree and print a report of class and protocol inheritance; i.e., list all locally defined classes and their subclasses, and all locally defined protocols and their implementors.  The output looks like:

```
@class Ungulate
+-> Goat
+-> Sheep


@protocol Headbutt
 - implemented by Goat
```
