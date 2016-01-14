from zn_api.zn_plugin_api import update_plugin
from wg_util import plugin_context_message
from wg_util import api_response_message
from build import build
from build_namespaced import make_namespaced_builder


def deploy(context):

    build(context)

    print plugin_context_message("Deploying", context)

    response = do_deploy(context)

    print api_response_message(response)


def do_deploy(context):

    request = assemble_deploy_request(context)

    return update_plugin(context, request)


def assemble_deploy_request(context):

    builder = make_namespaced_builder()

    request = {}
    request['draftJs'] = builder.contents_of_file(context, "js")
    request['draftHtml'] = builder.contents_of_file(context, "html")
    request['draftCss'] = builder.contents_of_file(context, "css")

    return request
