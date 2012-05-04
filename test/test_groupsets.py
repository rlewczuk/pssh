# Copyright (c) 2012, Rafal Lewczuk

import unittest, psshlib.groupsets as g
from os import getcwd as cwd


class TestHgRegex(unittest.TestCase):

    def testRegex01(self):
        m = g.re_line0.match('test: a,b,c')
        self.assertTrue(m != None)
        self.assertEquals("test", m.group(1).strip())
        self.assertEquals("a,b,c", m.group(2).strip())
    
    def testRegex02(self):
        m = g.re_line0.match('@test: c')
        self.assertTrue(m != None)
        self.assertEquals("@test", m.group(1).strip())
        self.assertEquals("c", m.group(2).strip())
    
    def testRegex11(self):
        m = g.re_line1.match('tst.01 (RHEL6 templates):  templ1, templ2')
        self.assertTrue(m != None)
        self.assertEquals('tst.01', m.group(1).strip())
        self.assertEquals('RHEL6 templates', m.group(2).strip())
        self.assertEquals('templ1, templ2', m.group(3).strip())
    
    def testRegex12(self):
        m = g.re_line1.match('http (HTTP servers): @http.p, @http.s')
        self.assertTrue(m != None)
        self.assertEquals('http', m.group(1).strip())
        self.assertEquals('HTTP servers', m.group(2).strip())
        self.assertEquals('@http.p, @http.s', m.group(3).strip())
        

class TestHostgroups(unittest.TestCase):
    
    def setUp(self):
        self.cwd = cwd()
        if not self.cwd.endswith("/test"):
            self.cwd = "%s/test" % self.cwd
        self.groups = g.GroupSet(self.cwd + "/hostgroups")
    
    def test1(self):
        self.assertEquals(['a','b'], self.groups['grp1'])
    
    def test2(self):
        self.assertEquals(['a','b','c','d'], self.groups["grp2"])
        
    def test3(self):
        self.assertEquals(['a','b','c'], self.groups['grp5'])

    def test4(self):
        self.assertEquals(['a'], self.groups['grp6'])
        
    def test5(self):
        self.assertEquals(['a'], self.groups['grp7'])

    def test6(self):
        "test6: read hostnames extended with username and port number"
        self.assertEquals(['host:333', 'user@host', 'user@host:222'], 
                    self.groups['grp8'])
        

if __name__ == "__main__":
    unittest.main()