"""Improve the exec build command."""

import html
import re
import subprocess
import sys
import textwrap

import sublime

import Default.exec

from .tools.patch import *

stylesheet_template = '''
<style>
    #arrow {
        border-top: 0.4rem solid transparent;
        margin-left: {column}px;
        width: 0;
        height: 0;
    }
    .error-arrow {
        border-left: 0.5rem solid color(var(--redish)
            blend(var(--background) 30%));
    }
    .warning-arrow {
        border-left: 0.5rem solid color(var(--orangish)
            blend(var(--background) 30%));
    }
    .note-arrow {
        border-left: 0.5rem solid color(var(--bluish)
            blend(var(--background) 30%));
    }
    #container {
        padding: 0.4rem 0.7rem 0.4rem 0.7rem;
        margin: 0 0 0.2rem;
        border-radius: 0 0.2rem 0.2rem 0.2rem;
    }
    .note {
        background-color: color(var(--bluish) blend(var(--background) 30%));
    }
    #message {
        padding-right: 0.7rem;
    }
    a {
        color: inherit;
        text-decoration: inherit;
    }
</style>
'''

html_template = '''
{stylesheet}
<body>
    <div id="arrow" class="{type}-arrow"></div>
    <div id="container" class="{type}">
        <a href=hide>
            <span id="message">{text}</span>
        </a>
    </div>
</body>
'''


def generate_stylesheet(self, view, line, column, text):
    """Generate a stylesheet for a phantom."""

    # GCC returns the column without taking tabs into account. We need to
    # correct the column to include the tabs as Sublime Text does.

    # get the text in line up to column
    pt = view.text_point(line - 1, column - 1)
    column_str = view.substr(view.line(pt))[:column - 1]

    # expand all tabs
    tab_size = view.settings().get("tab_size")
    column_str = column_str.expandtabs(tab_size)

    # the real column is now the same as the length of the string
    column = len(column_str)
    stylesheet = stylesheet_template.replace("{column}",
                                             str(column * view.em_width()))

    return stylesheet


def generate_html(self, view, line, column, text):
    """Generate the HTML for a phantom."""

    # detect the type of the message
    match = re.match("^(error|warning|note)", text)
    type = match.group(1) if match else "error"

    # combine the stylesheet with the HTML content
    stylesheet = generate_stylesheet(self, view, line, column, text)
    html = html_template.format(stylesheet=stylesheet,
                                type=type,
                                text=text)

    return html


def generate_phantom(self, view, line, column, text):
    """Generate a phantom."""
    html = generate_html(self, view, line, column, text)

    # create a phantom that is shown below the line
    pt = view.text_point(line - 1, column - 1)
    phantom = sublime.Phantom(sublime.Region(pt, view.line(pt).b),
                              html,
                              sublime.LAYOUT_BLOCK,
                              on_navigate=self.on_phantom_navigate)

    return phantom


def _get_windows_process_children(pid):
    # run a wmic command to find the children of this process
    wmic_command = [
        'wmic',
        'process',
        'where',
        '(ParentProcessId=%d)' % pid,
        'get',
        'Caption,ProcessId'
    ]

    children = subprocess.check_output(wmic_command,
                                       shell=True,
                                       universal_newlines=True)

    # split the text output into process names and ids
    children = [p.split() for p in children.splitlines() if p]

    # skip the first row of headers
    return children[1:]


def _kill_msys2_process(windows_pid):
    # call kill.exe because it allows to specify Windows process IDs
    kill_command = [
        'bash',
        '-c',
        'kill.exe -W %d' % windows_pid
    ]

    subprocess.check_output(kill_command, shell=True)


@patch(Default.exec.AsyncProcess)
def kill(patch, self):
    """Implement our own killing mechanism on certain platforms."""

    # when running the build process using MSYS2 and bash we can't just kill the
    # cmd.exe because this would leave the child processes running
    if sys.platform == "win32":
        if not self.killed:
            # search for a process id of bash
            cmd_children = _get_windows_process_children(self.proc.pid)
            bash_pid = -1
            for caption, pid in cmd_children:
                if caption.startswith("bash"):
                    bash_pid = int(pid)

            # if a bash instance was found, search for its children and kill
            # them from within MSYS2 to correctly terminate all children
            if bash_pid != -1:
                bash_children = _get_windows_process_children(bash_pid)
                for caption, pid in bash_children:
                    _kill_msys2_process(int(pid))

    # call the original method
    patch.original(self)


@patch(Default.exec.ExecCommand)
def on_finished(patch, self, proc):
    """Use a longer timeout to wait for the process to exit."""
    sublime.set_timeout(lambda: self.finish(proc), 1)


@patch(Default.exec.ExecCommand)
def update_phantoms(patch, self):
    """Create our own phantoms."""
    for file, errs in self.errs_by_file.items():
        view = self.window.find_open_file(file)
        if view:
            buffer_id = view.buffer_id()
            if buffer_id not in self.phantom_sets_by_buffer:
                phantom_set = sublime.PhantomSet(view, "exec")
                self.phantom_sets_by_buffer[buffer_id] = phantom_set
            else:
                phantom_set = self.phantom_sets_by_buffer[buffer_id]

            # use the rulers as an approximate maximum width
            rulers = view.settings().get("rulers", [])
            width = int((rulers[0] or 80) * 1.25)

            phantoms = []
            for line, column, text in errs:
                if not text:
                    continue

                # break the text up into shorter lines to make reading easier
                lines = textwrap.wrap(text, width)
                lines = [html.escape(l, quote=False) for l in lines]
                text = "<br>".join(lines)

                phantoms.append(generate_phantom(self, view,
                                                 line, column, text))

            phantom_set.update(phantoms)


def plugin_loaded():
    """Apply patches."""
    apply_patches(__name__)


def plugin_unloaded():
    """Restore patches."""
    restore_patches(__name__)
