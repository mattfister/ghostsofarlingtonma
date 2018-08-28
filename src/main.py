import os

SITE_TITLE = 'Ghosts of Arlington, MA'
UP_INDEX = '../index.html'


def read_properties_file(path):
    props = {}
    with open(path, "rt") as f:
        for line in f:
            l = line.strip()
            if l:
                key_value = l.split("=")
                key = key_value[0].strip()
                value = "=".join(key_value[1:]).strip().strip('"')
                if not props.get(key):
                    props[key] = []
                    props[key].append(value)
    return props


def get_font():
    return "<link href='https://fonts.googleapis.com/css?family=Lora' rel='stylesheet' type='text/css'>\n"

def get_css():
    return '<link rel="stylesheet" href="../css/base.css">\n'


def open_body():
    return '<body>\n'


def close_body():
    return '</body>\n'


def open_h(n):
    return '<h' + str(n) + '>'


def close_h(n):
    return '</h' + str(n) + '>\n'


def open_a(href):
    return '<a href=' + href + '>'


def close_a():
    return '</a>'


def p(content):
    return '<p>'+content+'</p>\n'


def open_ul():
    return '<ul>'


def close_ul():
    return '</ul>\n'


def open_li():
    return '<li>'


def close_li():
    return '</li>'


def write_output(f_name, props):
    f_name = f_name.replace('properties', 'html')
    with open("../l/" + f_name, 'w') as f:
        f.write(get_css())
        f.write(get_font())

        f.write(open_body())

        # Site title
        f.write(open_h(1))
        f.write(open_a(UP_INDEX))
        f.write(SITE_TITLE)
        f.write(close_a())
        f.write(close_h(1))

        # Page title
        f.write(open_h(2))
        f.write(open_a('./'+f_name))
        f.write(props.get('title')[0])
        f.write(close_a())
        f.write(close_h(2))

        # Overview title
        f.write(open_h(3))
        f.write('Overview\n')
        f.write(close_h(3))

        f.write(p(props.get('overview')[0]))

        # Images title
        f.write(open_h(3))
        f.write('Images\n')
        f.write(close_h(3))

        # Sources title
        f.write(open_h(3))
        f.write('Sources\n')
        f.write(close_h(3))

        f.write(open_ul())

        source_props = props.get("source")
        for source in source_props:
            f.write(open_li())
            f.write(open_a(source.split('>')[1]))
            f.write((source.split('>'))[0])
            f.write(close_a())
            f.write(close_li())

        f.write(close_ul())

        f.write(close_body())


if __name__ == '__main__':
    for name in os.listdir("../input"):
        props = read_properties_file("../input/" + name)
        write_output(name, props)
