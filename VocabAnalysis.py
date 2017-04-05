import sys
import csv
import click
import os.path

def word_stats(file_name):
	import re
	# balladin core_word_list 
	core_words = ["a", "can", "about", "cant", "actually", "car", "after", "catholic", "afternoon", "cause", "again", "close", "ago", "cold", "ah", "come", "all", "coming", "alright", "could", "always", "couldnt", "an", "couple", "and", "crew", "another", "day", "any", "days", "anything", "dear", "anyway", "did", "are", "didnt", "around", "different", "as", "do", "ask", "does", "at", "doesnt", "away", "doing", "back", "dollars", "bad", "done", "be", "dont", "beautiful", "down", "because", "dunno", "been", "eat", "before", "eight", "being", "either", "better", "eleven", "big", "else", "bit", "end", "bloody", "enough", "break", "er", "but", "even", "buy", "ever", "by", "every", "cake", "everyone", "came", "everything", "ey", "hour", "fair", "hours", "feel", "house", "find", "how", "finished", "hundred", "first", "i", "five", "if", "for", "in", "four", "into", "friday", "is", "from", "isnt", "fucking", "it", "get", "its", "gets", "its", "getting", "id", "give", "ill", "go", "im", "god", "ive", "goes", "job", "going", "just", "gone", "keep", "gonna", "kids", "good", "know", "got", "last", "gotta", "left", "had", "like", "half", "little", "happened", "live", "hard", "long", "has", "look", "have", "looking", "havent", "looks", "having", "lost", "he", "lot", "her", "love", "here", "lovely", "hell", "lunch", "hes", "made", "him", "make", "his", "many", "home", "married", "me", "people", "mean", "person", "might", "phone", "mind", "pick", "mine", "place", "minutes", "play", "mm", "pretty", "monday", "probably", "money", "put", "months", "quite", "more", "ready", "morning", "really", "much", "remember", "mum", "right", "must", "road", "my", "round", "name", "said", "need", "same", "never", "saturday", "new", "say", "next", "saying", "nice", "says", "night", "school", "no", "see", "not", "seen", "nothing", "seven", "now", "she", "of", "shell", "off", "shes", "oh", "shit", "ok", "shoes", "old", "should", "on", "sit", "once", "six", "one", "so", "ones", "some", "only", "someone", "or", "something", "other", "sorry", "our", "sort", "out", "start", "over", "started", "own", "still", "oclock", "straight", "past", "street", "pay", "stuff", "sure", "us", "take", "used", "talk", "very", "talking", "want", "tea", "wanted", "tell", "wants", "ten", "was", "than", "wasnt", "thanks", "way", "that", "we", "thats", "week", "the", "weekend", "their", "weeks", "them", "well", "then", "went", "there", "were", "theres", "were", "these", "weve", "they", "what", "theyre", "whats", "theyve", "when", "thing", "where", "things", "which", "think", "who", "thirty", "whos", "this", "why", "those", "will", "though", "with", "thought", "won", "three", "wont", "through", "work", "til", "working", "time", "would", "times", "wouldnt", "to", "wrong", "today", "yeah", "told", "year", "tomorrow", "years", "too", "yep", "try", "yes", "trying", "yesterday", "twelve", "you", "twenty", "your", "two", "youre", "um", "youve", "up"]
	file = open(file_name, "r")
	lines = file.readlines()
	predicted_words = 1
	words_per_sentence = []
	pwords = dict()
	in_core = dict()
	for line in lines:
		if any(s.isupper() for s in line):
			wordss = re.findall('\w+', line)
			for worda in wordss:
				# Core words?
				if worda.lower() in core_words:
					if worda.lower() in in_core:
						in_core[worda.lower()]=in_core[worda.lower()]+1
					else:
						in_core[worda.lower()]=1						
				# Predicted? 		
				if any(d.isupper() for d in worda):
					if worda.lower() in pwords:
						pwords[worda.lower()]=pwords[worda.lower()]+1
					else:
						pwords[worda.lower()]=1
					predicted_words = predicted_words+1
		# WPS
		words_per_sentence.append(len(re.findall('\w+', line.lower())))
	avg_wps = sum(words_per_sentence) / float(len(words_per_sentence))
	max_wps = max(words_per_sentence)
	file = open(file_name, "r")
	chars = file.read()
	# remove dodgy chars
	# Bad code. Could do this a lot better if I spent 5 minutes 
	chars_filtered = re.sub(r"\s+", '', chars.lower())
	chars_filtered = re.sub(r"[0-9]+", '', chars_filtered)
	chars_filtered = re.sub(r"#+", '', chars_filtered)
	chars_filtered = re.sub(r"'+", '', chars_filtered)
	chars_filtered = re.sub(r"\/+", '', chars_filtered)
	
	# Word count
	words = re.findall('\w+', chars.lower())
	avgWordLen = sum(map(len, words))/len(words)
	from collections import Counter
	charcount = Counter(chars_filtered)	
	wordcount = Counter(words)
	return int(avgWordLen), charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core

	
# Ignore all letters after an uppercase character
def getCharsSpoken(wordlist):
	cl = list()
	for word in wordlist:
		for c in word:
			if c.islower():
				 cl.append(c)
	return cl

# Given a list of words, remove any that are
# in a list of stop words.

def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

@click.command()
@click.option('--vocab-file', type=click.Path(exists=True), default='examples/vocab.txt', help='Path to a vocab file. String on each line. ')
#@click.option('--scan_steps', default=scan_steps, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
@click.option('--inc-spaces', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')
#@click.option('--stop-words', default=True, type=bool, help='Ignore spaces? Useful if you have no space in your layout')


# Open file. 
#  NB: Each line is a sentence. Only uppercase letters which have been predicted by a partner - INCLUDING first letters
def printStats(vocab_file, inc_spaces):

	# Outline your scan steps here
	# Sams Scan Steps - with the extra hit
	#scan_steps = {'e':2,'t':4,'o':7,'a':3,'n':9,'i':8,'s':5,'r':6,'h':4,'l':3,'d':8,'u':9,'w':4,'f':9,'m':5,'c':5,'g':7,'p':6,'b':8,'y':7,'k':6,'v':10,'x':6,'j':11,'z':7,'q':5}
	# Heidis Scan steps - "Full" steps
	scan_steps = { 'e':0,'t':2,'o':5,'a':1,'n':7,'i':6,'s':3,'r':4,'h':2,'l':1,'d':6,'u':7,'w':2,'f':7,'m':3,'c':3,'g':5,'p':4,'b':6,'y':5,'k':4,'v':8,'x':4,'j':9,'z':5,'q':3}

	# Not using these - but we could use this to exclude common (core) words
	# e.g http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
	# from an example at http://programminghistorian.org/lessons/counting-frequencies
	stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
	stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']

	total = totalpred = totalin_core = totalchr = 0
	avgWordLen, charcount, wordcount, avg_wps, max_wps, predicted_words, pwords, in_core = word_stats(vocab_file)
	click.echo("total words:")
	with open('output-all-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for item in sorted(wordcount, key=wordcount.get, reverse=True):
			writer.writerow([item, wordcount[item]])
			click.echo(item, wordcount[item])
			total = total+wordcount[item]
	click.echo("------")
	click.echo("predicted words:")
	with open('output-pred-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for itemp in sorted(pwords, key=pwords.get, reverse=True):
			writer.writerow([itemp, pwords[itemp]])
			click.echo(itemp, pwords[itemp])
			totalpred = totalpred+pwords[itemp]
	click.echo("------")
	click.echo("in core:")
	with open('output-incore-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for itemc in sorted(in_core, key=in_core.get, reverse=True):
			writer.writerow([itemc, in_core[itemc]])
			click.echo(itemc, in_core[itemc])
			totalin_core = totalin_core+in_core[itemc]
	click.echo("------")
	click.echo("total chars:")
	with open('output-incore-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		for itemch in sorted(charcount, key=charcount.get, reverse=True): 
			writer.writerow([itemch, charcount[itemch]])
			click.echo(itemch, charcount[itemch])
			totalchr = totalchr+charcount[itemch]
	click.echo("total words:" + str(total))
	click.echo("total chars:" + str(totalchr))
	click.echo("words in core:" + str(len(in_core)))
	click.echo("total words (i.e. inc repeats) in core:" + str(totalin_core))
	click.echo("avg word len:" +str(avgWordLen))
	click.echo("avg wps:" + str(avg_wps))
	click.echo("max wps:" + str(max_wps))
	click.echo("predicted words:" + str(predicted_words))
	click.echo("------")
	totalFreqScan = 0
	click.echo("Letter count, Frequency, Letter, Scan Steps, FreqXScanSteps, ")
	with open('output-freqfinal-words.csv', 'w') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(['Letter count', 'Frequency', 'Letter', 'Scan Steps', 'FreqXScanSteps' ])
		for s in charcount: 
			writer.writerow([str(float(charcount[s])),str(float(charcount[s])/totalchr),s, scan_steps[s], str((float(charcount[s])/totalchr) * scan_steps[s])])
			click.echo(str(float(charcount[s])),',',str(float(charcount[s])/totalchr),',',s,',', scan_steps[s],',', str((float(charcount[s])/totalchr) * scan_steps[s]))
			totalFreqScan = totalFreqScan + ((float(charcount[s])/totalchr) * scan_steps[s])
	click.echo("Total Frequency X Scan Steps:", totalFreqScan)

if __name__ == '__main__':
	printStats()

