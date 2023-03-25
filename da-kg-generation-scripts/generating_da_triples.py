import pandas as pd
import random
import csv
from collections import defaultdict

from queries.tv_queries import TVQueries
from tv_functions import TVFunctions

# Step 1: Load in DA mapping
da_mapping = pd.read_csv("kg-da-mapping/kg-da-mapping - TV.csv")
def write_csv(fname, data):
	with open(fname, 'w') as f:
		write = csv.writer(f)    
		write.writerows(data)
#def write_csv(fname, data):
#	with open(fname, 'w') as f:
#		write = csv.writer(f)    
#		write.writerows(data)

"""#Step 2: Generate a Dictionary/DataFrame that contains all the TV data that we can grab from
  #TV functions class function get all tv data will generate all the queries
train_comp_size = 5000
tv_functions = [TVFunctions.get_all_tv_data]
tv_data = {}
for func in tv_functions:
  tv_data[func] = func()
  if len(tv_data[func]) >= train_comp_size:
    tv_data[func] = tv_data[func][:train_comp_size]
  else:
    tv_data[func] = (tv_data[func]*int(train_comp_size/len(tv_data[func])+1))[:train_comp_size]
  
dir_name = "/Users/shashwat1225/Desktop/Winter'23/NLP244/KG Generation/da-kg-generation-scripts/tv_data_"
write_csv(dir_name+"train.csv", tv_data)"""

#Step 2: Generate a Dictionary/DataFrame that contains all the TV data that we can grab from TV functions class function get all tv data will generate all the queries
"""train_comp_size = 5
tv_functions = [TVFunctions.get_all_tv_data]
tv_data = []
for func in tv_functions:
  tv_data[func.__name__] = func() 
  if len(tv_data[func.__name__]) >= train_comp_size:
    tv_data[func.__name__] = tv_data[func.__name__][:train_comp_size]
  else:
    tv_data[func.__name__] = (tv_data[func.__name__]*int(train_comp_size/len(tv_data[func.__name__])+1))[:train_comp_size]"""


train_comp_size = 5
tv_functions = TVFunctions.get_genre_tv_data

tv_data = []
#for func in tv_functions:
func_data = tv_functions() 

if func_data is not None:
  if len(func_data) >= train_comp_size:
    func_data = func_data[:train_comp_size]
  else:
    func_data = (func_data*int(train_comp_size/len(func_data)+1))[:train_comp_size]
  
  # Add the sliced data to the tv_data list
  tv_data += func_data

print("\n\ntv_data: ", tv_data)
#func_data = func() 
#print("\n\nfunc_data: ", func_data)
#if func_data is not None:
#  func_data = func_data[:train_comp_size]
#else:
#func_data = tv_functions()
"""print("\n\nfunc_data: ", tv_functions)
if len(tv_functions) >= train_comp_size:
  functv_functions_data = tv_functions[:train_comp_size]
else:
  tv_functions = (tv_functions*int(train_comp_size/len(tv_functions)+1))[:train_comp_size]
  tv_data += tv_functions"""


end_token = " <|endoftext|> "
begin_token = " <|startoftext|> "

def formatTrainingData(training_data):
    final_data = []
    for data in training_data:
        triples = data[0]
        #print("triples: ", data[0])
        responses = data[1]
        text = random.choice(responses)
        if type(triples) == list:
            triples = " | ".join(map(lambda x: x[0] + " = " + x[1] + " = " + x[2], triples))
        else:
            triples = triples[0] + " = " + triples[1] + " = " + triples[2]
        train_inst = begin_token + triples + end_token + text + end_token
        train_inst = train_inst.strip()
        final_data.append([train_inst])
    return final_data

train_output = formatTrainingData(tv_data)
dir_name = "/Users/shashwat1225/Desktop/Winter'23/NLP244/KG Generation/da-kg-generation-scripts/tv_data_"
write_csv(dir_name+"train.csv", tv_data)



"""def formatTrainingData(training_data):
	final_data = []
	for data in training_data:
		triples = data[0]
		responses = data[1]
		text = random.choice(responses)
		if type(triples) == list:
			triples = map(lambda x: x[0] + " = " + x[1] + " = " + x[2], triples)
			triples = " | ".join(triples)
		else:
			triples = triples[0] + " = " + triples[1] + " = " + triples[2]
		train_inst = begin_token + triples + end_token + text + end_token
		train_inst = train_inst.strip()
		final_data.append([train_inst])

	split_num = int(len(final_data)*.1)
	dev_data = final_data[:split_num]
	train_data = final_data[split_num:]
	return final_data

train_output = formatTrainingData(list(tv_data.values()))

dir_name = "/Users/shashwat1225/Desktop/Winter'23/NLP244/KG Generation/da-kg-generation-scripts/tv_data_"
write_csv(dir_name+"train.csv", train_output)"""  # Pass the list of values of the tv_data dictionary to the write_csv function

#da_mapping
"""
DA	domain	min	max	mandatory slots
inform	tv	3	8	name
confirm	tv	2	3	name
give_opinion	tv	3	4	name, rating
recommend	tv	2	3	name
request	tv	1	2	specifier
request_attribute	tv	1	1	
request_explanation	tv	2	3	rating
suggest	tv	2	3	name
verify_attribute	tv	3	4	name, rating
"""


#Step 3: Create DA triples by
  # 1. Pick a random number between min to max for given DA
  # 2. Name will be the show, so create a filter function that will grab those specific entities
    #  from the dictionary and add to the pseudo MR
  # 3. Based on the random number from 1, choose the rest of the attributes
       #    (will need to confirm quality with different combos)
  #4. Create the pseudo MR to pass
    #5. Create a a file containing
      # domain , da, pseudo mr, tst prompt
        #tv,
#       inform,
#      The Hard Times of RJ Berger  genre  American television sitcom. The Hard Times of RJ Berger  genre  LGBTI+ related TV series
 #     Here is a text: "The Hard Times of RJ Berger  genre  American television sitcom  The Hard Times of RJ Berger  genre  LGBTI+ related TV series". Here is a rewrite of the text, which is a verify attribute dialogue act: "



"""for i in da_mapping:
      # 1. Pick a random number between min to max for given DA
      num = random.randint(i['min'], i['max'])
      tv_data = []
      for func in tv_functions:"""
          
      # 2. Name will be the show, so create a filter function that will grab those specific entities from the dictionary and add to the pseudo MR





dir_name = "/Users/shashwat1225/Desktop/Winter'23/NLP244/KG Generation/da-kg-generation-scripts/tv_data_"
write_csv(dir_name+"train.csv", train_output)
