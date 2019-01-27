"""Improve viewing package resources."""

import sublime_plugin

from .tools.patch import *


def plugin_loaded():
    """Apply patches."""

    # Force a reload of the plugin and do the patching here. The
    # package_resources module reloads the package_resource_viewer module on
    # the first start which would otherwise mess with the patching.
    sublime_plugin.reload_plugin(
        "PackageResourceViewer.package_resource_viewer")
    from PackageResourceViewer import package_resource_viewer

    @patch(package_resource_viewer.PackageResourceViewerBase)
    def insert_text(patch, self, content, view):
        """Call the original method and detect the indentation."""
        patch.original(self, content, view)
        if not view.is_loading():
            view.run_command("detect_indentation")

    apply_patches(__name__)


def plugin_unloaded():
    """Restore patches."""
    restore_patches(__name__)
