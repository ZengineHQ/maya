"""Maya (Zengine Plugin Build Automation).

Usage:
  maya (build | deploy | publish) [options] [<plugin>] [<environment>]
  maya service (build | deploy) <service> [<environment>]
  maya sublime-deploy <current-file-path>
  maya (-h | --help)
  maya --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -y            Publish without prompt.

"""
from docopt import docopt
from .wg_util import get_plugin_context
from .wg_util import get_service_context
from .wg_util import get_all_plugin_contexts
from .build import build
from .deploy import deploy
from .publish import publish
from .publish import prompt_publish
from .sublime_deploy import sublime_deploy
from .service.service_build import service_build
from .service.service_deploy import service_deploy
from .exception import MayaException
import sys

__version__ = "1.1.0"


def main():
    arguments = docopt(__doc__, version=__version__)

    try:
        execute(arguments)

    except MayaException as e:
        sys.exit(e)


def execute(arguments):
    if arguments['sublime-deploy']:
        sublime_deploy(arguments['<current-file-path>'])
    else:
        execute_normal_flow(arguments)


def execute_normal_flow(arguments):
    action = parse_action(arguments)

    contexts = parse_contexts(arguments)

    for context in contexts:
        action(context)


def parse_action(arguments):
    if arguments['service']:
        return parse_service_action(arguments)
    return parse_plugin_action(arguments)


def parse_service_action(arguments):
    if arguments['build']:
        return service_build

    if arguments['deploy']:
        return service_deploy


def parse_plugin_action(arguments):
    if arguments['build']:
        return build

    if arguments['deploy']:
        return deploy

    if arguments['publish']:
        if arguments['-y']:
            return publish
        else:
            return prompt_publish


def parse_contexts(arguments):
    if arguments['<service>']:
        context = get_service_context(arguments['<service>'], arguments['<environment>'])
        return [context]

    if arguments['<plugin>']:
        context = get_plugin_context(arguments['<plugin>'], arguments['<environment>'])
        return [context]

    return get_all_plugin_contexts()
