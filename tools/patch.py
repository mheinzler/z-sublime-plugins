"""Patch functions with a replacement."""

from collections import namedtuple

# a patch object containing information about a replaced function
Patch = namedtuple('Patch', [
    'cls',
    'name',
    'original',
    'replacement'
])

# the list of patched functions (do not overwrite the previous patches when the
# module is reloaded)
try:
    patches # noqa
except NameError:
    patches = {}


def patch(cls):
    """Patch a class method with a replacement function."""
    def decorator(replacement):
        # make sure there is an entry for the replacement's module
        module = replacement.__module__
        if module not in patches:
            patches[module] = []

        patch = None

        # wrap the replacement to also pass the patch object
        def replacement_wrapper(*args, **kwargs):
            return replacement(patch, *args, **kwargs)

        # store the information about this patch
        name = replacement.__name__
        patch = Patch(
            cls=cls,
            name=name,
            original=getattr(cls, name),
            replacement=replacement_wrapper
        )

        patches[module].append(patch)

        # return the function unchanged
        return replacement

    return decorator


def apply_patches(module):
    """Apply all patches registered by a module."""
    if module in patches:
        for patch in patches[module]:
            setattr(patch.cls, patch.name, patch.replacement)


def restore_patches(module):
    """Restore all original functions patched by a module."""
    if module in patches:
        for patch in patches[module]:
            setattr(patch.cls, patch.name, patch.original)

        # remove all patches for this module
        del patches[module]
