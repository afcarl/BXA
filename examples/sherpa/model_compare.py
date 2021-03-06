"""
Compare analysed models using the stats.json files (which contain the evidence,
but also marginal summaries)
"""
import json
import sys
import numpy
from math import log, log10

prefixes = sys.argv[1:]

models = dict([(f, json.load(open(f if f.endswith('stats.json') else f + "stats.json"))['global evidence']) for f in prefixes])

best = max(models, key=models.__getitem__)
Zbest = models[best]
for m in models: models[m] -= Zbest
Ztotal = log(sum(numpy.exp([Z for Z in models.values()])))
limit = 30 # for example, Jeffreys scale for the Bayes factor

print
print 'Model comparison'
print '****************'
print
for m in sorted(models, key=models.__getitem__):
	Zrel = models[m]
	print 'model %-25s: log10(Z) = %6.1f %s' % (m.replace('stats.json',''), Zrel / log(10),
		' XXX ruled out' if Zrel < Ztotal - log(limit) else '   <-- GOOD' )

print
print 'The last, most likely model was used as normalization.'
print 'Uniform model priors are assumed, with a cut of log10(%s) to rule out models.' % limit
print


