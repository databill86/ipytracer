from jinja2 import Template
from ipywidgets.widgets.domwidget import DOMWidget
import time
from IPython.core.display import (
    display,
    HTML,
    Javascript
)
from IPython.display import clear_output
from uuid import uuid4
from .model import ListElement


class Tracer(DOMWidget):
    """basic Tracer object it show list as table"""
    def __init__(self, data, delay=0.25, **kwargs):
        super(Tracer, self).__init__(**kwargs)
        self.data = data
        self.delay = delay
        self._id = uuid4()

    def __len__(self):
        return len(self.data)

    def __add__(self, value):
        # event when list or Tracer object added
        self.data += value
        self._update_html()

    def __setitem__(self, key, value):
        print("setitem")
        self.data[key] = value
        tpl_js = '''
                $('#{id}-{key}').addClass('set-item');
                $('#{id}-{key}').html({value});
                '''
        js = tpl_js.format(id=self._id, key=key, value=value)
        display(Javascript(js))

        time.sleep(self.delay)
        tpl_js = '''
                $('#{id}-{key}').removeClass('set-item');
                '''
        js = tpl_js.format(id=self._id, key=key)
        display(Javascript(js))

    def __getitem__(self, key):
        tpl_js = '''
                $('#{id}-{key}').addClass('get-item');
                '''
        js = tpl_js.format(id=self._id, key=key)
        display(Javascript(js))

        time.sleep(self.delay)
        tpl_js = '''
                $('#{id}-{key}').removeClass('get-item');
                '''
        js = tpl_js.format(id=self._id, key=key)
        display(Javascript(js))
        self._update_html()

        return self.data[key]

    def __delitem__(self, key):
        del self.data[key]
        self._update_html()

    '''
    Python List data type method
    '''
    def append(self, value):
        self.data.append(value)
        self._update_html()

    def extend(self, L):
        self.data.extend(L)
        self._update_html()

    def insert(self, i, x):
        self.data.insert(i, x)
        self._update_html()
        display(Javascript(
            '''
            '''
        ))

    def remove(self, x):
        self.data.remove(x)
        self._update_html()

    def pop(self, i):
        self.data.pop(i)
        self._update_html()

    def index(self, x):
        return self.data.index(x)

    def count(self, x):
        return self.data.count(x)

    def sort(self, key=None, reverse=False):
        self.data.sort(key=key, reverse=reverse)
        self._update_html()

    def reverse(self):
        self.data.reverse()
        self._update_html()

    # end

    def _update_html(self):
        """
        update display html
        """
        clear_output(wait=True)
        display(HTML('''
        <style>
            .set-item {
                background-color: blue;
                color: white;
            }
            .get-item {
                background-color: red;
                color: white;
            }
        </style>
        '''))

        tpl = Template('''
        <table id="{{id}}">
            <tr>
            {% for cell in data %}
                <td id="{{ id }}-{{ loop.index0 }}">{{ cell }}</td>
            {% endfor %}
            </tr>
        <table>
        ''')

        html = tpl.render(
            id=self._id,
            data=self.data
        )

        display(HTML(html))

    def _ipython_display_(self, **kwargs):
        self._update_html()

    def show(self):
        self._update_html()


class ChartTracer(object):
    def __init__(self, data, delay=0.25):
        self.data = data
        self.delay = delay
        self.is_show = False

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        if self.is_show:
            html = '<div style="display: table;">'
            for _index, _value in enumerate(self.data):
                if _index == key:
                    html += '<div style="display: table-cell; vertical-align: bottom;"><div style="width: 20px; height: %s0px; background: blue">%s</div></div>' % (
                    str(value), str(value))
                else:
                    html += '<div style="display: table-cell; vertical-align: bottom;"><div style="width: 20px; height: %s0px; background: gray">%s</div></div>' % (
                    str(_value), str(_value))
            html += '</div>'
            display(HTML(html))
            time.sleep(self.delay)
            clear_output(wait=True)
        self.data[key] = value

    def __getitem__(self, key):
        if self.is_show:
            html = '<div style="display: table">'
            for _index, _value in enumerate(self.data):
                if _index == key:
                    html += '<div style="display: table-cell; vertical-align: bottom;"><div style="width: 20px; height: %s0px; background: red">%s</div></div>' % (
                    str(_value), str(_value))
                else:
                    html += '<div style="display: table-cell; vertical-align: bottom;"><div style="width: 20px; height: %s0px; background: gray">%s</div></div>' % (
                    str(_value), str(_value))
            html += '</div>'
            display(HTML(html))
            time.sleep(self.delay)
            clear_output(wait=True)
        return self.data[key]

    def set_show(self, is_show, delay=0.25):
        self.is_show = is_show
        self.delay = delay


class Tracer2DList(object):
    data = []

    def __init__(self, data):
        self.base_id = id(data)
        self.data = [ListElement(_val, self.base_id, _i) for _i, _val in enumerate(data)]
        self.is_show = False
        self.delay = 0.25

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        if self.is_show:
            html = '<table>'
            for _i, _value in enumerate(self.data):
                html += '<tr>'
                for _index in range(len(_value)):
                    html += '<td id="%d-%d-%d">%s</td>' % (self.base_id, _i, _index, str(_value.get_val(_index)))
                html += '</tr>'
            html += '</table>'
            display(HTML(html))
            time.sleep(self.delay)
        return self.data[item]

    def set_show(self, is_show, delay=0.25):
        self.is_show = is_show
        self.delay = delay