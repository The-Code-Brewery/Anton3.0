# Reference : https://docs.atlassian.com/software/jira/docs/api/REST/8.5.3 
# Reference : https://developer.atlassian.com/cloud/jira/platform/rest/v2/
# https://id.atlassian.com/manage/api-tokens - create the api token
# https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/ - doing it

from configparser import ConfigParser
from constants import BASE_URL
import requests
import base64

class JiraAPI:
	headers={}
	base_url=BASE_URL

	@staticmethod
	def get_from_config(item):

		config = ConfigParser()
		config.read('../secret.ini')
		try:
			return config.get('Jira',item)
		except:
			return None

	def __init__(self):
		"""
		Get the username and password from the secrets.ini file
		"""

		email = self.get_from_config("email")
		api_token = self.get_from_config("api_token")

		required_string = f"{email}:{api_token}"
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
				params=params
			)
		# Return the response to get the required data
		try:
			return response.json()
		except:
			return None

	# Application roles

	def get_application_roles_all(self):
		"""
		Returns all application roles.
		"""

		route = "rest/api/2/applicationrole"
		return self.get(route=route) or {}

	def get_application_roles(self,key):
		"""
		Returns an application roles.
		
		:key: - The key of the application role.
		"""

		route = f"rest/api/2/applicationrole/{key}"
		return self.get(route=route) or {}

	# Audit Records

	def get_audit_records(self,startat=None,maxresults=None):
		"""
		Returns a list of audit records.

		:startat: - The number of records to skip before returning the first result.
		:maxresults: - The maximum number of results to return.
		"""

		params={}
		if(startat):
			params["startat"] = startat
		if(maxresults):
			params["maxresults"] = maxresults
		route = "rest/api/2/auditing/record"
		return self.get(route=route,params=params) or {}

	# Avatars

	def get_system_avatars_by_type(self,avtype):
		""" 
		Returns a list of system avatar details by owner type, where the owner
		types are issue type, project, or user.

		:avtype: - avatar type
		"""

		route = f"rest/api/2/avatar/{avtype}/system"
		return self.get(route=route) or {}

	def get_avatars(self,avtype,entityid):
		"""
		Returns the system and custom avatars for a project or issue type.

		:avtype: - avatar type
		:entityid: - The ID of the item the avatar is associated with.
		"""

		route = f"rest/api/2/universal_avatar/type/{avtype}/owner/{entityid}"
		return self.get(route=route) or {}

	# Dashboard

	def get_all_dashboards(self,startat=None,maxresults=None):

		params={}
		if(startat):
			params["startAt"] = startat
		if(maxresults):
			params["maxResults"] = maxresults
		route = "rest/api/2/dashboard"
		return self.get(route=route,params=params) or {}

	def search_for_dashboards(self,name=None,accid=None,groupname=None):
		
		params={}
		if(name):
			params["dashboardName"] = name
		if(accid):
			params["accountId"] = accid
		if(groupname):
			params["groupname"] = groupname
		route = "rest/api/2/dashboard/search"
		return self.get(route=route,params=params) or {}

	def get_dashboard_item_property_keys(self,dashboardId,itemId):

		route = f"rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties"
		return self.get(route=route) or {}

	def get_dashboard_item_property(self,dashboardId,itemId,propertyKey):

		route = f"rest/api/2/dashboard/{dashboardId}/items/{itemId}/properties/{propertyKey}"
		return self.get(route=route) or {}

	def get_dashboard(self,dId):
		route = f"rest/api/2/dashboard/{dId}"
		return self.get(route=route) or {}

	# Filter

	def get_filter(self,fId):
		route = f"rest/api/2/filter/{fId}"
		return self.get(route=route) or {}

	def get_my_filters(self):
		route = "rest/api/2/filter/my"
		return self.get(route=route) or {}

	# Groups

	def get_users_from_group(self,groupname,includeInactiveUsers=None,startAt=None,maxResults=None):
		params={}
		params["groupname"] = groupname
		if(includeInactiveUsers):
			params["includeInactiveUsers"] = includeInactiveUsers
		if(startat):
			params["startat"] = startat
		if(maxResults):
			params["maxResults"] = maxResults
		route = "rest/api/2/group/member"
		return self.get(route=route,params=params) or {}

	# Issues --partial

	def get_issue(self,issueIdOrKey):

		route = f"rest/api/2/issue/{issueIdOrKey}"
		return self.get(route=route) or {}

	def get_changelogs(self,issueIdOrKey,startAt=None,maxResults=None):

		params={}
		if(startat):
			params["startat"] = startat
		if(maxResults):
			params["maxResults"] = maxResults
		route = f"rest/api/2/issue/{issueIdOrKey}/changelog"
		return self.get(route=route,params=params) or {}

	def get_transitions(self,issueIdOrKey,transitionId=None):

		params={}
		if(transitionId):
			params["transitionId"] = transitionId
		route = f"rest/api/2/issue/{issueIdOrKey}/changelog"
		return self.get(route=route,params=params) or {}

	def get_comments(self,issueIdOrKey,startAt=None,maxResults=None):

		params={}
		if(startat):
			params["startat"] = startat
		if(maxResults):
			params["maxResults"] = maxResults
		route = f"rest/api/2/issue/{issueIdOrKey}/comments"
		return self.get(route=route,params=params) or {}

	def get_comment(self,issueIdOrKey,cId):

		route = f"rest/api/2/issue/{issueIdOrKey}/comment/{cId}"
		return self.get(route=route) or {}

	# Permissions

	def get_my_permissions(self):

		"""
		Provide permission information for the current user.
		"""

		route = "rest/api/2/mypermissions"
		return self.get(route=route) or {}

	def get_permissions_all(self):

		"""
		Provide permission information for the current user.
		"""

		route = "rest/api/2/permissions"
		return self.get(route=route) or {}

	def get_property(self,key=None,permissionLevel=None):

		"""
		Returns an application property.

		:key: OPT
		:permissionLevel: OPT
		"""

		params={}
		if(key):
			params["key"] = key
		if(permissionLevel):
			params["permissionLevel"] = permissionLevel

		route = "rest/api/2/application-properties"
		return self.get(route=route,params=params)

	# Projects -- partial

	def get_project(self,projectIdOrKey):

		route = f"rest/api/2/project/{projectIdOrKey}"
		return self.get(route=route) or {}

	def get_all_projects(self,startAt=None,maxResults=None):

		params={}
		if(startat):
			params["startat"] = startat
		if(maxResults):
			params["maxResults"] = maxResults
		route = f"rest/api/2/project/search"
		return self.get(route=route,params=params) or {}

	# User

	def get_user(self,accountId=None):

		params={}
		if(accountId):
			params["accountId"] = accountId
		route = f"rest/api/2/project/search"
		return self.get(route=route,params=params) or {}
