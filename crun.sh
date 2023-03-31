#!/bin/bash
print "Script 1 running now"
python nlp2.py & 
wait
print "Script 2 running now"
python nlp3.py &
wait
print "Script 3 running now"
python nlp4.py &
wait
print "Script 4 running now"
python nlp5.py &
wait
print "Script 5 running now"
python nlp6.py 