import sublime
import sublime_plugin

from Default import comment

# inherit everything from the toggle_comment command but prevent it from
# removing block comments
class ToggleLineCommentCommand(comment.ToggleCommentCommand):
	def remove_block_comment(self, view, edit, comment_data, region):
		return False
