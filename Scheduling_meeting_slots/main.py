time_slot = 30

p1_schedule = [["9:00","10:30"],["12:30","13:00"]]
p1_time_avaible = ["7:00","18:00"]

p2_schedule = [["10:00","11:30"],["12:30","13:00"],["14:30","15:00"]]
p2_time_avaible = ["8:00","20:00"]

def concat_schedule(schedule1,schedule2,t1_avaible,t2_avaible):
	concat_schedule = []
	time_avaible = concat_time_avaible(t1_avaible,t2_avaible)
	concat_schedule.append([time_avaible[0],time_avaible[0]])

	while len(schedule1) > 0 and len(schedule2) > 0:
		if comparetime(schedule1[0][0],schedule2[0][0]) == 1:
			concat_schedule.append(schedule1[0])
			schedule1.pop(0)
		else:
			concat_schedule.append(schedule2[0])
			schedule2.pop(0)

	concat_schedule.extend(schedule1)
	concat_schedule.extend(schedule2)
	schedule = concat_schedule
	print(schedule)

	i = 0
	while i < len(schedule) - 1:
		if not comparetime(schedule[i][1],schedule[i+1][0]) == 1:
			if not comparetime(schedule[i][1],schedule[i+1][1]) == 1:
				schedule.remove(schedule[i+1])
			else:
				schedule[i][1] = schedule[i+1][1]
			i += -1
		i += 1

	schedule.append([time_avaible[1],time_avaible[1]])

	i = len(schedule) - 1
	while i > 0:
		if not comparetime(schedule[i-1][1],schedule[i][0]) == 1:
			if not comparetime(schedule[i-1][0],schedule[i][0]) == 1:
				schedule.remove(schedule[i-1])
			else:
				schedule[i][0] = schedule[i-1][0]
		print(schedule)
		i += -1


	return schedule

def concat_time_avaible(t1_avaible,t2_avaible):
	time_avaible = []
	if not comparetime(t1_avaible[0],t2_avaible[0]) == 1:
		time_avaible.append(t1_avaible[0])
	else: time_avaible.append(t2_avaible[0])
	if not comparetime(t1_avaible[1],t2_avaible[1]) == -1:
		time_avaible.append(t1_avaible[1])
	else: time_avaible.append(t2_avaible[1])

	return time_avaible

def time_in_min(time):
	hour = ""
	min = ""
	is_hour = True
	for c in time:
		if c == ":":
			is_hour = False
		elif is_hour :
			hour += c
		else : min += c

	return int(hour)*60 + int(min)

def comparetime(t1,t2):

	t1 = time_in_min(t1)
	t2 = time_in_min(t2)

	if t1 < t2:
		return 1
	elif t1 > t2:
		return -1
	else:
		return 0

def free_time(t1,t2):

	t1 = time_in_min(t1)
	t2 = time_in_min(t2)

	return abs(t1-t2)

def avaible_timeslot(t1,t2,t1_avaible,t2_avaible):
	schedule = concat_schedule(t1,t2,t1_avaible,t2_avaible)
	avaible_timeslot = []

	for i in range(len(schedule) - 1):
		if free_time(schedule[i][1],schedule[i+1][0]) >= 30:
			time_slot = [schedule[i][1],schedule[i+1][0]]
			avaible_timeslot.append(time_slot)

	return avaible_timeslot

print(avaible_timeslot(p1_schedule,p2_schedule,p1_time_avaible,p2_time_avaible))