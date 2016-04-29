from .b_build import get_dist_file_path
from .b_build import b_build
from ..zn_api.service_dao import upload_draft
from ..wg_util import service_context_message
from ..wg_util import api_response_message


def b_deploy(context, args):
    if 'services' not in context['plugin']:
        return deploy_one_service(context, args)
    services = context['plugin'].pop('services')
    for service in services:
        context['service'] = service
        deploy_one_service(context, args)


def deploy_one_service(context, args):
    b_build(context, args)
    print service_context_message("Deploying", context)
    response = do_deploy(context)
    print api_response_message(response)


def do_deploy(context):
    path = get_dist_file_path(context)
    return upload_draft(context, path)
