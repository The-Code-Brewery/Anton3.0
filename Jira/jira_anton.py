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
