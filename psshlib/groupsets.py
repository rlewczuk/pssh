# Copyright (c) 2012, Rafal Lewczuk

import re

re_line0 = re.compile(r'([^\s\:(]+)\s*:\s*(.*)$')
re_line1 = re.compile(r'([^\s:\(]+)\s*\(([^\)]*)\)\s*:(.*)$') 

class GroupSet:
    def __init__(self, path):
        self.groups = { }
        self.comments = { }
        self._read(path)


    def _read(self, filename):
        buf, lnum = "", 0
        with open(filename, "r") as f:
            for line in f:
                lnum += 1
                line = line.strip()
                if len(line) == 0 or line.startswith("#"): continue
                buf += line
                if line.endswith("\\"): continue
                ln = buf.replace("\\", " ").strip()
                if self._parseLine1(ln) or self._parseLine0(ln):
                    buf = ""
                else:
                    raise Exception("Cannot parse line %d: '%s'" % (lnum,ln))


    def _parseLine0(self, line):
        m = re_line0.match(line)
        if not m: return None
        s1,s2 = m.group(1).strip(), m.group(2).strip()
        self.comments[s1] = ''
        self.groups[s1] = [s2.strip()] if not ',' in s2 \
                else [s.strip() for s in s2.split(',')]
        return self.groups[s1]


    def _parseLine1(self, line):
        m = re_line1.match(line)
        if not m: return None
        s1,s2,s3 = [m.group(i).strip() for i in [1,2,3]]
        self.comments[s1] = s2
        self.groups[s1] = [s3.strip()] if not ',' in s3 \
                else [s.strip() for s in s3.split(',')]
        return self.groups[s1]

    
    def __getitem__(self, key):
        if not key in self.groups:
            raise Exception("No such group: '%s'" % key)
        ret = [(self[x[1:]] if x[0] == '@' else [x]) for x in self.groups[key]]
        ret = [x for x in set([i for o in ret for i in o])] 
        ret.sort()
        return ret


