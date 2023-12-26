from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader("lib.jinja.templates"),
    autoescape=True,
    enable_async=True,
)
