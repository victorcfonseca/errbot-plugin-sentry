# errbot-plugin-sentry

#sentry #github #errbot #slack

This plugin is designed to be run inside an [errbot-based](https://errbot.readthedocs.io/en/latest/) bot and installed in your Slack workspace. When invoked, it will:

1. [create a new project in Sentry](https://docs.sentry.io/product/sentry-basics/guides/integrate-frontend/create-new-project/) based on input from a requester and already assign it to a previously created team
2. add the repository informed if it has Sentry x Github integration.

## How its works?
As with all [other plugins](https://github.com/topics/errbot-plugins), the 'sentry.plug' and 'sentry.py' files must be placed inside the errbot's /plugins directory.

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

