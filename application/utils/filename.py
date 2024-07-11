from uuid import uuid4


def maker(root: str, instance, filename: str, keys: list | None = None):
    filename, extension = filename.split(".")

    sub_directories = [getattr(instance, field) for field in keys or []]
    return f"{root}/{'/'.join(sub_directories)}/{uuid4()}.{extension}"
