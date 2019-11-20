"""Change the behavior of SublimeLinter."""

import re

import sublime
import sublime_plugin


def is_building(window):
    """Check if there is an ongoing build process."""

    # the messages to be searched for to detect a finished build
    finished_regex = re.compile(r"^\[(Finished in .*|Cancelled)\]$",
                                re.MULTILINE)

    # find the build output
    exec_view = window.find_output_panel("exec")
    if exec_view:
        text = exec_view.substr(sublime.Region(0, exec_view.size()))

        # look for the finish strings
        if re.search(finished_regex, text):
            return False

        # still building
        return True

    # unknown
    return False


class LinterEventListener(sublime_plugin.EventListener):
    """Listen for events to change the behavior of SublimeLinter."""

    def on_window_command(self, window, command_name, args):
        """Listen to window commands and possibly rewrite them."""

        # prevent the panel to be shown automatically when a build is currently
        # running or the build panel is visible
        if command_name == "show_panel":
            linter_panel = "output.SublimeLinter"
            if args.get('panel') == linter_panel:
                if (is_building(window) or
                        window.active_panel() == "output.exec"):
                    # rewrite the command to a non-existing one to cancel it
                    return ("do_nothing")
