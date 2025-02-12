"""This python file takes in input the  border crossing data from
Bureau of Transportation Statistics as csv data file 
and gives out a csv file containing counts of number of vehicles 
crossing the US-Canada Border and US-Mexico Border each month along
with the running averages for each month."""

import sys

# Adds data from the csv file to a dictionary
def adding_in_dictionary(x, y, z, dict_, USorMEX):
    if x not in dict_[USorMEX]:
        dict_[USorMEX][x] = list()
        dict_[USorMEX][x].append([y, z])
    else:
        dict_[USorMEX][x].append([y, z])

#Calculates the cummulative sum of each months count of type of vehicles
def calculate_cummulative_sum(index):
    for l in sorted_dates[index]:
        for m in dict1[k][l]:
            if int(str(l).split('-')[1]) == 1:
                dict1[k][l][m].append(0)
            else:
                x = int(str(l).split('-')[1]) - 1
                if len(str(x)) == 1:
                    y = '0' + str(x)
                else:
                    y = str(x)
                z = str(l).split('-')[0] + '-' + y + '-' + str(l).split('-')[2]
                if z in dict1[k]:
                    if m in dict1[k][z] and m in dict1[k][l]:
                        if len(dict1[k][z][m]) == 2:
                            dict1[k][l][m].append(dict1[k][z][m][0] + dict1[k][z][m][1])
                else:
                    if m in dict1[k][l]:
                        dict1[k][l][m].append(0)


if __name__ == '__main__':
    input_param = sys.argv[1]
    with open(input_param, 'r') as dataset:
        from datetime import datetime

        dict1 = dict()
        dict1["US"] = {}
        dict1["MEX"] = {}
        next(dataset)
        for i in dataset:
            i = i.strip().split(",")
            x, y, z = i[-4], i[-3], int(i[-2])
            x = x.split(" ")[0]
            x = datetime.strptime(x, '%m/%d/%Y').strftime("%Y-%m-%d")
            for j in i:
                if j == "US-Canada Border":
                    adding_in_dictionary(x, y, z, dict1, "US")
                elif j == "US-Mexico Border":
                    adding_in_dictionary(x, y, z, dict1, "MEX")

        for k in dict1:
            for l in dict1[k]:
                d = {}
                for m in dict1[k][l]:
                    if m[0] not in d:
                        d[m[0]] = m[1]
                    else:
                        d[m[0]] += m[1]
                dict1[k][l] = d
                
        #Adding the count of each type of crossing for each month as a list to the dictionary
        for k in dict1:
            for l in dict1[k]:
                for m in dict1[k][l]:
                    dict1[k][l][m] = [dict1[k][l][m]]
        
        #Sorting the dates beforehand to calculate the running monthly average
        sorted_dates = []
        us_list = []
        mex_list = []
        for k in dict1:
            if k == 'US':
                for l in dict1[k]:
                    us_list.append(l)
            else:
                for l in dict1[k]:
                    mex_list.append(l)
        sorted_dates.append(sorted(us_list))
        sorted_dates.append(sorted(mex_list))

        for k in dict1:
            if k == 'US':
                calculate_cummulative_sum(0)
            else:
                calculate_cummulative_sum(1)

        for k in dict1:
            for l in dict1[k]:
                for m in dict1[k][l]:
                    if len(dict1[k][l][m]) == 1:
                        dict1[k][l][m].append(0)

        import math
        
        #Collecting data from the dictionary created and appending desired output to a list of lists
        output = []
        for k in dict1:
            for l in dict1[k]:
                for m in dict1[k][l]:
                    if int(str(l).split('-')[1]) == 1:
                        output.append(str(l) + ',' + str(k) + ',' + str(m) + ',' + str(dict1[k][l][m][0]) + ',' + str(
                            dict1[k][l][m][1]))
                    else:
                        z = int(str(l).split('-')[1]) - 1
                        if len(dict1[k][l][m]) == 2:
                            a = math.ceil(dict1[k][l][m][1] / z)
                        else:
                            a = 0
                        output.append(
                            str(l) + ',' + str(k) + ',' + str(m) + ',' + str(dict1[k][l][m][0]) + ',' + str(a))
        
        # Sorting data in based on the sorting criteria given
        result = []
        for i in output:
            i = i.strip().split(",")
            result.append(i)
        result = sorted(result, key=lambda x: (x[0], int(x[3]), x[2], x[1]), reverse=True)

        output_param = sys.argv[2]
        
        #Writing the data to a csv file besides formating data for readability and prevent loss of originality of the data.
        file = open(output_param, 'w+')
        file.write("Border,Date,Measure,Value,Average\n")
        for i in result:
            if i[1] == "MEX":
                i[1] = "US-Mexico Border"
            else:
                i[1] = "US-Canada Border"
            i[0] = datetime.strptime(i[0], '%Y-%m-%d').strftime("%m/%d/%Y") + str(" 12:00:00 AM")
            file.write("{},{},{},{},{}\n".format(i[1], i[0], i[2], i[3], i[4]))

        file.close()
