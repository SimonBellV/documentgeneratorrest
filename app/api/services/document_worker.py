from io import BytesIO
from datetime import datetime
from pytz import timezone
from relatorio.templates.opendocument import Template


ALLOWED_EXTENSIONS = ['odt', 'ods', 'odp']


class DocumentWorkerException(Exception): pass


class DocumentWorker:
    def __init__(self, template, ext: str, data: dict):
        self.template = template
        self.ext = ext
        self.data = data

    def render_template(self):
        """Returns document like BytesIO object and new filename"""
        template_name, template_ext = self.template.filename.split('.', 1)
        if self.ext == template_ext and self.ext in ALLOWED_EXTENSIONS:
            basic = Template(source=self.template, filepath='')
            basic_generated = basic.generate(json=self.data).render()
            document = BytesIO(basic_generated.getvalue())
            time_zone = timezone('Europe/Moscow')
            now_date = datetime.strftime(datetime.now(time_zone), "%d%m%Y:%H%M%S")
            filename = f'{template_name}{now_date}.{self.ext}'
            return document, filename
        else:
            raise DocumentWorkerException('Incorrect extension!')
