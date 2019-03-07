import sublime
import sublime_plugin

class ContextMenuCursorCommand(sublime_plugin.TextCommand):
	def run(self, edit, event, *args):
		self.view.run_command("drag_select", { "event": event })
		self.view.run_command("context_menu", { "event": event })

	def want_event(self):
		return True
