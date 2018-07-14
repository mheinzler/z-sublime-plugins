"""Improve viewing package resources."""

from PackageResourceViewer import package_resource_viewer


class PackageResourceViewerCommand(
        package_resource_viewer.PackageResourceViewerCommand):
    """Overwrite the insert_text method."""

    def insert_text(self, content, view):
        """Call the original method and detect the indentation."""
        super().insert_text(content, view)
        if not view.is_loading():
            view.run_command("detect_indentation")
