import os
import sys
import re
import copy

class Schedule():
	def __init__(self):
		self.ifile = sys.argv[1]
		self.level =0
		self.T = 0
		self.M = 0
		self.E = 0
		self.unassigned = []
		self.mostConstrainedVar = 0
		self.leastConstrainingValue = 0
		self.employeeMeeting = dict()
		self.meetingEmploy = dict()
		self.travelTime = []
		self.assignment= dict()

		self.ConstrainedMeatings = dict()
		self.ConstrainingTimes = dict()
		self.GetInput()
		#print 'self.ConstrainedMeatings, ', self.ConstrainedMeatings 
		#print 'self.meetingEmploy, ',self.meetingEmploy
		#print 'unassigned', self.unassigned
		self.Revursive_Backtracking(self.assignment, self.unassigned, self.ConstrainedMeatings, self.level)

	def Revursive_Backtracking (self, assignment, unassigned, ConstrainedMeatings, level):
		if (len(assignment) == self.M):
			##print 'solution assignment: ', assignment
			#print 'solution ConstrainedMeatings: ', ConstrainedMeatings
			##print '\n'
			for key, value in assignment.items():
				print 'Meeting ', key, ' is scheduled at time ', value
			sys.exit()
			#return assignment

		#print '******start Revursive_Backtracking'
		#print '_assignment', assignment
		#print '_unassigned', unassigned
		_assignment = copy.deepcopy(assignment)
		_unassigned = copy.deepcopy(unassigned)
		_ConstrainedMeatings = copy.deepcopy(ConstrainedMeatings)
		_level = copy.deepcopy(level)
		_level+=1

		unasg = self.findMostConstrained(_unassigned, _ConstrainedMeatings)
		#print 'min: ', unasg
		_mostConstrained = copy.deepcopy(unasg)
		_VV = self.findLeastConstraining(_mostConstrained, _unassigned, _ConstrainedMeatings)
		_VVConstrain = copy.deepcopy(_VV[1])
		_conflictMeeting = copy.deepcopy(_VV[0])
		#print '_conflictMeeting', _conflictMeeting

		#print 'start Loop on level: ', _level
		for value in _VVConstrain:
			prune = self.Prune(value, _unassigned, _mostConstrained, _conflictMeeting,_ConstrainedMeatings, _level)

			if prune == -1:
				#print 'break! on level: ', _level
				break
			if prune != -1:
				_ConstrainedMeatings_ =copy.deepcopy(prune)
				##print 'aaa: ', _ConstrainedMeatings_
				_unassigned_ =copy.deepcopy(_unassigned)
				_assignment_ =copy.deepcopy(_assignment)

				_assignment_[_mostConstrained] = value
				_unassigned_.remove(_mostConstrained)
				#print '\n#######assigne time ', value, ' to meeting ', _mostConstrained
				self.Revursive_Backtracking(_assignment_, _unassigned_, _ConstrainedMeatings_, _level)


	def Prune(self, value, unassigned,mostConstrained, conflictMeeting, ConstrainedMeatings, level):
		#_conflictMeeting = 
		#print 'value: ', value, ' on level', level
		#print 'mostConstrained: ', mostConstrained, ' on level', level
		#print 'conflictMeeting', conflictMeeting
		##print 'in prune unassigned: ', unassigned
		_ConstrainedMeatings = copy.deepcopy(ConstrainedMeatings)
		for var in conflictMeeting:
			 if var in unassigned:

			 	interval1 = self.travelTime[mostConstrained-1][var-1]
			 	interval2 = self.travelTime[var-1][mostConstrained-1]

			 	thresh1 = interval1 + value
			 	thresh2 = value - interval2
			 	##print 'ahz, interval: ', interval

			 	#print 'ahz, remove var: ', var, ' ConstrainedMeating[var] :', ConstrainedMeatings[var], ' on thresh: (', thresh2, ', ', thresh1, ')' 
			 	if value in _ConstrainedMeatings[var]:
			 		_ConstrainedMeatings[var].remove(value)

			 	##print 'var: ', var,'original ConstrainedMeatings[var]: ', ConstrainedMeatings[var]

			 	if not _ConstrainedMeatings[var]:
			 		#print 'empty ahead, reuturn'
			 		return -1	
			 	_ConstrainedMeatings[var]= [item for item in _ConstrainedMeatings[var] if (item>thresh1 or item < thresh2)]
			 	##print 'var: ', var, '_ConstrainedMeatings[var]: ',_ConstrainedMeatings[var]

			 	if not _ConstrainedMeatings[var]:
			 		#print 'empty after assignment, reuturn'
			 		return -1
		#print '-----------ConstrainedMeatings: ', _ConstrainedMeatings
		return _ConstrainedMeatings			

	def findMostConstrained(self, unassigned, ConstrainedMeatings):
		MC = 0
		Sm = 999
		
		unasgC = dict()
		for i in unassigned:
			unasgC [i] = len(ConstrainedMeatings[i])
		_unasgC = sorted(unasgC, key = unasgC.get)

		unasg = []
		for key in _unasgC:
			unasg.append(key)
		#print 'ordered unasg: ', unasg
		return unasg[0]

	def findLeastConstraining(self, mostConstrained, unassigned, ConstrainedMeatings):
		#print 'ahaaa'
		_ConstrainedMeatings = copy.deepcopy(ConstrainedMeatings)
		#_unassigned = unassigned
		aValues = _ConstrainedMeatings[mostConstrained]

		#print 'aValues: ', aValues
		if not aValues:
			#print 'empty aValues!'
			return (-1, 0)
		empls = self.meetingEmploy[mostConstrained]
		conflictMeeting = []
		for emp in empls:
			conflictMeeting+= self.employeeMeeting[emp]
		conflictMeeting = list(set(conflictMeeting))
		conflictMeeting.remove(mostConstrained)	

		##print 'conflictMeeting, ', conflictMeeting
		valueConstrain = dict()
		for value in aValues:
			##print 'value: ', value
			PruneCount = 0
			for var in conflictMeeting:
				if var in unassigned:
					##print 'var: ',var
					interval1 = self.travelTime[mostConstrained-1][var-1]
					interval2 = self.travelTime[var-1][mostConstrained-1]
					_thresh1 =value + interval1
					_thresh2 =value - interval2
					##print '_thresh: (', _thresh2, ', ', _thresh1, ')'
					##print '_thresh2: ', _thresh2
					for time in _ConstrainedMeatings[var]:
						if time <= _thresh1 and time >= _thresh2:
							PruneCount+=1
			valueConstrain[value] = PruneCount
			#lokey = min(valueConstrain, key = valueConstrain.get)

		#print 'valueConstrain: ', valueConstrain

		_VVConstrain = sorted(valueConstrain, key = valueConstrain.get)
		#print '_VVConstrain', _VVConstrain
		return [conflictMeeting,_VVConstrain]
		##print 'lokey: ', lokey		

	def GetInput(self):
		infile = open(self.ifile, "r")
		lines = infile.readlines()
		for i in range(len(lines)):
			if re.match("Number of meetings:", lines[i]):
			   #print lines[i]
			   self.M = int(lines[i][20:])  
			   #print self.M
			if re.match("Number of employees:", lines[i]):
			   #print lines[i]
			   self.E = int(lines[i][21:])  
			   #print self.E
			if re.match("Number of time slots:", lines[i]):
			   #print lines[i]
			   self.T = int(lines[i][22:])  
			   #print self.T

			if re.match("Meetings each employee must attend:", lines[i]):
				i+=1
				for i in range (i, i+self.E):
					line = lines[i].strip('\n\r ').split()
					self.employeeMeeting[int(line[0][:-1])] = map(int, line[1:]) 
				#print 'self.employeeMeeting ~', self.employeeMeeting
				
				
			for j in range(self.M):
				self.ConstrainedMeatings[j+1] = range(1, self.T+1)
				self.meetingEmploy[j+1] = []
			##print 'self.meetingEmploy,', self.meetingEmploy	
			for key in self.employeeMeeting:
				for meet in self.employeeMeeting[key]:
					self.meetingEmploy[meet].append(key)
			 

			if re.match("Travel time between meetings:", lines[i]):
				i+=2
				for i in range (i, i+self.M):
					line = lines[i].strip('\n ').split()
					self.travelTime.append(map(int, line[1:]))
				#print 'self.travelTime: ',self.travelTime
		self.unassigned = range(1, self.M+1)
		infile.close()	



if __name__ == "__main__":
    app = Schedule()