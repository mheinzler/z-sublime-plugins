"""Improve the Corona Editor plugin."""

Corona_Editor = __import__("Corona Editor")


class CoronaDocsCommand(Corona_Editor.corona_docs.CoronaDocsCommand):
    """Improve the CoronaDocsCommand."""

    def is_visible(self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "(source.lua | source.luae) - entity"

        s = self.view.sel()[0]
        return self.view.match_selector(s.a, selector)


class CoronaDebuggerCommand(Corona_Editor.debugger.CoronaDebuggerCommand):
    """Improve the CoronaDebuggerCommand."""

    def is_enabled(self):
        """Enable for Lua and LuaExtended syntax."""
        selector = "(source.lua | source.luae) - entity"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False

    def is_visible(self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "source.lua | source.luae"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False


class ClearOutputPanelCommand(
        Corona_Editor.run_project.ClearOutputPanelCommand):
    """Improve the ClearOutputPanelCommand."""

    def is_enabled(self):
        """Enable only if visible to prevent clearing the panel."""
        if not self.is_visible():
            return False

        return super().is_enabled()

    def is_visible(self):
        """Show only for Lua and LuaExtended syntax."""
        selector = "source.lua | source.luae"

        view = self.window.active_view()
        if view is not None:
            s = view.sel()[0]
            return view.match_selector(s.a, selector)

        return False
