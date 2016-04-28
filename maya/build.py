from build_canonical import make_canonical_builder
from build_namespaced import make_namespaced_builder


def build(context, args):
    plugin = context['plugin']
    print "Building {0}".format(plugin['name'])
    canonical = make_canonical_builder()
    namespaced = make_namespaced_builder()
    canonical.build(plugin['name'])
    namespaced.build(
        plugin['name'],
        plugin['namespace'],
        plugin['route']
    )
    print "Done"
