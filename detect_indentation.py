"""Improve indentation detection."""

from Default import detect_indentation

from .tools.patch import *


@patch(detect_indentation.DetectIndentationCommand)
def run(patch, self, edit, show_message=True, threshold=1):
    """Call the original method with a smaller default threshold."""
    patch.original(self, edit, show_message, threshold)


def plugin_loaded():
    """Apply patches."""
    apply_patches(__name__)


def plugin_unloaded():
    """Restore patches."""
    restore_patches(__name__)
