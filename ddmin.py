#!/usr/bin/env python

from split import split
from listsets import listminus
from xml.parsers.xmlproc import xmlproc
import re
import sys

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n
		
        some_complement_is_failing = 0
        for subset in subsets:
	        
	    complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
		n = max(n - 1, 2)
                some_complement_is_failing = 1
		break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances



if __name__ == "__main__":
    tests = {}
    circumstances = []
    
    """Split the string s into a list of distinguishable characters."""	
    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c
    
    """Test the circustances and return the parsing result."""	
    def mytest(c):
        global tests
        global circumstances

        s = ""
        for (index, char) in c:
            s += char

        if s in tests.keys():
            return tests[s]

        print "%03i" % (len(tests.keys()) + 1), "Testing",

	f = open('case.xml','w')
	f.write(s)
	f.close()

	try:
                app=xmlproc.Application()
                p=xmlproc.XMLProcessor()
                p.parse_resource('case.xml')
                print PASS
                tests[s] = PASS
                return PASS
        except UnboundLocalError :
                print FAIL
                tests[s] = FAIL
                return FAIL
        except:
                print UNRESOLVED
                tests[s] = UNRESOLVED
                return UNRESOLVED


    file = open(sys.argv[1], 'r')
    content = file.read()
    file.close()
    circumstances = string_to_list(content)
    mytest(circumstances)
    print ddmin(circumstances, mytest)
