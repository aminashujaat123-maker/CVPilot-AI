import os


def allowed_file(filename, allowed_extensions):
    """Check if the uploaded file has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def get_file_extension(filename):
    """Return the lowercase extension of a filename without the dot."""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""