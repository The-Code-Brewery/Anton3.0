from . import jira_anton as ja

def get_time(seconds):

	intervals = [
	    ('weeks', 604800),  # 60 * 60 * 24 * 7
	    ('days', 86400),    # 60 * 60 * 24
	    ('hours', 3600),    # 60 * 60
	    ('minutes', 60),
	    ('seconds', 1),
	    ]
	def display_time(seconds, granularity=2):
	    result = []
	    for name, count in intervals:
	        value = seconds // count
	        if value:
	            seconds -= value * count
	            if value == 1:
	                name = name.rstrip('s')
	            result.append("{} {}".format(value, name))
	    return ', '.join(result[:granularity])

	return display_time(seconds)

def project_status(project_key,speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	proj = jira.get_project(project_key)

	speak(f"Status of project {proj.name}")
	speak(f"The current leader is {proj.lead.displayName}")
	speak("The latest version is version one point oh point oh") 
	speak(f"The are totally 7 issues pending")

def all_issues_in(project_key,speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issues = jira.get_issues_in_project(project_key)

	speak(f"there are {len(issues)} issues")
	speak("listing the top 5 issues")
	for issue in issues[0:5]:
		speak(f"{issue.fields.summary} assigned to {issue.fields.assignee.displayName if issue.fields.assignee != None else 'No one' }")

def all_my_issues_in(project_key,speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issues = jira.get_issues_of_current_user_in_project(project_key)

	speak(f"there are {len(issues)} issues")
	speak("listing the top 5 issues")
	for issue in issues[0:5]:
		speak(f"{issue.fields.summary}. the priority is {issue.fields.priority}.{'it is due by'+str(get_time(issue.fields.timeestimate)) if issue.fields.timeestimate != None else 'there is no deadline'}")

def all_my_issues(speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issues = jira.get_issues_of_current_user()

	speak(f"there are {len(issues)} issues")
	speak("listing the top 5 issues")
	for issue in issues[0:5]:
		speak(f"{issue.fields.summary}. It is from project {issue.fields.project.name} .the priority is {issue.fields.priority}.{'it is due by'+str(get_time(issue.fields.timeestimate)) if issue.fields.timeestimate != None else 'there is no deadline'}")

def all_my_issues_in_latest(project_key,speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issue = jira.get_issues_of_current_user_in_project(project_key)[0]
	speak("Here is the latest issue assigned to you")
	speak(f"{issue.fields.summary}. the priority is {issue.fields.priority}.{'it is due by'+str(get_time(issue.fields.timeestimate)) if issue.fields.timeestimate != None else 'there is no deadline'}")
	speak("Here is the description")
	speak(f"{issue.fields.description}")

def all_my_issues_latest(speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issue = jira.get_issues_of_current_user()[0]

	speak("Here is the latest issue assigned to you")
	speak(f"it is from project {issue.fields.project.name}")
	speak(f"{issue.fields.summary}. the priority is {issue.fields.priority}. {'it is due by'+str(get_time(issue.fields.timeestimate)) if issue.fields.timeestimate != None else 'there is no deadline'}")
	speak("Here is the description")
	speak(f"{issue.fields.description}")

def all_issues_in_latest(project_key,speak):

	jira = ja.AntonJira('https://anton3.atlassian.net','thenameisanton3@gmail.com', 'TKLhcdc5zw2anmiX8DQ946BD')
	issue = jira.get_issues_in_project(project_key)[0]

	speak(f"Here is the latest issue from project {issue.fields.project.name}")
	speak(f"{issue.fields.summary}. the priority is {issue.fields.priority}. {'it is due by'+str(get_time(issue.fields.timeestimate)) if issue.fields.timeestimate != None else 'there is no deadline'}")
	speak("Here is the description")
	speak(f"{issue.fields.description}")