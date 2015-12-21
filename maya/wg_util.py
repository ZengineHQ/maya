import sys
from plugin_environment import make_environment

def get_plugin_context(plugin_name, environment_name=None):
    environment = make_environment(environment_name)
    return environment.get_plugin_context(plugin_name)

def get_all_plugin_contexts():
    environment = make_environment()
    return environment.get_all_plugin_contexts()

def plugin_context_message(action, context):
    return "{0} {1} {2} to {3}".format(action, context['plugin_name'], context['plugin_id'], context['api_endpoint'])

def api_response_message(response):
    return "Done"

def query_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    prompt = " [y/n] "

    while True:
        sys.stdout.write(question + prompt)

        choice = raw_input().lower()

        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
