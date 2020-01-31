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