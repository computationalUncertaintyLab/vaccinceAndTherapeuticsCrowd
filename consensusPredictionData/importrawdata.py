#mcandrew

import sys
import numpy as np
import pandas as pd

class mVaccTherQuestions(object):
    def __init__(self,loginfile):
        self.importLoginInfo(loginfile)
        
    def importLoginInfo(self,loginfile):
        loginInfo = {}
        for line in open(loginfile):
            k,v = line.strip().split(",")
            loginInfo[k] = v
        self.username  = loginInfo['username']
        self.password  = loginInfo['password']
        self.csrftoken = loginInfo['csrftoken']

    def sendRequest2Server(self):
        import requests
        client = requests.session() # start session
    
        # add CSRF cookie
        cookie_obj = requests.cookies.create_cookie(name="csrftoken",value= self.csrftoken)
        client.cookies.set_cookie(cookie_obj)

        # add headers
        headers = { "referer":"https://covid.metaculus.com/questions/"
                    ,'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
                    ,'accept': 'application/json; version=LATEST'
        }
        client.headers.update(headers)
        
        # post username and password to form to authenticate
        payload = {
	    "username": self.username, 
	    "password": self.password,
        }
        p = client.post("https://covid.metaculus.com/api2/accounts/login/", data = payload)
        self.client = client
        self.auth   = p

    def collectQdata(self,QN):
        root = "https://covid.metaculus.com/api2/questions/{:d}"
        data = self.client.get(root.format(QN)).json()
        self.data = data

    def constructPDF(self):
        density = self.data['community_prediction']['unweighted']['y']
        numProbs = len(density)
        
        minvalue  = self.data['possibilities']['scale']['min']
        maxvalue  = self.data['possibilities']['scale']['max']

        if type(minvalue) is int:
            minvalue = float(minvalue)
            maxvalue = float(maxvalue)
        elif "-" in minvalue:
            minvalue = pd.to_datetime(minvalue)
            maxvalue = pd.to_datetime(maxvalue)
        interval = (maxvalue-minvalue)/numProbs
        
        xs = [minvalue]
        for _ in range(numProbs-1):
            xs.append(xs[-1]+interval)
        self.xs=xs
        self.probs=density
        self.interval = interval

def addInCDF(data):
    def cuumsum(x):
        x = x.sort_values('bin')
        x['cdf'] = np.cumsum(x.prob*x.interval)
        return x
    return data.groupby('qid').apply(cuumsum).drop(columns=['qid']).reset_index()

if __name__ == "__main__":

    qdata = {'numOfPredictions':[],'question':[],'qid':[],'publishtime':[],'closetime':[],'numcomments':[],'numvotes':[]}
    data = {'qid':[],'bin':[],'interval':[],'prob':[]}
    
    fromsurveyNumber2Questionlist = {1:[4639,4641,4643,4640,4638,4642], 2:[4828,4827,4829,4824,4825,4823,4822]}

    for surveyNum,questions in fromsurveyNumber2Questionlist.items():
        metac = mVaccTherQuestions("../../loginInfo.text")
        metac.sendRequest2Server() # ping the server

        for q in questions:
            metac.collectQdata(q) # collect json data for this specific question
            metac.constructPDF()  # contstuct community, unweighted consensus PDF

            qid = metac.data['id']
            qdata['qid'].append(qid)
            
            npredics = metac.data['number_of_predictions']
            qdata['numOfPredictions'].append(npredics)
            
            questionText = metac.data['title'] 
            qdata['question'].append(questionText)

            pubbed = metac.data['publish_time']
            qdata['publishtime'].append(pubbed)
            
            closed = metac.data['close_time']
            qdata['closetime'].append(closed)

            ncomments = metac.data['comment_count']
            qdata['numcomments'].append(ncomments)

            nvotes =  metac.data['votes']
            qdata['numvotes'].append(nvotes)

            interv = metac.interval
            for (x,p) in zip(metac.xs,metac.probs):
                data['qid'].append(qid)
                data['bin'].append(x)
                data['prob'].append(p)
                data['interval'].append(interv)

    # transform dict to a data frame
    qdata = pd.DataFrame(qdata)
    data  = pd.DataFrame(data)

    # store data
    qdata.to_csv("./qdata.csv")
    data.to_csv("./predictiondata.csv")
