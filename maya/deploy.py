from frontend.f_deploy import f_deploy
from service.service_deploy import service_deploy


def deploy(context, args):
    if args['--frontend']:
        return f_deploy(context, args)
    if args['--backend']:
        return service_deploy(context, args)
    f_deploy(context, args)
    service_deploy(context, args)
