import os

SITE_TITLE = 'Ghosts of Massachusetts'
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
                else:
                    props[key].append(value)
    return props


def get_font():
    return "<link href='https://fonts.googleapis.com/css?family=Lora' rel='stylesheet' type='text/css'>\n"

def get_css(up):
    if up:
        return '<link rel="stylesheet" href="../css/base.css">\n'
    else:
        return '<link rel="stylesheet" href="./css/base.css">\n'

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
    return '</li>\n'

def open_footer():
    return '<footer>'

def close_footer():
    return '</footer>'

def get_head():
    return "<head>\n\
    <!-- Global site tag (gtag.js) - Google Analytics -->\n\
    <script async src='https://www.googletagmanager.com/gtag/js?id=UA-124818630-1'></script>\n\
    <script>\n\
    window.dataLayer = window.dataLayer || [];\n\
    function gtag(){dataLayer.push(arguments);}\n\
    gtag('js', new Date());\n\
    gtag('config', 'UA-124818630-1');\n\
    </script>\n\
    <title>" + SITE_TITLE + "</title>\n\
    </head>\n"

def write_index(all_props):
    with open("../index.html", 'w') as f:
        f.write(get_css(False))
        f.write(get_font())

        f.write(get_head())

        f.write(open_body())

        # Site title
        f.write(open_h(1))
        f.write(open_a('./'))
        f.write(SITE_TITLE)
        f.write(close_a())
        f.write(close_h(1))

        f.write(p("The below map tracks ghosts and haunted places in Massachusetts. Click on a location for more information. To report a ghost sighting in MA, <a href='https://www.twitter.com/matt_fister'>please contact me.</a>\n"))

        f.write(open_h(2))
        f.write("Map of Ghost Sightings")
        f.write(close_h(2))

        f.write('<iframe src="https://www.google.com/maps/d/embed?mid=1L5_PGGQLr11iCM2b7mwZQD-8mSiTj7Jy&hl=en" width="640" height="480"></iframe>\n')

        f.write(close_body())

        f.write(open_h(2))
        f.write("All Ghost Sightings")
        f.write(close_h(2))


        cities_to_props_list = {}
        for props in all_props:
            city = props.get('city')[0]
            if not cities_to_props_list.get(city):
                cities_to_props_list[city] = []
                cities_to_props_list[city].append(props)
            else:
                cities_to_props_list[city].append(props)

        f.write(open_ul())
        for city, props_list in cities_to_props_list.items():
            f.write(open_li())
            f.write(city+'\n')
            f.write(close_li())

            f.write(open_ul())

            for props in props_list:
                f.write(open_li())
                f.write(open_a('./l/'+props.get('fname')))
                f.write(props.get('title')[0])
                f.write(close_a())
                f.write(close_li())
            f.write(close_ul())
        f.write(close_ul())


def write_page(f_name, props):
    f_name = f_name.replace('properties', 'html')
    with open("../l/" + f_name, 'w') as f:
        f.write(get_css(True))
        f.write(get_font())

        f.write(get_head())

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

        print(source_props)
        for source in source_props:
            f.write(open_li())
            f.write(open_a(source.split('>')[1]))
            f.write((source.split('>'))[0])
            f.write(close_a())
            f.write(close_li())

        f.write(close_ul())

        f.write(open_footer())
        f.write(open_a(".."))
        f.write("Back to " + SITE_TITLE)
        f.write(close_a())
        f.write(close_footer())

        f.write(close_body())

if __name__ == '__main__':
    all_props = []
    for name in os.listdir("../input"):
        props = read_properties_file("../input/" + name)
        props['fname'] = name.replace('.properties', '.html')
        all_props.append(props);
        write_page(name, props)

    write_index(all_props)
