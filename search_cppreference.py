"""Search cppreference.com."""

import sublime
import sublime_plugin
import webbrowser
import re
import urllib


SEARCH_URL = "http://en.cppreference.com/mwiki/index.php"
SEARCH_URL += "?title=Special:Search&search={search_term}"


class SearchCppreferenceCommand(sublime_plugin.TextCommand):
    """Search cppreference.com."""

    def run(self, edit):
        """Run the command."""

        # expand selection to current word
        sel = self.view.sel()[0]
        start = sel.a
        end = sel.b

        while (start > 0 and
               self.view.classify(start) & sublime.CLASS_LINE_START == 0 and
               re.match("[\w:]", self.view.substr(start - 1))):
            start -= 1

        view_size = self.view.size()
        while (end < view_size and
               self.view.classify(end) & sublime.CLASS_LINE_END == 0 and
               re.match("[\w:]", self.view.substr(end))):
            end += 1

        # extract the word from the view
        search = self.view.substr(sublime.Region(start, end))

        # escape the search term and open the URL in a browser
        search = urllib.parse.quote_plus(search)
        webbrowser.open_new_tab(SEARCH_URL.format(search_term=search))
