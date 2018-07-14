import sublime
import sublime_plugin

# like the chain command but implemented as a TextCommand which merges all
# changes into a single undo entry
class TextChainCommand(sublime_plugin.TextCommand):
	def run(self, edit, commands):
		for command in commands:
			command_name = command[0]
			command_args = command[1:]
			self.view.run_command(command_name, *command_args)
