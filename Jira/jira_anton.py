from jira import JIRA

class AntonJira():

	def __init__(self,server,email,apitoken):
		self.jira_instance = JIRA(server = server, basic_auth = (email,apitoken))

	def get_project(self,project_key):
		"""
		name -- project name
		lead.displayName -- leader name
		"""
		return self.jira_instance.project(project_key)

	def get_project_components(self,project):
		"""
		requires : project instance
		returns : list of components
		"""
		return [comp.name for comp in self.jira_instance.project_components(project)]

	def get_issue_detail(self,issue_key):
		"""
		.fields.summary -- summary
		.fields.votes.votes -- votes
		.fields.description
		.fields.comment : [{
			.author.displayName
			.body
		}]
		"""
		return self.jira_instance.issue(issue_key)

	def get_issues_in_project(self,project_key):
		"""
		[
			.fields.summary -- summary
			.fields.votes.votes -- votes
			.fields.description
			.fields.comment : [{
				.author.displayName
				.body
			}]
		]
		"""
		return self.jira_instance.search_issues(f"project={project_key}")

	def get_issues_of_current_user_in_project(self,project_key):
		"""
		[
			.fields.summary -- summary
			.fields.votes.votes -- votes
			.fields.description
			.fields.comment : [{
				.author.displayName
				.body
			}]
		]
		"""
		return self.jira_instance.search_issues(f"project={project_key} and assignee=currentuser()")

	def get_issues_of_current_user(self):
		"""
		[
			.fields.summary -- summary
			.fields.votes.votes -- votes
			.fields.description
			.fields.comment : [{
				.author.displayName
				.body
			}]
		]
		"""
		return self.jira_instance.search_issues(f"assignee=currentuser()")
 
# jira = JIRA('https://anton3.atlassian.net',basic_auth=('thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD'))
# jra = jira.project('AN')
# print(jra.name)              
# print(jra.lead.displayName)    
 
# email:thenameisanton3@gmail.com
# password: pratikbaid@2471

# jira = AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
# print(jira.get_issues_of_current_user('AN'))