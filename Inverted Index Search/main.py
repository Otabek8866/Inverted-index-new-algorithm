import os
import fnmatch

CLEANING_LIST_CHARACTERS = set(['.', ',', '!', '?', '-', '$', '\t', '\'', '\"', '\n', '(', ')', '[', ']', '{', '}'])
CLEANING_LIST_WORDS = set(['the', 'a', 'an', 'is'])


def final_content(docs_dict, lines_dict, accuracy):
	
	search_content = []
	iterator_doc = [x for x in sorted(docs_dict.keys(), reverse=True) if x >= accuracy]

	for i in iterator_doc:
		for j in docs_dict[i]:
			iterator_line = [x for x in sorted(lines_dict[j].keys(), reverse=True) if x >= accuracy]
			for k in iterator_line:
				search_content.append((j, lines_dict[j][k], k))

	return search_content
		

def count_occurance(counting_list):

	unique_list = {}
	for x in set(counting_list):
		if counting_list.count(x) in unique_list:
			unique_list[counting_list.count(x)].append(x)
		else:
			unique_list[counting_list.count(x)] = [x]
	
	return unique_list


def search(words, source_dict, accuracy):
	
	found_lines = {}
	final_list_docs = []
	found_docs = {}
	accuracy = int(len(words) * accuracy)
	
	#=============== Delete this block of code=========
	for word in words:
		if word in source_dict:
			found_docs[word] = source_dict[word]
	print_dict(found_docs)
	#==================================================

	for word in words:
		if word in source_dict:
			final_list_docs.extend(source_dict[word].keys())	
	

	final_dict = count_occurance(final_list_docs)
	for i in sorted(final_dict.keys(), reverse=True):
		for j in final_dict[i]:
			jlist = []
			for word in words:
				if j in source_dict[word]:
					jlist.extend(list(source_dict[word][j][0]))

			found_lines[j] = count_occurance(jlist)

	final_result = final_content(final_dict, found_lines, accuracy)
	
	return final_result	


def dictionary_words(file, adict):

	unique_words = extraction_words(file)
	all_lines = clean_up_file(file)
	
	for word in unique_words:
		
		lines = []
		counts = []

		for x, line in enumerate(all_lines, start=1):
			
			y = line.split(' ').count(word)
			if y:
				lines.append(x)
				counts.append(y)

		content = [tuple(lines), tuple(counts)]
		
		if not check_word(word, adict):
			adict[word] = {file: content}
		else:
			adict[word].update({file: content})

	return adict


def clean_up_line(line):

	line = line.lower()
	line.strip()

	for char in CLEANING_LIST_CHARACTERS:
			line = line.replace(char, '')

	return line	


def clean_up_file(file):
	"""
	Clean lines from the unnecessary characters.
	Remove duplicate words.
	"""
	cleaned_lines = []

	with open(file, 'r') as main_file:
		lines = main_file.readlines()

	for raw_string in lines:
		raw_string = clean_up_line(raw_string)
		cleaned_lines.append(raw_string)

	return cleaned_lines


def extraction_words(file):
	"""
	Return the unique words as a list.
	"""
	words_set = set()
	lines = clean_up_file(file)
	
	for line in lines:
		words_set.update(set(line.split(' ')) - CLEANING_LIST_WORDS)

	return list(words_set)


def check_word(word, adict):

	if word in adict.keys():
		return True
	else:
		return False


def print_dict(adict):

	for item in adict:
		print("{:<17}: {}".format(item, adict[item]))


def print_findings(alist):
	
	print("The requested term(s) can be found in the following order")
	print('='*30)
	alist.sort(key=lambda x: x[2], reverse=True)
	for x in range(len(alist)):
		print("{:<2}: {:<25} file, in the line(s): {}".format(x+1, alist[x][0], alist[x][1]))


if __name__ == "__main__":

	text_files = fnmatch.filter([file.lower() for file in os.listdir()], "*.txt")
	
	print("==================Source files=========================")
	for i in range(len(text_files)):
		print("{:<2}: {}".format(i + 1, text_files[i]))
	print("==================************=========================")

	main_dict = {}
	for file in text_files:
		main_dict = dictionary_words(file, main_dict.copy())

	while True:
		accuracy = float(input("Please enter the accuracy (from 0.0 to 1.0) by which you want to search: "))
		user_input = input('Please enter a text to search: ')
		searching_words = clean_up_line(user_input).split(' ')
		searching_words = [word for word in searching_words if word not in CLEANING_LIST_WORDS]

		founded_files = search(set(searching_words), main_dict, accuracy)

		print_findings(founded_files)

		x = input('Q: quite, S: search again').lower()

		if x == 'q':
			print("Thank you for using my service")
