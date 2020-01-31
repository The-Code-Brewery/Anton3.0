from atlassian.rest_client import AtlassianRestAPI
from configparser import ConfigParser

class BitbucketAPI(AtlassianRestAPI):
	# from constants import BASE_URL
	bulk_headers = {"Content-Type": "application/vnd.atl.bitbucket.bulk+json"}

	@staticmethod
	def get_from_config(item):

		config = ConfigParser()
		try:
			config.read('./secret.ini')
		except:
			config.read('../secret.ini')
		try:
			return config.get('Bitbucket',item)
		except:
			return None

	def __init__(self):

		url = self.get_from_config("url")
		username = self.get_from_config("username")
		password = self.get_from_config("password")
		cloud = self.get_from_config("cloud")

		super(BitbucketAPI,self).__init__(url=url,username=username,password=password,cloud=cloud)


	def get_details(self):
		"""
		:no params:

		Returns the currently logged in user's details.
		"""
		if not self.cloud:
			url = '1.0/user'
		else:
			url = '2.0/user'
		return self.get(url) or {}

	def get_emails(self):
		"""
		:no params:

		Returns all the authenticated user's email addresses. Both confirmed and
		unconfirmed.
		"""
		if not self.cloud:
			url = '1.0/user/emails'
		else:
			url = '2.0/user/emails'
		return self.get(url) or {}  

	def get_user_emails(self,email):
		"""
		:email:

		Returns details about a specific one of the authenticated user's email
		addresses.
		"""
		if not self.cloud:
			url = '1.0/user/emails/{0}'.format(email)
		else:
			url = '2.0/user/emails/{0}'.format(email)
		return self.get(url) or {}  

	def get_repositories_permissions(self):
		"""
		:no params:

		Returns an object for each repository the caller has explicit access to and
		their effective permission — the highest level of permission the caller has.
		This does not return public repositories that the user was not granted any
		specific permission in, and does not distinguish between direct and indirect
		privileges.
		"""
		if not self.cloud:
			url = '1.0/user/permissions/repositories'
		else:
			url = '2.0/user/permissions/repositories'
		return self.get(url) or {}  

	def get_team_permissions(self):
		"""
		:no params:

		Returns an object for each team the caller is a member of, and their
		effective role — the highest level of privilege the caller has. If a user is
		a member of multiple groups with distinct roles, only the highest level is
		returned.
		"""

		if not self.cloud:
			url = '1.0/user/permissions/teams'
		else:
			url = '2.0/user/permissions/teams'
		return self.get(url) or {}

	def get_user_details(self,user):
		"""
		:username:

		Gets the public information associated with a user account.
		"""

		if not self.cloud:
			url = '1.0/users/{0}'.format(user)
		else:
			url = '2.0/users/{0}'.format(user)
		return self.get(url) or {}

	def get_team_users(self,user):
		"""
		:username:

		Returns all members of the specified team. Any member of any of the team's
		groups is considered a member of the team. This includes users in groups
		that may not actually have access to any of the team's repositories.
		"""

		if not self.cloud:
			url = '1.0/users/{0}/members'.format(user)
		else:
			url = '2.0/users/{0}/members'.format(user)
		return self.get(url) or {}

	def get_user_repositories(self,workspace):
		"""
		:workspace:

		All repositories owned by a user/team. This includes private repositories,
		but filtered down to the ones that the calling user has access to.
		"""
		if not self.cloud:
			url = '1.0/users/{0}/repositories'.format(workspace)
		else:
			url = '2.0/users/{0}/repositories'.format(workspace)
		return self.get(url) or {}

	def search_user_code(self,user,code=None):
		"""
		:code:

		Search for code in the repositories of the specified user
		"""

		params={}
		if(code):
			params["search_query"]=code

		if not self.cloud:
			url = '1.0/users/{0}/search/code'.format(user)
		else:
			url = '2.0/users/{0}/search/code'.format(user)
		return self.get(url,params=params) or {}

	def get_user_repo_commits(self,workspace,repo_slug):
		if not self.cloud:
			url = f'1.0/repositories/{workspace}/{repo_slug}/commits/'
		else:
			url = f'2.0/repositories/{workspace}/{repo_slug}/commits/'
		return self.get(url) or {}

	def get_user_repo_commit(self,workspace,repo_slug,commit_hash):
		if not self.cloud:
			url = f'1.0/repositories/{workspace}/{repo_slug}/commit/{commit_hash}'
		else:
			url = f'2.0/repositories/{workspace}/{repo_slug}/commit/{commit_hash}'
		return self.get(url) or {}

	def get_user_repo_commit_diff(self,workspace,repo_slug,commit_hash):
		if not self.cloud:
			url = f'1.0/repositories/{workspace}/{repo_slug}/diff/{commit_hash}'
		else:
			url = f'2.0/repositories/{workspace}/{repo_slug}/diff/{commit_hash}'
		return self.get(url) or {}

	def get_user_repo_downloads(self,workspace,repo_slug):
		if not self.cloud:
			url = f'1.0/repositories/{workspace}/{repo_slug}/downloads'
		else:
			url = f'2.0/repositories/{workspace}/{repo_slug}/downloads'
		return self.get(url) or {}

	def get_user_repo_pullrequests(self,workspace,repo_slug):
		if not self.cloud:
			url = f'1.0/repositories/{workspace}/{repo_slug}/pullrequests'
		else:
			url = f'2.0/repositories/{workspace}/{repo_slug}/pullrequests'
		return self.get(url) or {}