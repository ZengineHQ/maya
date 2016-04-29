from frontend.f_build import f_build
from service.service_build import service_build


def build(context, args):
    if args['--frontend']:
        return f_build(context, args)
    if args['--backend']:
        return service_build(context, args)
    f_build(context, args)
    service_build(context, args)
