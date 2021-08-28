from errbot import BotPlugin, re_botcmd

import requests
import json
import os


class Sentry(BotPlugin):

    @re_botcmd(pattern=r"(sentry create project)\b\s\b([\w\/\-]+) for ([\w\-]+)")
    def create_project(self, msg, match):
        '''
        Create sentry project <project_name> for <project_team> team
        '''

        # get evns
        org_github                      = os.environ['GITHUB_ORG']
        org_slug                        = os.environ['SENTRY_ORG_SLUG']
        token                           = os.environ['SENTRY_TOKEN']
        sentry_github_integration_id    = os.environ['SENTRY_GITHUB_ID']

        # headers
        headers = {"Content-Type": "application/json", "Authorization": "Bearer {token}".format(token=token)}

        # get author
        frm = str(msg.frm).split("/")

        if len(frm) == 2:
            _, author = frm
        if len(frm) == 1:
            author = frm[0][1:]

        feature, repo, team = match.groups()

        # check if team informed is valid
        url = "https://sentry.io/api/0/organizations/{org_slug}/teams/".format(org_slug=org_slug)

        resp = requests.get(url, headers=headers)
        json_data = json.loads(resp.text)

        teams = ""
        for item in json_data:
            teams += item['slug'] + ", "

        if team not in teams or team == "":
            self.send(
                msg.to,
                text=f":exclamation: You need to provide a valid Sentry team name. **{team}** is the team that you provided.",
                in_reply_to=msg,
            )
            self.send(
                msg.to,
                text=f":exclamation: The correct syntax is `sentry create project <project_name> for <team_name>` and the team options are: ```{teams}",
                in_reply_to=msg,
            )
            return

        # start to create the project
        url = "https://sentry.io/api/0/teams/{org_slug}/{team}/projects/".format(team=team, org_slug=org_slug)

        resp = requests.post(url, headers=headers, json={"name": repo, "slug": repo})

        self.send(
            msg.to,
            text=f":clock1: Trying to create project: {repo} on Sentry...",
            in_reply_to=msg,
        )

        if resp.status_code == 201:
            self.send(
                msg.to,
                text=f":rocket: Project {repo} **created** on Sentry inside team **{team}**",
                in_reply_to=msg,
            )
            self.send(
                msg.to,
                text=f"Sentry project link: https://sentry.io/organizations/{org_slug}/projects/{repo}/",
                in_reply_to=msg,
            )
        elif resp.status_code == 409:
            self.send(
                msg.to,
                text=f":exclamation: HTTP 409 - **Conflict** because the project **{repo}** already exists on Sentry. But, it's not a problem, ok? :grin:",
                in_reply_to=msg,
            )
            self.send(
                msg.to,
                text=f"Sentry project link: https://sentry.io/organizations/{org_slug}/projects/{repo}/",
                in_reply_to=msg,
            )
        else:
            self.send(
                msg.to,
                text=f":exclamation: Error! :cry: HTTP {resp.status_code} - `{resp.content}`",
                in_reply_to=msg,
            )

        # add repo to Github x Sentry integration
        self.send(
            msg.to,
            text=f":clock1: Trying to add project on Sentry x Github integration...",
            in_reply_to=msg,
        )

        url = "https://sentry.io/api/0/organizations/{org_slug}/repos/".format(org_slug=org_slug)

        response = requests.post(url, headers=headers, json={"installation": "" + sentry_github_integration_id + "", "identifier": "" + org_github + "/" + repo + "", "provider": "integrations:github"})

        if response.status_code == 201:
            self.send(
                msg.to,
                text=f":rocket: Project added to GitHub integration on Sentry",
                in_reply_to=msg,
            )
        else:
            self.send(
                msg.to,
                text=f":exclamation: Error! :cry: HTTP {response.status_code} - `{response.content}`",
                in_reply_to=msg,
            )

        # list DSN from project"
        url = "https://sentry.io/api/0/projects/{org_slug}/{repo}/keys/".format(repo=repo, org_slug=org_slug)

        resp = requests.get(url, headers=headers)
        json_data = json.loads(resp.text)

        # send private message to the requester with the DSN
        self.send(self.build_identifier("@" + author), text=f"Hey, @{author}! Here are the DSN of project **{repo}** on Sentry: {json_data[0]['dsn']['public']}",)

        self.send(
            msg.to,
            text=f"@{author}, I've sent the DSN config in private message to you!",
            in_reply_to=msg,
        )
