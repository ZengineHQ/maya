import sys
import re
from plugin_environment import make_environment


def get_plugin_context(plugin_name, environment_name=None):
    environment = make_environment(environment_name)
    return environment.get_plugin_context(plugin_name)


def get_service_context(service_name, environment_name=None):
    environment = make_environment(environment_name)
    return environment.get_service_context(service_name)


def get_all_plugin_contexts(environment_name=None):
    environment = make_environment(environment_name)
    return environment.get_all_plugin_contexts()


def plugin_context_message(action, context):
    return "{0} {1} {2} to {3}".format(
        action,
        context['plugin']['name'],
        context['plugin']['id'],
        context['api']['endpoint']
    )


def service_context_message_simple(action, context):
    return "{0} {1}/{2}".format(
        action,
        context['plugin']['name'],
        context['service']['name']
    )


def service_context_message(action, context):
    return "{0} {1}/{2} {3}/{4} to {5}".format(
        action,
        context['plugin']['name'],
        context['service']['name'],
        context['plugin']['id'],
        context['service']['id'],
        context['api']['endpoint']
    )


def api_response_message(response):
    return "Done"


def query_yes_no(question):
    valid = {
        "yes": True, "y": True, "ye": True,
        "no": False, "n": False
    }
    prompt = " [y/n] "
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def convertToDashCase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()