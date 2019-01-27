"""Improve the Corona Editor plugin."""

from .tools.patch import *

try:
    Corona_Editor = __import__("Corona Editor")
except ImportError:
    pass
else:
    @patch(Corona_Editor.corona_docs.CoronaDocsCommand)
    def is_visible(patch, self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "(source.lua | source.luae) - entity"

        s = self.view.sel()[0]
        return self.view.match_selector(s.a, selector)

    @patch(Corona_Editor.debugger.CoronaDebuggerCommand)
    def is_enabled(patch, self):
        """Enable for Lua and LuaExtended syntax."""
        selector = "(source.lua | source.luae) - entity"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False

    @patch(Corona_Editor.debugger.CoronaDebuggerCommand) # noqa
    def is_visible(patch, self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "source.lua | source.luae"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False

    @patch(Corona_Editor.run_project.ClearOutputPanelCommand) # noqa
    def is_enabled(patch, self):
        """Enable only if visible to prevent clearing the panel."""
        if not self.is_visible():
            return False

        return patch.original(self)

    @patch(Corona_Editor.run_project.ClearOutputPanelCommand) # noqa
    def is_visible(patch, self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "source.lua | source.luae"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False


def plugin_loaded():
    """Apply the patches."""
    apply_patches(__name__)


def plugin_unloaded():
    """Restore the patches."""
    restore_patches(__name__)
