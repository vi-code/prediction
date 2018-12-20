import numpy as np 
import json
import argparse
import scipy.sparse.linalg as E
import scipy.linalg as sc
import time
import csv
import pandas as pd
from scipy import spatial


def exists(dishID_list, userID, user_ratings):
	count = 0
	flag = False
	for i in user_ratings[userID]:
		for j in dishID_list:
			if i[0]	== j:
				flag = True
	return flag

def user_dish_thingy(dishID_list, dish_list, userID):

	with open("user_ratings.json") as json_file:
		user_ratings = json.load(json_file)
	user_rated = {}
	if userID in user_ratings:
		for i in user_ratings[userID]:
			for j in (dishID_list):
				if (i[0] == j):
					user_rated[i[0]] = i[1]
	return user_rated

def computeVectorSpace(user_ratings, userID, dishID):

	#	print user_ratings
	valid_users = []
	valid_ratings = []
	counter = 0
	for i in range(0, 999):
		for x in user_ratings[str(i)]:
			if(x[0] == dishID):
				#print x, i
				valid_users.append(i)
				valid_ratings.append(x[1])
	#print valid_users

#	print user_ratings[str(1)]
	sums = []
	dishes_valid_users = []
	for j in range(len(valid_users)):
		sum = 0
		dishes_per_user = 0
		for dish_rating in user_ratings[str(valid_users[j])]:
			sum+=dish_rating[1]
			dishes_per_user+=1
		dishes_valid_users.append(dishes_per_user)
		sums.append(sum)
		sum = 0
		dishes_per_user = 0
	#print len(sums), len(dishes_valid_users)
	i = 0
	avgs = []
	for i in range(len(sums)):
		avgs.append(sums[i]/dishes_valid_users[i])
	#print avgs, valid_users
	i = 0
	user_wts = []
	user_calc = [] #User wt * (user rating - user average)
	counter= 0
	for i in (valid_users):
		User_curr_ratings = []
		User_X_ratings = []
		for x in user_ratings[str(i)]:
			#print x
			for y in user_ratings[userID]:
				#print x, y
				if(x[0] == y[0]):
					User_curr_ratings.append(y[1])
					User_X_ratings.append(x[1])
					break
		#print i
		if len(User_curr_ratings) != 0 and len(User_X_ratings) != 0:
			dot_product = np.inner(User_X_ratings, User_curr_ratings)
			norm_a = np.linalg.norm(User_X_ratings)
			norm_b = np.linalg.norm(User_curr_ratings)
			#user_wts.append(spatial.distance.cosine(User_X_ratings, User_curr_ratings))
			user_wts.append(dot_product/(norm_a*norm_b))

		else:
			user_wts.append(0)
#		print User_X_ratings
#		print i, valid_ratings[counter], user_wts[counter], user_wts[counter]*(valid_ratings[counter] - avgs[counter])
		user_calc.append(user_wts[counter]*(valid_ratings[counter] - avgs[counter]))
		counter+=1
	#print user_wts, user_calc
	sum_of_wts = np.sum(user_wts)
	sum_of_calc = np.sum(user_calc)

	input_ID_avg = 0
	numRatings_ID_avg = 0
	for i in user_ratings[userID]:
		numRatings_ID_avg+=1
		input_ID_avg += i[1]
#	print sum_of_wts, sum_of_calc, input_ID_avg/numRatings_ID_avg
	estimated = (input_ID_avg/numRatings_ID_avg) + (sum_of_calc/sum_of_wts)
	return estimated 
	

		


if __name__ == '__main__':
	start_time = time.time()
	with open("user_ratings.json") as json_file:
		user_ratings = json.load(json_file)
		#print user_ratings['0']
	#user_ratings = json.load(open(user_ratings, 'r'))
	arg_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	#print user_ratings
	dishID = int(input("Enter dish ID: "))
	userID = str(input("Enter user ID: "))

	d = 'dishes.csv'
	#for key, value in user_ratings.items():
		#for 
	check = 0
	if userID in user_ratings:
		for x in user_ratings[userID]:
			if(dishID == x[0]):
				print ("\nRating: " + str(x[1]) + " (existing)\n")
				check = 1
				break
	if check == 0:
		est_rating = computeVectorSpace(user_ratings, userID, dishID) 
		print("\nRating: " + str(est_rating) + " (estimated)\n")


	

	#PART 2
#	reader = csv.reader(open('dishes.csv', 'r'))
#	rownum = 0
#	for row in reader:
#		if rownum == 0:
#			header = row
#		else: 
#			colnum = 0
#			for col in row:
#				print header[colnum], col
#				colnum+=1
#		rownum+=1
	# rows = []
	# fields = []
	# with open("dishes.csv", 'r') as csvfile:
	# 	csvreader = csv.reader(csvfile)
	# 	fields = csvreader.next()

	# 	for row in csvreader:
	# 		rows.append(row)
	# print rows[1] 

	# fin = open("dishes.csv", 'r')
	# i_data = fin.readlines()
	# dish_names = {}
	# in_arr = []
	# ingredients = []
	# line_no = 0
	# for line in i_data:
	# 	line = parse_data(line)
	# 	print(line)
		# if(line_no == 0):
		# 	in_arr = line[2:]
		# else:
		# 	dish_names[line]
	dishes = pd.read_csv(d, sep=',', quotechar='\"', header=0)
	dish_data = dishes.values
	column = list(dishes.columns.values)
	

#	print dish_data
	userID = str(input("Enter user ID: "))
	num_ingredients = int(input("Enter number of ingredients: "))
	#THIS IS A LIST OF USER INPUTED INGREDIENTS
	ing_list = [] 
	for ingInput in range(num_ingredients):
		ing_list.append(raw_input("Enter ingredient I" + str(ingInput+1) + ": "))
	#THIS IS A DICTIONARY OF ALL INGREDIENTS 
	columnasDict = {} 	
	columnasDict = dict((map(reversed, enumerate(column))))

#	print type(columnasDict.values()[0])
#	for k, v in columnasDict.items():
#	column = { i : columnasDict[i] for i in range(0, len(listOfStr) ) }
	flag = 0
	count = 0

	dish_list = []
	dishID_list = []
	r = dish_data.shape[0]
	c = dish_data.shape[1]
	ingredient_index_toCheck = []
	for each in ing_list:
		if each in columnasDict:
			ingredient_index_toCheck.append(columnasDict[each])
	#print ingredient_index_toCheck
	# dd is the DISH NUMBER i.e. column and ingredient is the binary value for each dish. 
	# INGREDIENT 0 = DISH ID; INGREDIENT 1 = DISH NAME
	for dd in range(0, r):
		#print (dish_data[dd])
		for ingredient in range(0, c):
#			if(dish_data[dd,ingredient] == 1 and ingredient != 1 ):
			for index in ingredient_index_toCheck:
				if(dish_data[dd, index] == 1):
					flag = 1
					count+=1
					#print columnasDict
				else:
					flag = 0
					count = 0
					break

			if flag == 1 and count == len(ingredient_index_toCheck):
				dish_list.append(dish_data[dd,1])
				dishID_list.append(dd)
			#print count
	#print dish_list, dishID_list, userID
	# FINDING DISH IS RATED BY USER
	user_rated = user_dish_thingy(dishID_list, dish_list, userID)
	#print (user_rated)
					
	if len(dish_list) == 0:
		print("\nNo dish with specified ingredients")
	elif len(dishID_list) == 1:
		if exists(dishID_list, userID, user_ratings):
			print("\nNo new dish with specified ingredients\nYour best-rated dish:\n" + dish_list[0])
		else: 
			print("\nSuggested dish: \n"+ dish_list[0])
	elif len(dishID_list) > 1:
		for i in user_rated:
			if i in dishID_list:
				#print(dishID_list.index(i))
				dish_list.pop(dishID_list.index(i))
				dishID_list.remove(i)
		estimated_ratings_list = []
		#print dish_list, dishID_list
		for x in dishID_list:
			estimated_ratings_list.append(computeVectorSpace(user_ratings, userID, x))
		indexofMax = estimated_ratings_list.index(max(estimated_ratings_list))
		print("\nSuggested dish: \n"+dish_list[indexofMax])





