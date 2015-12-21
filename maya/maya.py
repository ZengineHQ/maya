"""Maya (Zengine Plugin Build Automation).

Usage:
  maya (build | deploy | publish) [options] [<plugin>] [<environment>]
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
from .wg_util import get_all_plugin_contexts
from .build import build
from .deploy import deploy
from .publish import publish
from .publish import prompt_publish
from .sublime_deploy import sublime_deploy
from .exception import MayaException
import sys

__version__ = "1.0.1"


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
    if arguments['build']:
        return build
    elif arguments['deploy']:
        return deploy
    elif arguments['publish']:
        if arguments['-y']:
            return publish
        else:
            return prompt_publish


def parse_contexts(arguments):
    if arguments['<plugin>']:
        context = get_plugin_context(arguments['<plugin>'], arguments['<environment>'])
        return [context]
    else:
        return get_all_plugin_contexts()
