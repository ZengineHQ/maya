from zn_api.plugin_dao import update_plugin
from wg_util import plugin_context_message
from wg_util import api_response_message
from build import build
from build_namespaced import make_namespaced_builder


def deploy(context, args):
    build(context, args)
    print plugin_context_message("Deploying", context)
    response = do_deploy(context)
    print api_response_message(response)


def do_deploy(context):
    request = assemble_deploy_request(context)
    return update_plugin(context, request)


def assemble_deploy_request(context):
    builder = make_namespaced_builder()
    name = context['plugin']['name']
    request = {}
    request['draftJs'] = builder.contents_of_file(name, "js")
    request['draftHtml'] = builder.contents_of_file(name, "html")
    request['draftCss'] = builder.contents_of_file(name, "css")
    return request
