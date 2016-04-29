from frontend.f_deploy import f_deploy
from backend.b_deploy import b_deploy


def deploy(context, args):
    if args['--frontend']:
        return f_deploy(context, args)
    if args['--backend']:
        return b_deploy(context, args)
    f_deploy(context, args)
    b_deploy(context, args)
