from chatFeatures import ChatFeatures
from topic import Topic
from role import Role
from pprint import pprint

print "Chat Features"

iChat = ChatFeatures()
iChat.process()

print "========================="
print "===== Link Analysis ====="
print "========================="

pprint(iChat.linkAnalysis())

print "========================="
print "====== Domain Words ====="
print "========================="

pprint(iChat.domainWordsPerDay())

print "========================="
print "=== Messages per Turn ==="
print "========================="

pprint(iChat.msgPerTurn())

'''
print "========================="
print "====== Orthographic ====="
print "========================="
pprint(iChat.orthographic())
'''

print "Role Analysis"

iRol = Role()

print "========================="
print "==== Relevance Scores ==="
print "========================="
pprint(iRol.computeRolesPerDay())

print "Topic Analysis"

iTopic = Topic()

print "========================="
print "===== Relevant Days ====="
print "========================="
iTopic.relevantDayDetection()