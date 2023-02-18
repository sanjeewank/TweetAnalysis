import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network



connections=[]
countedCountries=[]
filteredConnections=[]

def getWordList(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        elif word.startswith('#'):
            word=word[1:]
        tweet_words.append(word)
    return tweet_words
    
def preProcessor(tweet_words):
    newList=[]
    for word in tweet_words:
        word=word.lower()
        newList.append(word)
    return newList
    
def countryIdentifier(tweet_words,countries):
    Countrycount=0
    for word in tweet_words:
        if word in countries:
            Countrycount+=1
    return Countrycount
    
def makeConnection(tweet_words,countries):
    newConnection=[]
    for word in tweet_words:
        if word in countries:
            newConnection.append(word)
    connections.append(newConnection)  
    
def removeDuplicateCountries(countryList):
    return list(dict.fromkeys(countryList))
    
def makeConnections(tweet_words,countries):
    countryList=[]
    cleanedCountryList=[]
    connections=[]
    filteredConnectionList=[]
    for word in tweet_words:
        if word in countries:
            countryList.append(word)
    cleanedCountryList=removeDuplicateCountries(countryList)
    if(len(cleanedCountryList)==1):
        countCountries(cleanedCountryList,countries)
    elif(len(cleanedCountryList)==2):
        makeConnection(cleanedCountryList,countries)
    elif(len(cleanedCountryList)>2):
        for x in range(0,len(cleanedCountryList)):
    	    for y in range(x+1,len(cleanedCountryList)):
                connection=[]
                connection.append(cleanedCountryList[x])
                connection.append(cleanedCountryList[y])
                makeConnection(connection,countries)
          
def getTweets(tweetsData):
    tweetsData=tweetsData["Tweets"].to_list()
    return tweetsData

def removeDuplicates(connections,countries):
    tempConnections=[]
    for connection in connections:
        if(connection[0] != connection[1]):
            newConnection=[]
            newConnection=[connection[0],connection[1]]
            tempConnections.append(newConnection)
    return tempConnections

def countCountries(tweet_words,countries):
    for word in tweet_words:
        if word in countries:
            countedCountries.append(word)
    
def nodeSize(connections,countedCountries,countries):
    nodeSizes=[10]*32
    for connection in connections:
        countryOne=connection[0]
        countryTwo=connection[1]
        for country in countries:
            if(country==countryOne):
                CountryIndex=countries.index(country)
                nodeSizes[CountryIndex]=nodeSizes[CountryIndex]+0.06
            elif(country==countryTwo):
                CountryIndex=countries.index(country)
                nodeSizes[CountryIndex]=nodeSizes[CountryIndex]+0.06       
    for countedCountry in countedCountries:
        for country in countries:
            if(countedCountry==country):
                CountryIndex=countries.index(country)
                nodeSizes[CountryIndex]=nodeSizes[CountryIndex]+0.06
    return nodeSizes
        
def DrawGraph(connections,countries,nodeSizeList):
    g = nx.DiGraph()
    for country in countries:
        nodeSize=nodeSizeList[countries.index(country)]
        g.add_node(country,size=nodeSize)
    for connection in connections:
        g.add_edge(connection[0], connection[1])     
    
    pos = nx.spring_layout(g, seed=1969)
    options = {"node_color": "black", "linewidths": 0, "width": 0.1,"with_labels":True,"arrows":None}
    nx.draw(g, pos,**options)
    plt.show()
    
    
def DrawNetworkGraph(connections,countries,nodeSizeList):
    net = Network(height="750px", width="100%",filter_menu=True,select_menu=True,layout=None)
    for country in countries:
        nodeSize=nodeSizeList[countries.index(country)]
        net.add_node(country,value=nodeSize,label=country)
    for connection in connections:
        net.add_edge(connection[0], connection[1])
        
    net.show_buttons(filter_=['physics'])
    net.show("abc.html")
    
def main(tweetsData,countries):
    tweets=getTweets(tweetsData)
    for tweet in tweets:
        tweet_words=getWordList(tweet)
        tweet_words=preProcessor(tweet_words)
        Countrycount=countryIdentifier(tweet_words,countries)
        if(Countrycount==1):
            countCountries(tweet_words,countries)
        elif(Countrycount==2):
            makeConnection(tweet_words,countries)
        elif(Countrycount>2):
            makeConnections(tweet_words,countries)
    filteredConnections=removeDuplicates(connections,countries)
    nodeSizeList=nodeSize(filteredConnections,countedCountries,countries)
    #DrawNetworkGraph(filteredConnections,countries,nodeSizeList)
    df = pd.DataFrame (nodeSizeList,countries)
    df.to_csv('merged_Count.csv')
    df1 = pd.DataFrame (filteredConnections)
    df1.to_csv('merged_Conne.csv')
    
        
tweetsData = pd.read_csv('csv/merged.csv')
countries=["qatar","ecuador","senegal","netherland","england","iran","usa","wales","argentina","saudiArabia","mexico","poland","france","australia","denmark" ,"tunisia","spain","costaRica","germany","japan","belgium","canada","morocco","croatia","brazil","serbia","switzerland","cameroon","portugal","ghana","uruguay","southKorea"]
main(tweetsData,countries)


