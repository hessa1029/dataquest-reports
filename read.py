import pandas as pd
from collections import Counter

with open('AviationData.txt') as my_file:
    file = my_file.read()
    
aviation_data = file.split('\n')

aviation_list = [row.split(' | ') for row in aviation_data]
    
lax_code = []

#Using this method, it iterates across two dimensions, slowing this down considerably
for row in aviation_list:
    for item in row:
        if 'LAX94LA336' in item:
            lax_code.append(row)
            
print(lax_code)

#Linear method for searching aviation_data. Will search by row only
lax_code2 = []
for row in aviation_list:
    if 'LAX94LA336' in row:
        lax_code2.append(row)
        
print(lax_code2)

#There is no real good way to use a logarithmic time algo given that the data is not sorted by accident number. We can't narrow down based on that value

aviation_dict_list = []

column_headers = aviation_data[0].split(' | ')
aviation_data_new = aviation_data[1:]
for row in aviation_data_new:
    split = row.split(' | ')
    temp_dict = {}
    for i in range(len(split)):
        temp_dict[column_headers[i]] = split[i]
    aviation_dict_list.append(temp_dict)
    
lax_dict = []

for dictionary in aviation_dict_list:
    if 'LAX94LA336' in dictionary.values():
        lax_dict.append(dictionary)
        
# Overall, it seems easier to search through a list of dictionaries for the value than a list of lists since we just have to search for key value.


state_accidents_list = []

for dictionary in aviation_dict_list:
    if 'Country' in dictionary:
        if dictionary['Country'] == 'United States':
            state_list = dictionary['Location'].split(', ')
            try:
                state = state_list[1]
            except:
                state = ''
            if len(state) == 2:
                state_accidents_list.append(state)
        
state_accidents = Counter(state_accidents_list)

print('State with most aviation accidents: {}'.format(max(state_accidents, key=state_accidents.get)))

#We'll calculate the number of fatalities and serious injuries by looking at the "Total Fatal Injuries" and "Total Serious Injuries" coumns by month and year. Since data includes MM/DD/YYYY, we'll need to parse and remove the DD portion.

month_year = []
for dictionary in aviation_dict_list:
    month_injuries = []
    if 'Event Date' in dictionary:
        split = dictionary['Event Date'].split('/')
        try:
            ser_inj = int(dictionary['Total Serious Injuries'])
        except:
            ser_inj = 0
        try:
            fatal_inj = int(dictionary['Total Fatal Injuries'])
        except:
            fatal_inj = 0
        try:
            mm_yyyy = split[0] + '/' + split[2]
        except:
            mm_yyyy = ''
        if len(mm_yyyy) == 7:
            month_injuries.append(mm_yyyy)
            month_injuries.append(ser_inj)
            month_injuries.append(fatal_inj)
    month_year.append(month_injuries)
    
monthly_injuries = {}
for event in month_year:
    try:
        month = event[0]
        serious_injury = event[1]
        fatality = event[2]
    except:
        continue
    if month not in monthly_injuries:
        monthly_injuries[month] = {'Serious Injury': serious_injury, 'Fatal Injury': fatality}
    else:
        monthly_injuries[month]['Serious Injury'] += serious_injury
        monthly_injuries[month]['Fatal Injury'] += fatality
        
print(monthly_injuries)
