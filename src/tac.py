from symbol_table import table_stack
tac_stack = table_stack()
mult_flag = 0

class ThreeAddressCode:
	def __init__(self):
		self.symbolTable = None
		self.allCode = []
		self.tempVarCount = 1
		self.label_counter = 1

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		#code.print_quadruple()
		self.allCode.append(code)

	def print_code(self):
		print("\tOperation\tArg1\t\tArg2\t\tResult")
		for i in self.allCode:
			print("\t", i.operation, "\t\t", i.arg1, "\t\t", i.arg2, "\t\t", i.result)

	def generate_icg(self, operation, arg1, arg2, result):
		global mult_flag
		if operation == '+' or operation == '-':
			if tac_stack.get_length() == 1:
				if mult_flag == 1:
					self.generateCode(operation, str(arg1), str(tac_stack.pop()), 't'+str(self.tempVarCount))
					mult_flag -= 1
				else:
					self.generateCode(operation, str(arg2), str(tac_stack.pop()), 't'+str(self.tempVarCount))

				tac_stack.push('t'+str(self.tempVarCount))
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				self.generateCode(operation, str(tac_stack.pop()), str(tac_stack.pop()), 't'+str(self.tempVarCount))
				tac_stack.push('t'+str(self.tempVarCount))
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:
				self.generateCode(operation, str(arg1), str(arg2), 't'+str(self.tempVarCount))
				tac_stack.push('t'+str(self.tempVarCount))
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1
	
		elif operation == '*' or operation == '/':
			#print("Peek: ", tac_stack.peek(), "Length: ", tac_stack.get_length())
			
			#self.generateCode(operation, str(arg1), str(arg2), 't'+str(self.tempVarCount))
			
			#tac_stack.push('t'+str(self.tempVarCount))
			# add 't'+str(self.tempVarCount) to symbol_table
			
			#self.tempVarCount += 1
		
			if tac_stack.get_length() == 1:
				if mult_flag == 1:
					self.generateCode(operation, str(arg2), str(tac_stack.pop()), 't'+str(self.tempVarCount))
				else:
					mult_flag -= 1
					self.generateCode(operation, str(arg1), str(arg2), 't'+str(self.tempVarCount))

				tac_stack.push('t'+str(self.tempVarCount))
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				self.generateCode(operation, str(tac_stack.pop()), str(tac_stack.pop()), 't'+str(self.tempVarCount))
				tac_stack.push('t'+str(self.tempVarCount))
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:
				self.generateCode(operation, str(arg1), str(arg2), 't'+str(self.tempVarCount))
				tac_stack.push('t'+str(self.tempVarCount))
				mult_flag += 1
				# add 't'+str(self.tempVarCount) to symbol_table
				self.tempVarCount += 1
		
		elif operation == '=':
				if tac_stack.get_length() > 0:
					self.generateCode(operation, str(tac_stack.pop()), '', result)
				else:
					self.generateCode(operation, str(arg1), '', result)
				#tac_stack.push('t'+str(self.tempVarCount))

		elif operation == "goto":
			self.generateCode(operation, arg1, arg2, result)

		elif operation.endswith('F'):
			self.generateCode(operation, str(arg1), str(arg2), result)
		
		elif operation == "print":
			self.generateCode("SWI 0X02", '', '', result.strip())
		
		else:
			print("Invalid operation")

	def putLabel(self, kind):
		label = len(self.allCode)
		if kind == 'result':
			for i in reversed(self.allCode):
				if i.result.endswith("S"):
					i.result += str(label)
					break
		
		elif kind == 'arg1':
			for i in reversed(self.allCode):
				if i.arg1.endswith("S"):
					i.arg1 += str(label)
					break
		else:
			allCodeReverse = self.allCode[::-1]
			for i in range(len(allCodeReverse)):
				if allCodeReverse[i].result.endswith("S"):
					self.generate_icg("goto", "S"+str(label-i-1), '', '')
					break
		
class Quadruple:
	def __init__(self, operation, arg1, arg2, result):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

	def print_quadruple(self):
		print(self.operation, self.arg1, self.arg2, self.result)