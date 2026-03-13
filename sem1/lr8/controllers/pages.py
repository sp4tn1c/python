from jinja2 import Environment, PackageLoader


class PagesController:
    def __init__(self, template_dir: str = "templates"):
        self.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=True
        )

    def render_index(self, author_name, author_group, currencies):
        template = self.env.get_template("index.html")
        return template.render(
            myapp="CurrenciesListApp",
            navigation=[...],
            author_name=author_name,
            author_group=author_group,
            currencies=currencies
        )

    def render_currencies(self, currencies):
        template = self.env.get_template("currencies.html")
        return template.render(currencies=currencies)
