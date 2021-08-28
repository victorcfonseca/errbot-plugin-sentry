# errbot-plugin-sentry

#sentry #github #errbot #slack

This plugin is designed to be run inside an [errbot-based](https://errbot.readthedocs.io/en/latest/) bot and installed in your Slack workspace. The idea is to give autonomy to any developer in an IT Engineering structure instead of having to open a ticket and wait for the activity to be done. When invoked, it will:

1. [create a new project in Sentry](https://docs.sentry.io/product/sentry-basics/guides/integrate-frontend/create-new-project/) based on input from a requester and already assign it to a previously created team
2. add the repository informed if it has [Sentry x Github integration](https://sentry.io/integrations/github/).

## How its works?
As with all [other plugins](https://github.com/topics/errbot-plugins), the 'sentry.plug' and 'sentry.py' files must be placed inside the errbot's /plugins/<your-directory-plugin-name> directory, as in the structure shown below:
```
|_ errbot
   |_ plugins
      |_ sentry
         - sentry.plug
         - sentry.py
```

It has been tested and validated on Slack with the following packages:
- errbot 6.1.7 (`!about` to check version)
- slackclient 1.3.2 (`pip list` to check installed packages)
- websocket-client 0.54.0 (`pip list` to check installed packages)

## Environment Variables
- [GITHUB_ORG](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-your-membership-in-organizations/accessing-an-organization)
- [SENTRY_ORG_SLUG]
- [SENTRY_TOKEN]
- [SENTRY_GITHUB_INTEGRATION_ID]

## Sintaxe
You need to pass two parameters in the command to your bot:
- name of the project to be created within Sentry
- team created within Sentry

Example:
```
@your_bot sentry create project *vf-validate-java-monitoring* for *sre*
```

