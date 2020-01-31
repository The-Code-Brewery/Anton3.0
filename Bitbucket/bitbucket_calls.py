from . import bitbucket

def get_all_repos(workspace,speak):

	bb = bitbucket.BitbucketAPI()

	data = bb.get_user_repositories(workspace)

	speak(f"there are {len(data['values'])} repositories")

def get_last_commit(workspace,repo_slug,speak):

	bb = bitbucket.BitbucketAPI()

	data = bb.get_user_repo_commits(workspace,repo_slug)
	values = data["values"][0]
	commit_hash = values["hash"]
	data_commit = bb.get_user_repo_commit(workspace,repo_slug,commit_hash)
	speak(f"the latest commit was made by{data_commit['author']['raw']}")
	speak(f"the commit message was {values['rendered']['message']['raw']}")

def get_last_pullrequest(workspace,repo_slug,speak):
	bb = bitbucket.BitbucketAPI()

	data = bb.get_user_repo_pullrequests(workspace,repo_slug)
	speak(f"there are {len(data['values'])} pull requests")
	speak(f"the request is from the branch {data['values'][0]['source']['branch']} to the branch {data['values'][0]['destination']['branch']}")
	speak(f"the title is {data['values'][0]['title']}")

def get_last_commit_for_email(workspace,repo_slug,emailAutomatorDetailMail):
	bb = bitbucket.BitbucketAPI()
	data = bb.get_user_repo_commits(workspace,repo_slug)
	values = data["values"][0]
	commit_hash = values["hash"]
	data_commit = bb.get_user_repo_commit(workspace,repo_slug,commit_hash)

	emailBody='Author:  '+data_commit['author']['raw']
	emailBody=emailBody +'\n'
	emailBody=emailBody +'Message:  '
	emailBody=emailBody + values['rendered']['message']['raw']
	emailAutomatorDetailMail("The Bitbucket data with the last commit",emailBody)

def get_last_pullrequest_for_email(workspace,repo_slug,emailAutomatorDetailMail):
	bb = bitbucket.BitbucketAPI()
	data = bb.get_user_repo_pullrequests(workspace,repo_slug)
	noOfPullReq=str(len(data['values']))
	fromBranch=str(data['values'][0]['source']['branch'])
	toBranch=str(data['values'][0]['destination']['branch'])
	title=str(data['values'][0]['title'])

	emailBody='There are '+noOfPullReq+' pull requests.\nThe request is from the branch '+fromBranch+' to the branch '+toBranch+'\nTitle: '+title
	emailAutomatorDetailMail("The Bitbucket data with the last commit",emailBody)