from .service_build import get_dist_file_path
from .service_build import service_build
from ..zn_api.service_dao import upload_service
from ..wg_util import service_context_message
from ..wg_util import api_response_message


def service_deploy(context):

    service_build(context)

    print service_context_message("Deploying", context)

    response = do_deploy(context)

    print api_response_message(response)


def do_deploy(context):
    path = get_dist_file_path(context)
    files = {
        'draftSource': ('dist.zip', open(path, 'rb'), 'application/zip', {'Expires': '0'})
    }
    return upload_service(context, files)
