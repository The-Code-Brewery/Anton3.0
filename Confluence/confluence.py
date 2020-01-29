# Reference : https://docs.atlassian.com/ConfluenceServer/rest/7.2.1/

from configparser import ConfigParser
from constants import BASE_URL
import requests
import base64


class Confluence:
    headers = {}
    base_url = BASE_URL

    @staticmethod
    def get_from_config(item):

        config = ConfigParser()
        config.read('../secret.ini')
        try:
            return config.get('Confluence',item)
        except:
            return None

    def __init__(self):
        """
        Get the username and access token from the secrets.ini file
        """

        username = self.get_from_config("username")
        access_token = self.get_from_config("accesstoken")

        required_string = f"{username}:{access_token}"
        encoded = base64.b64encode(
            required_string.encode("utf-8")).decode("utf-8")

        self.headers = {
            'Authorization': f"Basic {encoded}",
            'Content-Type': "application/json"
        }

    def get(self, route, params=None):
        """
        Get the API Response
        """
        print(f"{self.base_url}{route}")
        response = None
        if params is None:
            response = requests.get(
                f"{self.base_url}{route}",
                headers=self.headers,
            )
        else:
            response = requests.get(
                f"{self.base_url}{route}",
                headers=self.headers,
                params=[params, ]
            )
        # Return the response to get the required data
        return response

    def get_longtasks(self):
        """
        Returns information about all tracked long-running tasks
        """
        route = "wiki/rest/api/longtask"
        return self.get(route=route)

    def get_audit_records(self):
        """
        Fetch a paginated list of AuditRecord instances
        dating back to a certain time
        Can be modified to return records between certain dates
        """
        route = "wiki/rest/api/audit"
        return self.get(route=route)

    def get_content(self):
        """
        Returns a paginated list of Content
        Can be modified to get the records for a particular date
        or a start and end date
        """
        route = "wiki/rest/api/content"
        return self.get(route=route)

    def get_groups(self):
        """
        Returns a collection of user groups
        """
        route = "wiki/rest/api/group"
        return self.get(route=route)

    def get_specific_group(self, groupName):
        """
        Returns the user group with the specific group name
        """
        route = f"wiki/rest/api/group/{groupName}"
        return self.get(route=route)

    def get_members(self, groupName):
        """
        Returns the collection of users in a given group
        """
        route = f"wiki/rest/api/group/{groupName}/member"
        return self.get(route=route)

    def get_specific_task(self, taskID):
        """
        Returns information about a specific long running task
        """
        route = f"wiki/rest/api/longtask/{taskID}"
        return self.get(route=route)

    def get_spaces(self):
        """
        Returns information about the number of spaces
        """
        route = f"wiki/rest/api/space"
        return self.get(route=route)

    def get_specific_space(self, spaceKey):
        """
        Returns information about a specific space
        """
        route = f"wiki/rest/api/space/{spaceKey}"
        return self.get(route=route)

    def get_specific_space_content(self, spaceKey):
        """
        Returns the content in the given space
        """
        route = f"wiki/rest/api/space/{spaceKey}/content"
        return self.get(route=route)

    def get_user(self, accountId):
        """
        Get information about the current logged in user
        """
        params = ('accountId', accountId)
        route = f"wiki/rest/api/user"
        return self.get(route=route, params=params)

    def get_current_user(self):
        """
        Returns the current logged in user
        """
        route = f"wiki/rest/api/user/current"
        return self.get(route=route)

    def get_groups(self, accountId):
        """
        Returns the groups of the logged in user
        """
        params = ('accountId', accountId)
        route = f"wiki/rest/api/user/memberof"
        return self.get(route=route, params=params)
