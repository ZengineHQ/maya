from zn_api.plugin_dao import update_plugin
from deploy import deploy
from wg_util import plugin_context_message
from wg_util import api_response_message
from wg_util import query_yes_no


def publish(context, args):
    should_publish = prompt(context, args)
    if should_publish:
        execute(context, args)


def prompt(context, args):
    if args['-y']:
        return True
    question = plugin_context_message("Publish", context) + "?"
    return query_yes_no(question)


def execute(context, args):
    deploy(context, args)
    print plugin_context_message("Publishing", context)
    response = do_publish(context)
    print api_response_message(response)


def do_publish(context):
    request = {}
    request['publish'] = True
    return update_plugin(context, request)
