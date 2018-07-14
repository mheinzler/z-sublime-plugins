import sublime
import sublime_plugin

from Default.comment import ToggleCommentCommand

# inherit everything from the toggle_comment command but prevent it from
# removing block comments
class ToggleLineCommentCommand(ToggleCommentCommand):
	def remove_block_comment(self, view, edit, comment_data, region):
		return False
