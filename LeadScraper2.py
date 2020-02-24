#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
response = requests.get("https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=Lead")


# In[3]:


if(response.status_code):
    try:
        f = open("recallIDLog.txt","r")
        currIDs = f.readlines()
        currID = int(currIDs[0])
        f.close()
        f = open("recallIDLog.txt","w")
        fDescs = open("recallDescs.txt","w")
    except:
        f = open("recallIDLog.txt","w")
        fDescs = open("recallDescs.txt","w")
        description = response.json()[0]['Hazards'][0]['Name']
        remedy = response.json()[0]['ConsumerContact']
        currID = response.json()[0]['RecallID']
        name = response.json()[0]["Products"][0]["Name"]
        f.write("%d \r\n" % currID)
        fDescs.write("%s \r\n %s \r\n %s \r\n" % (name,description,remedy))
    ii = 0;
    recallID = response.json()[ii]['RecallID']
    while(currID<recallID):
        recallID = response.json()[ii]['RecallID']
        description = response.json()[ii]['Hazards'][0]['Name']
        remedy = response.json()[ii]['ConsumerContact']
        name = response.json()[ii]["Products"][0]["Name"]
        f.write("%d \r\n" % recallID)
        fDescs.write("%s \r\n %s \r\n %s \r\n" % (name,description,remedy))
        ii = ii+1
    f.close()
    fDescs.close()

# In[ ]:




