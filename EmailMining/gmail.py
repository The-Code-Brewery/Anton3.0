from configparser import ConfigParser
import requests
from EmailMining.constants import BASE_URL
import pickle
import logging
import os
import json

class Gmail:
    email = None
    base_url = BASE_URL
    headers = {}

    @staticmethod
    def get_from_config(item):
	    config = ConfigParser()
	    config.read('./secret.ini')
	    try:
		    return config.get('Generic',item)
	    except:
		    return None
    
    def __init__(self):
        email = self.get_from_config('emailid')
        self.email = email
        content = None
        os.system(
                """
                python3 EmailMining/quickstart.py
                """
        )
        with open('EmailMining/token.pickle', 'rb') as pickle_file:
            content = pickle.load(pickle_file)
        self.headers = {
            'Authorization': f"Bearer {content.token}",
            'Accept': "application/json"
        }
    
    def get(self, route, params = None):
        response = None
        if params is None:
            response = requests.get(
                f"{self.base_url}{route}",
                headers = self.headers
            )
        else:
            response = requests.get(
                f"{self.base_url}{route}",
                headers = self.headers,
                params = params
            )
        return response
    
    def get_user_profile(self):
        """
        Get the user's profile based on the email address
        """
        route = "/me/profile"
        return self.get(route = route)
    
    def get_messages_list(self, maxResults = None, unread = False, messageFrom = None):
        """
        Get a list of messages
        """
        params = []
        queryString = ''
        if messageFrom is not None:
            queryString = queryString + f"from:{messageFrom}"
        if unread:
            queryString = queryString + f" is:'unread'"
        if maxResults is not None:
            params = [('maxResults',maxResults)]
        if queryString is not '':
            params.append(('q',queryString))
        route = '/me/messages'
        if params is []:
            return self.get(route = route)
        return self.get(route = route, params = params)
    
    def get_specific_message(self, id, metadata = False):
        """
        Get a specific message
        Metadata false means message body is not included
        """
        route = f'/me/messages/{id}'
        if metadata:
            params = [('format', 'metadata')]
            return self.get(route = route, params = params)
        return self.get(route = route)

def get_messages(unread = False, maxResults = None):
    """
    Will return from and subject as a dictionary
    """
    # An array of dictionaries with subject and from
    result = []
    gmail = Gmail()
    jsonList = json.loads(gmail.get_messages_list(maxResults=maxResults, unread=unread).content)
    messages = jsonList.get('messages')
    for message in messages:
        id = message.get('id')
        jsonSpecific = json.loads((gmail.get_specific_message(id=id, metadata=True).content))
        jsonSpecific = jsonSpecific.get('payload').get('headers')
        dictRes = {}
        for specific in jsonSpecific:
            if specific.get('name') == 'From':
                emailFrom = specific.get('value')
                try:
                    dictRes["from"] = emailFrom[0:emailFrom.index("<")-1]
                except:
                    dictRes["from"] = emailFrom
                continue
            if specific.get('name') == 'Subject':
                dictRes["subject"] = specific.get('value')
                break
        result.append(dictRes)
    return result

def get_messages_from_someone(messageFrom, unread = False, maxResults = None):
    """
    Will return from and subject as a dictionary
    From a certain person
    """
    # An array of dictionaries with subject and from
    result = []
    gmail = Gmail()
    jsonList = json.loads(gmail.get_messages_list(maxResults=maxResults, messageFrom=messageFrom, unread=unread).content)
    # messages = (gmail.get_specific_message(id='16fd903fe5e8cb9a').content.decode("utf-8"))
    messages = jsonList.get('messages')
    for message in messages:
        id = message.get('id')
        jsonSpecific = json.loads((gmail.get_specific_message(id=id, metadata=True).content))
        jsonSpecific = jsonSpecific.get('payload').get('headers')
        dictRes = {}
        for specific in jsonSpecific:
            if specific.get('name') == 'From':
                emailFrom = specific.get('value')
                try:
                    dictRes["from"] = emailFrom[0:emailFrom.index("<")-1]
                except:
                    dictRes["from"] = emailFrom
                continue
            if specific.get('name') == 'Subject':
                dictRes["subject"] = specific.get('value')
                break
        result.append(dictRes)
    return result