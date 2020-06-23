from math import log

alphabet = 'PQRSTUVWXYZ'

def ivan_generator(column, iteration=0):
	'''Generate a logical statement with a given truth table column.

	column - a binary string representing a column in a logical truth table

	If column is of length 2, then this is a truth table for a one-predicate
	statement and we simply output one of the four possible answers.
	Otherwise, split the column into its top and bottom halves, run the function
	on each half to obtain statements A and B respectively and return
	(A and X) or (B and ~X), where X is the next available letter in alphabet
	'''
	base_case = {
		'11' : '(_ or ~_)',
		'10' : '_',
		'01' : '~_',
		'00' : '(_ and ~_)'
	}
	length = len(column)
	assert set(char for char in column) <= set(['0','1']), 'Input column contains values other than 1 (True) and 0 (False).'
	assert log(length, 2).is_integer(), 'Input column of invalid length. Should be 2^n, where n is the number of predicates.'
	number_of_predicates = int(log(length, 2))
	if length == 2:
		return base_case[column].replace('_', alphabet[iteration])
	else:
		top_half, bottom_half = column[:length//2], column[length//2:]
		if length == 4:
			return '(' + alphabet[iteration] + ' and ' + ivan_generator(top_half, iteration+1) + ') or (~' + alphabet[iteration] + ' and ' + ivan_generator(bottom_half, iteration+1) + ')'
		else:
			return '(' + alphabet[iteration] + ' and (' + ivan_generator(top_half, iteration+1) + ')) or (~' + alphabet[iteration] + ' and (' + ivan_generator(bottom_half, iteration+1) + '))'

def mike_generator(column):
	'''Generate a logical statement with a given truth table column.alphabet[iteration]

	column - a binary string representing a column in a logical truth table

	Finds which rows in column contain "1" entries and creates an "and"
	statement that resolves to true for exactly that row. Then it joins	all of
	these statements together with "or" and outputs the result.
	'''
	length = len(column)
	assert set(char for char in column) <= set(['0','1']), 'Input column contains values other than 1 (True) and 0 (False).'
	assert log(length, 2).is_integer(), 'Input column of invalid length. Should be 2^n, where n is the number of predicates.'
	number_of_predicates = int(log(length, 2))

	# trues will be a list of lists.
	# If there are n predicates and j < n, trues[j] will be the list of rows
	# in the truth table for which the jth predicate is true. i.e., trues[0]
	# is the column under P in a normally-organized truth table, trues[1] is
	# the column under Q, etc.
	trues = [ [] for i in range(number_of_predicates)]
	for j in range(number_of_predicates):
		interval = length // (2**(j+1))
		for k in range(2**j):
			trues[j] += range(2*k*interval, (2*k + 1)*interval)

	statement_list = []

	for i in range(len(column)):
		if column[i] == '1':
			row = [i in trues[predicate] for predicate in range(number_of_predicates)]
			and_statement = ' and '.join(['~'*(not row[predicate]) + alphabet[predicate] for predicate in range(number_of_predicates)])
			statement_list.append( '(' + and_statement + ')' )

	output = ' or '.join([statement for statement in statement_list])

	if not output: return 'Contradiction!'

	return output

def get_string_inside_innermost_parentheses(text):
	'''Return string inside innermost matched parentheses.

	expressions is the list of all results. Currently set to only return the
	first one.
	'''
	inside = 0
	last_open_paren = 0
	expressions = []
	for i in range(len(text)):
		if text[i] == '(':
			inside += 1
			last_open_paren = i
		elif text[i] == ')' and inside:
			inside = 0
			expressions.append(text[last_open_paren+1:i])
	return expressions[0:1]

def triviality_finder(statement):
	'''Reduce a logical 'and' or 'or' statement to a single predicate, if possible.

	statement - a string containing a logical statement

	Find the outermost 'and' or 'or' in statement, and the two predicates on either
	side. If either of the two predicates are tautologies or contradictions,
	reduce the expression accordingly. Specifically:

		(tautology) and P == P
		(contradiction) and P == contradiction

		(tautology) or P == tautology
		(contradiction) or P == P

	Next, find all contradictions of the form "P and not P" and all
	tautologies of the form "P or not P", and mark them as such.

	If the input statement has no 'and' or 'or', or cannot be reduced in this
	way, return the statement surrounded by square brackets (so it is ignored by
	the innermost parenthesis expression finding function).

	'''
	inside = 0
	for i in range(len(statement)):
		if statement[i] == '(' or statement[i] == '[': inside += 1
		if statement[i] == ')' or statement[i] == ']': inside -= 1
		if inside == 0:
			if statement[i:i+2].lower() == 'or':
				data = statement[:i-1], 'or', statement[i+3:]
				break
			elif statement[i:i+3].lower() == 'and':
				data = statement[:i-1], 'and', statement[i+4:]
				break
	output = ''
	if data and data[1] == 'and':
		# Reduce "and" statements, as specified above.
		if data[0] == '--c--' or data[2] == '--c--': output = '--c--'
		elif data[0] == '--t--': output = data[2]
		elif data[2] == '--t--': output = data[0]
		chars = sorted(data[0]+data[2])
		if len(chars) == 3 and chars[2] == '~' and chars[0] == chars[1]:
			output = '--c--'

	if data and data[1] == 'or':
		# Reduce "or" statements, as specified above.
		if data[0] == '--t--' or data[2] == '--t--': output = '--t--'
		elif data[0] == '--c--':
			output = data[2]
		elif data[2] == '--c--': output = data[0]
		chars = sorted(data[0]+data[2])
		if len(chars) == 3 and chars[2] == '~' and chars[0] == chars[1]:
			output = '--t--'

	if not output:
		# If the statement could not be reduced in any of the above ways,
		# return it surrounded by square brackets so it is ignored on the next
		# pass of the recursion.
		return '[' + statement + ']'
	return output

def reducer(statement):
	'''Reduce a logical expression to the shortest-possible equivalent statement.

	statement - a string representing a logical statement,
			    using 'or', 'and', and '~' to represent negation

	If statement contains no parenthetical sub-statements, check it for possible
	reductions with triviality_finder and return the result. Otherwise, find
	the first sub-statement in statement in parentheses and	replace it with
	its reduced form according to triviality_finder. Then call itself on the
	new statement.
	'''
	innermost = get_string_inside_innermost_parentheses(statement)
	if not innermost:
		interpretation = triviality_finder(statement)
		if interpretation == '--c--': return 'Contradiction!' # Modify this and the next line to have it return whatever you want in this case
		elif interpretation == '--t--': return 'Tautology!'
		else: return interpretation.replace('[','(').replace(']',')') # If there are no more parentheses, returns the
	for expression in innermost:
		start, end = statement.find(expression) - 1, statement.find(expression) + len(expression) + 1
		statement = statement.replace('(' + expression + ')', triviality_finder(expression))

	return reducer(statement)

def main():
	# How many predicates do you want?
	predicates = 2

	#
	# A demonstration of both generators
	#

	number_of_columns = 2**(2**predicates)

	# n predicates makes for 2^2^n columns (e.g., 256 columns with 3 predicates),
	# so this lets you limit it for shorter outputs.
	limit = 50

	for i in range(number_of_columns):
		# A column is a binary string of a certain length. Any such string
		# represents a numbers under number_of_columns. So we list all such
		# numbers, convert to binary, and pad with zeroes to the appropriate
		# length.
		column = format(i, '0{0}b'.format(2**predicates))
		statement = ivan_generator(column)
		print('-'*40)
		print(''.join(column)) # If you want the entries to be separated, put the separating text in the empty quotes
		print()
		print("Ivan's statement:", statement)
		print()
		print("Ivan's reduced:  ", reducer(statement))
		print()
		print("Mike's statement:", mike_generator(column))
		if i > limit:
			break
if __name__ == '__main__':
	main()
