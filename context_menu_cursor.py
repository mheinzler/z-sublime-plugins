"""Context menu command that also positions the cursor."""

import sublime_plugin


class ContextMenuCursorCommand(sublime_plugin.TextCommand):
    """Context menu command that also positions the cursor."""

    def run(self, edit, event, *args):
        """Run the command."""
        self.view.run_command("drag_select", {"event": event})
        self.view.run_command("context_menu", {"event": event})

    def want_event(self):
        """Whether we need the event data."""
        return True
