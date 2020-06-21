from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

weightNames = ["Minimum Trail Weight", "Fly / Footprint Pitch Weight", "Packaged Weight"]
areaNames   = ["Floor Area"]
dimNames    = ["Floor Dimensions"]

specsNames = ["Minimum Trail Weight", "Fly / Footprint Pitch Weight", "Packaged Weight", "Floor Area", "Floor Dimensions", "Number of Doors"]
nonSpecsNames = ["Current Price", "Original Price", "Tent Name"]
tentParamNames = specsNames + nonSpecsNames


# the real best way to do this - at the top define all the parameters we care about 
# and then for each tent look for those, if not present enter -1 or something 

#%%
   
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
    
def weightNamesExtract(paramText):
    try: 
        poundsStart = paramText.find("pound")
        if poundsStart != -1:
            pounds = paramText[ : poundsStart]
            paramValue = float(pounds)
            
        else:
            lbsStart = paramText.find("lbs")
            lbs = float(paramText[:lbsStart])
            oz =  float(paramText[lbsStart + 4: -3])
            paramValue = lbs + oz / 16
            
    except: 
         paramValue = paramText
    
    return(paramValue)

def areaNamesExtract(paramText):
    squareStart = paramText.find("square")
    squares = paramText[0:squareStart]
    paramValue = float(squares)
        
    return paramValue

def dimNamesExtract(paramText):
    paramText = paramText.replace("/", " ")
    paramText = paramText.replace("x", " ")
    components = paramText.split(" ")
    nums =  [float(i) for i in components if i.replace(".", "").isdigit()]
    length = max(nums)
    nums.remove(length)
    width = max(nums)

    return([length, width])
    
    
            
def specsDetails(pageSoupTent, allTentsInfo):
    techSpecContainer = pageSoupTent.findAll("script", {"data-client-store":"product-details"})
    if not techSpecContainer:
        techSpecContainer = pageSoupTent.findAll("script", type="application/json")
        tentSpecsText = techSpecContainer[2].string
    else:
        tentSpecsText = techSpecContainer[0].string

    startSpecs = tentSpecsText.find("specs") + 7
    nearEndSpecs = tentSpecsText.find("Design Type")
    endSpecs = tentSpecsText[nearEndSpecs: ].find("variants") + nearEndSpecs
    
    tentTextMod = tentSpecsText[startSpecs:endSpecs]
    
    for tentParam in specsNames: 
        if tentParam == "Number of Doors": 
            x = 1
            #pdb.set_trace()
        if tentTextMod.find(tentParam) == -1:
            paramValue = -1
        
        else: 
            relevantText = tentTextMod.split(tentParam)[1]
            startVal = relevantText.find("[") + 2
            endVal = relevantText.find("]") - 1
            paramText = relevantText[startVal:endVal]
            
            if (tentParam in weightNames):
                paramValue = weightNamesExtract(paramText)

            elif (tentParam in areaNames):
                paramValue = areaNamesExtract(paramText)
                
            elif (tentParam in dimNames):
                paramValue = dimNamesExtract(paramText)
                
            else: 
                paramValue = paramText
                

        allTentsInfo[tentParam].append(paramValue)
    


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
allTentsUrl = "https://www.rei.com/c/backpacking-tents?ir=category%3Abackpacking-tents&r=category%3Acamping-and-hiking%7Ctents%7Cbackpacking-tents%3Bsleeping-capacity%3A3-person%3Bseasons%3A3-season%3Bbest-use%3ABackpacking%3Bdesign-type%3AFreestanding%3Bprice%3A%24200.00%20to%20%24499.99"
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


allTentsInfo = {key : [] for key in tentParamNames}

#for i in range(len(tentContainers)):
for i in range(17, 18): 
#for i in range(5, 6):
    if i == 17:
        x = 1
        pdb.set_trace()
        
    contain = tentContainers[i]
    
    (tentName, pageSoupTent) = nameAndHTML(contain)
    
    specsDetails(pageSoupTent, allTentsInfo)
    priceDetails(pageSoupTent, allTentsInfo)

    allTentsInfo["Tent Name"].append(tentName)

