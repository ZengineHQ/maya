from frontend.f_build import f_build
from backend.b_build import b_build


def build(context, args):
    if args['--frontend']:
        return f_build(context, args)
    if args['--backend']:
        return b_build(context, args)
    f_build(context, args)
    b_build(context, args)
