import os
import re
from datetime import datetime

import sublime
import sublime_plugin

# configuration
build_timeout = 300 # seconds
build_check_interval = 100 # milliseconds

# like the chain command but waits for build commands to finish before running
# the next
class BuildChainCommand(sublime_plugin.WindowCommand):
    # the messages to be searched for to detect the current build status
    error_regex = re.compile(r"^\[Finished in \d+\.\d+s with exit code .*\]$",
                             re.MULTILINE)
    success_regex = re.compile(r"^\[Finished in \d+\.\d+s\]$", re.MULTILINE)

    # id of the currently run command
    current_id = 0

    def run(self, commands):
        # increase the id of this run
        self.id = BuildChainCommand.current_id + 1
        BuildChainCommand.current_id = self.id

        # start with the first command
        if commands:
            self.commands = iter(commands)
            self.command = next(self.commands)

            self.start = datetime.now()
            self.building = False
            self.handle_command()

    def handle_command(self):
        # stop if this is not the latest run
        if self.id != BuildChainCommand.current_id:
            return

        # stop if the plugin is running for too long
        if (datetime.now() - self.start).total_seconds() > build_timeout:
            return

        # wait for any currently running build command
        if self.building:
            build_finished = self.build_finished()
            if build_finished: # build was successful
                self.building = False
            else:
                if build_finished is None: # still running (or unknown)
                    # check again later
                    sublime.set_timeout_async(lambda: self.handle_command(),
                                              build_check_interval)
                    return
                elif build_finished is False: # finished with errors
                    # do not continue to run any other commands
                    return

        # prepare for the build command
        if self.command[0] == "build":
            self.prepare_build()
            self.building = True

        # do it
        self.run_command()

    def run_command(self):
        # run the command
        name = self.command[0]
        args = self.command[1] if len(self.command) > 1 else None
        self.window.run_command(name, args)

        # handle the next command
        self.command = next(self.commands, None)
        if self.command:
            self.handle_command()

    def prepare_build(self):
        # XXX: maybe the build panel needs to be cleared of any previous
        #       "finished" messages here to prevent build_finished from
        #       detecting the messages of a previous build
        # self.window.destroy_output_panel("exec")

        pass

    def build_finished(self):
        # find the build output
        exec_view = self.window.find_output_panel("exec")
        if exec_view:
            text = exec_view.substr(sublime.Region(0, exec_view.size()))

            # look for the error string
            if re.search(BuildChainCommand.error_regex, text):
                return False

            # look for the success string
            if re.search(BuildChainCommand.success_regex, text):
                return True

        # still running (or unknown)
        return None
