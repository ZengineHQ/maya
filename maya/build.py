from build_canonical import make_canonical_builder
from build_namespaced import make_namespaced_builder


class PluginCodeBuilder:

    def __init__(self, canonical_builder, namespaced_builder):
        self.canonical_builder = canonical_builder
        self.namespaced_builder = namespaced_builder

    def build(self, context):
        self.canonical_builder.build(context)
        self.namespaced_builder.build(context)


def build(context):
    print "Building {0}".format(context['plugin_name'])

    make_builder().build(context)

    print "Done"


def make_builder():
    canonical = make_canonical_builder()
    namespaced = make_namespaced_builder()

    return PluginCodeBuilder(canonical, namespaced)
