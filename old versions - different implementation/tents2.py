from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

weightNames = ["Minimum Trail Weight", "Fly / Footprint Pitch Weight", "Packaged Weight"]
areaNames   = ["Floor Area"]

tentParamNames = ["Minimum Trail Weight", "Fly / Footprint Pitch Weight", "Packaged Weight", "Floor Area"]


# the real best way to do this - at the top define all the parameters we care about 
# and then for each tent look for those, if not present enter -1 or something 

#%%
'''
def addItemToDict(d, key, val):
    if key not in d:
        d[key] = [val]
'''        
        
def initializeDict(pageSoupTent):
    techSpecContainer = pageSoupTent.findAll("script", {"data-client-store":"product-details"})
    tentSpecsText = techSpecContainer[0].string
    
    startSpecs = tentSpecsText.find("specs") + 7
    nearEndSpecs = tentSpecsText.find("Design Type")
    endSpecs = tentSpecsText[nearEndSpecs: ].find(",\n") + nearEndSpecs
    
    tentTextMod = tentSpecsText[startSpecs:endSpecs]
    compDict = eval(tentTextMod)
    allTentsInfo = dict()
    for tentParam in compDict:
        paramName = tentParam["name"]
        allTentsInfo[paramName] = []
        
    allTentsInfo["Current Price"] = []
    allTentsInfo["Original Price"] = []
    allTentsInfo["Tent Name"] = []
        
    return(allTentsInfo)


def priceDetails(pageSoupTent, allTentsInfo):
    techPriceContainer = pageSoupTent.findAll("script", {"data-client-store":"product-price-data"})
    tentPriceText = techPriceContainer[0].string
    
    tentPriceTextSplit = tentPriceText.split("compareAt")[1]
    startPrice = tentPriceTextSplit.find(" ") + 1
    endPrice   = tentPriceTextSplit.find("\n") - 1
    ogPrice = tentPriceTextSplit[startPrice:endPrice]
    
    tentPriceTextSplit = tentPriceText.split("min")[1]
    startPrice = tentPriceTextSplit.find(" ") + 1
    endPrice   = tentPriceTextSplit.find("\n") - 1
    curPrice = tentPriceTextSplit[startPrice:endPrice]
    
    #tentInfoDict["Current Price"] = float(curPrice)
    #tentInfoDict["Original Price"] = float(ogPrice)
    allTentsInfo["Current Price"].append(float(curPrice))
    allTentsInfo["Original Price"].append(float(ogPrice))
    


def specsDetails(pageSoupTent, allTentsInfo):
    techSpecContainer = pageSoupTent.findAll("script", {"data-client-store":"product-details"})
    tentSpecsText = techSpecContainer[0].string
    
    startSpecs = tentSpecsText.find("specs") + 7
    nearEndSpecs = tentSpecsText.find("Design Type")
    endSpecs = tentSpecsText[nearEndSpecs: ].find(",\n") + nearEndSpecs
    
    tentTextMod = tentSpecsText[startSpecs:endSpecs]
    compDict = eval(tentTextMod)
    #tentInfo = dict()
    for tentParam in compDict:
        paramName = tentParam["name"]
        paramValue = tentParam["values"][0]

        
        if (paramName in weightNames):
            poundsStart = paramValue.find("pound")
            if poundsStart != -1:
                pounds = paramValue[ : poundsStart]
                paramValue = float(pounds)
                
            else:
                lbsStart = paramValue.find("lbs")
                lbs = float(paramValue[:lbsStart])
                oz =  float(paramValue[lbsStart + 4: -3])
                paramValue = lbs + oz / 16
                
        if (paramName in areaNames):
            squareStart = paramValue.find("square")
            squares = paramValue[0:squareStart]
            paramValue = float(squares)
            
        #tentInfoDict[paramName] = paramValue
        if paramName in allTentsInfo:
            allTentsInfo[paramName].append(paramValue)
        
    #return tentInfo
            
def specsDetails_2(pageSoupTent, allTentsInfo):
    techSpecContainer = pageSoupTent.findAll("script", {"data-client-store":"product-details"})
    tentSpecsText = techSpecContainer[0].string
    
    startSpecs = tentSpecsText.find("specs") + 7
    nearEndSpecs = tentSpecsText.find("Design Type")
    endSpecs = tentSpecsText[nearEndSpecs: ].find(",\n") + nearEndSpecs
    
    tentTextMod = tentSpecsText[startSpecs:endSpecs]
    
    for tentParam in tentParamNames: 
        tentParamInd = tentTextMod.find(tentParam)
    
    
    compDict = eval(tentTextMod)
    #tentInfo = dict()    
    
    paramsFilled = [0] * len(tentParamNames)
    
    
    
    for tentParam in compDict:
        paramName = tentParam["name"]
        paramValue = tentParam["values"][0]
        
        
        if paramName not in tentParamNames:
            continue
        
        if (paramName in weightNames):
            poundsStart = paramValue.find("pound")
            if poundsStart != -1:
                pounds = paramValue[ : poundsStart]
                paramValue = float(pounds)
                
            else:
                lbsStart = paramValue.find("lbs")
                lbs = float(paramValue[:lbsStart])
                oz =  float(paramValue[lbsStart + 4: -3])
                paramValue = lbs + oz / 16
                
        if (paramName in areaNames):
            squareStart = paramValue.find("square")
            squares = paramValue[0:squareStart]
            paramValue = float(squares)
            
        #tentInfoDict[paramName] = paramValue
        if paramName in allTentsInfo:
            allTentsInfo[paramName].append(paramValue)
        
    #return tentInfo

def nameAndHTML(container):
    urlAddition = container.a["href"]
    tentUrl = reiUrl + urlAddition

    uClientTent = uReq(tentUrl)
    htmlTent = uClientTent.read()
    uClientTent.close()

    pageSoupTent = soup(htmlTent, "html.parser")
    
    tentNameStart = urlAddition.rfind("/") + 1
    tentName = urlAddition[tentNameStart:]
    tentName = tentName.replace("-", " ")
    
    uClientTent = uReq(tentUrl)
    htmlTent = uClientTent.read()
    uClientTent.close()
    pageSoupTent = soup(htmlTent, "html.parser")
    
    #tentInfoDict["Tent Name"] = tentName
    return(tentName, pageSoupTent)


#%%
allTentsUrl = "https://www.rei.com/c/backpacking-tents?ir=category%3Abackpacking-tents&r=category%3Acamping-and-hiking%7Ctents%7Cbackpacking-tents%3Bsleeping-capacity%3A3-person%3Bseasons%3A3-season%3Bbest-use%3ABackpacking%3Bdesign-type%3AFreestanding%3Bweight-lbs%3A3%20to%204.99%3Bprice%3A%24200.00%20to%20%24499.99"
tentClassMarker = "_2hd2hZzWXqYu7ZUGWvZw70"
reiUrl = "https://www.rei.com/"

uClientAllTents = uReq(allTentsUrl)
htmlAllTents = uClientAllTents.read()
uClientAllTents.close()

pageSoupAllTents = soup(htmlAllTents, "html.parser")

tentContainers = pageSoupAllTents.findAll("li", {"class":tentClassMarker})


#%%

import pdb 
#pdb.set_trace()
allTentsInfo = [0] * len(tentContainers)

allTentsInfo = dict()

for i in range(len(tentContainers)):
#for i in range(5, 6):
    if i == 2:
        x = 1
        pdb.set_trace()
        
    contain = tentContainers[i]
    
    (tentName, pageSoupTent) = nameAndHTML(contain)
    
    if (i == 0):
        allTentsInfo = initializeDict(pageSoupTent)
    
    specsDetails(pageSoupTent, allTentsInfo)
    priceDetails(pageSoupTent, allTentsInfo)

    allTentsInfo["Tent Name"].append(tentName)

