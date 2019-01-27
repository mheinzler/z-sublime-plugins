"""Focus the active view in the tabs of all windows."""

import sublime


try:
    first_run # noqa
except NameError:
    first_run = True


def plugin_loaded():
    """Focus the active view in the tabs of all windows."""
    global first_run
    if first_run:
        for window in sublime.windows():
            # save the active view and focus on it later to not change the
            # active group
            active_view = window.active_view()

            for group in range(window.num_groups()):
                # setting the index again forces the tabs to focus on the view
                view = window.active_view_in_group(group)
                window.set_view_index(view, *window.get_view_index(view))

            window.focus_view(active_view)

        first_run = False
