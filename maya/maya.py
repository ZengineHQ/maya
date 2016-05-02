"""Maya (Zengine Plugin Build Automation).

Usage:
  maya build [<plugin>] [--frontend | --backend] [--env=ENV]
  maya deploy [<plugin>] [--frontend | --backend] [--env=ENV]
  maya publish [<plugin>] [--frontend | --backend] [--env=ENV] [-y]
  maya service (build | deploy) <service> [--env=ENV]
  maya sublime-deploy <current-file-path>
  maya --help
  maya --version

Options:
  -h --help        Show this screen.
  -v --version     Show version.
  -y               Publish without prompt.

"""
from docopt import docopt
from .wg_util import get_plugin_context
from .wg_util import get_service_context
from .wg_util import get_all_plugin_contexts
from .build import build
from .deploy import deploy
from .publish import publish
from .sublime_deploy import sublime_deploy
from .backend.b_build import b_build
from .backend.b_deploy import b_deploy
from .exception import MayaException
import sys

__version__ = "2.0.edge"


def main():
    args = docopt(__doc__, version=__version__)
    try:
        execute(args)
    except MayaException as e:
        sys.exit(e)


def execute(args):
    if args['sublime-deploy']:
        return sublime_deploy(args['<current-file-path>'], args)
    return execute_normal_flow(args)


def execute_normal_flow(args):
    action = parse_action(args)
    contexts = parse_contexts(args)
    for context in contexts:
        action(context, args)


def parse_action(args):
    if args['service']:
        return parse_service_action(args)
    return parse_plugin_action(args)


def parse_service_action(args):
    if args['build']:
        return b_build
    if args['deploy']:
        return b_deploy


def parse_plugin_action(args):
    if args['build']:
        return build
    if args['deploy']:
        return deploy
    if args['publish']:
        return publish


def parse_contexts(args):
    if args['<service>']:
        context = get_service_context(args['<service>'], args['--env'])
        return [context]
    if args['<plugin>']:
        context = get_plugin_context(args['<plugin>'], args['--env'])
        return [context]
    return get_all_plugin_contexts(args['--env'])
