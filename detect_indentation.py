"""Improve indentation detection."""

import Default.detect_indentation

original_run = Default.detect_indentation.DetectIndentationCommand.run


def run(self, edit, show_message=True, threshold=1):
    """Call the original method with a smaller default threshold."""
    original_run(self, edit, show_message, threshold)


def plugin_loaded():
    """Overwrite the run method."""
    Default.detect_indentation.DetectIndentationCommand.run = run


def plugin_unloaded():
    """Restore the original run method."""
    Default.detect_indentation.DetectIndentationCommand.run = original_run
