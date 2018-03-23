import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import math

stock_list = []
AltmanScores = []
InterestCoverageScores = []
DebtEBITDAScores = []
DebtAssetScores = []
# Initialize the lists that we will use

number = int(input("How many stocks would you like to look up?"))
for i in range(number):
    tickers = input('Enter ticker for the stock you would like to look up')
    stock_list.append(tickers)
# Get the tickers for the stocks we want

for ticker in stock_list:
    r = requests.get("https://www.gurufocus.com/term/zscore/"\
                     +ticker.upper()+"/Altman-Z-Score/")
    # pull the webpage for each stock, we will use guru focus
    #  to find all our data

    soup = BeautifulSoup(r.content, 'lxml')
    # parse the web page

    for meta in soup.find_all("meta"):
        AltmanString = meta
    altmanString = str(AltmanString)
    # find the relevant object (the last one) and turn it into a string

    stringConstructor = ""
    Toggle = False
    Failure = 0
    AltmanScore = 0
    while Failure != 10:
        try:
            for char in altmanString:
                if Toggle == False:
                    stringConstructor += char
                    if len(stringConstructor) == 17:
                        stringConstructor = stringConstructor[1:]
                    if stringConstructor == "Altman Z-Score: ":
                        Toggle = True
                        stringConstructor = ""
                else:
                    if char != " ":
                        stringConstructor += char
                    else:
                        AltmanScore = float(stringConstructor)
                        Failure = 10
                        break
            # Go through the string and find the Altman score

        except:
            Failure += 1
            if Failure == 5:
                print("Error with Altman Score")
                sys.exit()
                break
        # Errors sometimes happen randomly, if it happens 5 times then exit prog

    AltmanScores.append((ticker, AltmanScore))
print()
print("When Z-Score is less than 1.81, it is in Distress Zones. \n\
When Z-Score is greater than 2.99, it is in Safe Zones.\n\
When Z-Score is between 1.81 and 2.99, it is in Grey Zones.")
print()
for i in AltmanScores:
    print(i[0].upper() + " has an Altman Z-Score of " + str(i[1]))
# Add scores to a list and print the result

for ticker in stock_list:
    r = requests.get("https://www.gurufocus.com/term/interest_coverage/"\
                     + ticker.upper()+'/')
    # pull the webpage for each stock, we will use guru focus
    #  to find all our data
    # will now look up the interest coverage data

    soup = BeautifulSoup(r.content, 'lxml')
    # parse the web page

    for meta in soup.find_all("meta"):
        interestString = meta
    interestString = str(interestString)
    # find relevant object and turn it into a string

    stringConstructor = ""
    Toggle = False
    for char in interestString:
        if Toggle == False:
            stringConstructor += char
            if len(stringConstructor) == 20:
                stringConstructor = stringConstructor[1:]
            if stringConstructor == "Interest Coverage: ":
                Toggle = True
                stringConstructor = ""
        else:
            if char != " ":
                stringConstructor += char
            else:
                break
    # go through string and find the interest coverage

    try:
        InterestCoverageScore = float(stringConstructor)
    except:
        InterestCoverageScore = "Negative Value"
    # exception for if the interest coverage is negative (company incurs loss)

    InterestCoverageScores.append((ticker, InterestCoverageScore))
print()
#print(InterestCoverageScores)
for i in InterestCoverageScores:
    print(i[0].upper() + " has an Interest Coverage Ratio of " + str(i[1]))
# append to list to store and print out the result

for ticker in stock_list:
    r = requests.get("https://www.gurufocus.com/term/debt2ebitda/" \
                     + ticker.upper()+'/')
    #Once again pull page through http request

    soup = BeautifulSoup(r.content, 'lxml')
    #parse page

    for meta in soup.find_all("meta"):
        DEString = meta
    DEString = str(DEString)
    #find relevant object and turn into a string for traversal

    stringConstructor = ""
    Toggle = False
    for char in DEString:
        if Toggle == False:
            stringConstructor += char
            if len(stringConstructor) == 17:
                stringConstructor = stringConstructor[1:]
            if stringConstructor == "Debt-to-EBITDA: ":
                Toggle = True
                stringConstructor = ""
        else:
            if char != " ":
                stringConstructor += char
            else:
                break
    # find the Debt to ebitda ratio

    try:
        DebtEBITDAScore = float(stringConstructor)
    except:
        DebtEBITDAScore = "No Debt"
    # exception if no debt

    if DebtEBITDAScore == "No Debt":
        DebtEBITDAScores.append((ticker, 0))
    else:
        DebtEBITDAScores.append((ticker, DebtEBITDAScore))
    # add ratio to list to store

print()
for i in DebtEBITDAScores:
    print(i[0].upper() + " has an Debt-to-EBITDA Ratio of " + str(i[1]))
# print out our result

for ticker in stock_list:
    r = requests.get("https://www.gurufocus.com/term/debt2asset/" \
                     + ticker.upper()+'/')
    # http request to pull webpage debt to asset ratio

    soup = BeautifulSoup(r.content, 'lxml')
    # parse webpage

    for meta in soup.find_all("meta"):
        DAString = meta
    DAString = str(DAString)
    # turn into a string for further parsing

    stringConstructor = ""
    Toggle = False
    for char in DAString:
        if Toggle == False:
            stringConstructor += char
            if len(stringConstructor) == 16:
                stringConstructor = stringConstructor[1:]
            if stringConstructor == "Debt-to-Asset: ":
                Toggle = True
                stringConstructor = ""
        else:
            if char != " ":
                stringConstructor += char
            else:
                break
    # try and find the debt to asset ratio

    DebtAssetScore = float(stringConstructor)
    DebtAssetScores.append((ticker, DebtAssetScore))
print()
for i in DebtAssetScores:
    print(i[0].upper() + " has an Debt-to-Asset Ratio of " + str(i[1]))
# turn ratio into a float, then store and print result

graphing_list = []
Altman_score = []
IntCov = []
D_EBITDA = []
D_Asset = []
for i in range(len(AltmanScores)):
    graphing_list.append((AltmanScores[i][1], InterestCoverageScores[i][1], \
                          DebtEBITDAScores[i][1]))
    Altman_score.append(AltmanScores[i][1])
    if InterestCoverageScores[i][1] == "Negative Value":
        IntCov.append(0)
    else:
        IntCov.append(InterestCoverageScores[i][1])
    D_EBITDA.append(DebtEBITDAScores[i][1])
    D_Asset.append(DebtAssetScores[i][1])
# creation of lists for the purpose of graphing

fig = plt.figure()
xpos = np.arange(len(stock_list))
plt.xticks(xpos, stock_list)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.bar(xpos, Altman_score,width = 0.2, color = 'r', label = "Altman Z-Score")
ax1.bar(xpos+0.2, IntCov, width = 0.2, color = 'b', label = "Interest Coverage")
ax2.bar(xpos-0.2, D_EBITDA, width = 0.2, color = 'g', label = "Debt To EBITDA")
ax2.bar(xpos-0.4, D_Asset, width = 0.2, color = 'y', label = "Debt To Asset")
# Create a 2 axis bar graph

low1 = min(Altman_score)
high1 = max(Altman_score)
low2 = min(D_EBITDA)
high2 = max(D_EBITDA)
ax1.set_ylim([math.ceil(low1-0.5*(high1-low1)),\
              math.ceil(high1+0.5*(high1-low1))])
# Scale the y axis

ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,\
           ncol=2, mode="expand", borderaxespad=0)
ax2.legend(bbox_to_anchor=(0., 1.07, 1., .102), loc=6,\
           ncol=2, mode="expand", borderaxespad=0)
plt.title("Credit Metrics")
# Form the legends and the title

plt.show()
# and display graph