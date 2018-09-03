import os
from PIL import Image

SITE_TITLE = 'Ghosts of Massachusetts'
SITE_TITLE_WITH_LOGO = '<img src="./i/ghosts_of_ma_logo.svg" alt="Ghosts of MA Logo" style="height: 1.8em;"> ' + SITE_TITLE
SITE_TITLE_WITH_LOGO_UP = '<img src="../i/ghosts_of_ma_logo.svg" alt="Ghosts of MA Logo" style="height: 1.8em;"> ' + SITE_TITLE
UP_INDEX = '../index.html'
IMAGE_PATH = 'gimg'
THUMBNAIL_PATH = 'tgimg'


def gen_thumbs():
    base_width = 300
    for path in os.listdir('../' + IMAGE_PATH):
        img = Image.open('../' + IMAGE_PATH + '/'+path)
        w_percent = (base_width/float(img.size[0]))
        h_size = int((float(img.size[1])*float(w_percent)))
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
        img.save('../' + THUMBNAIL_PATH + '/' + path)


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


def open_tag(tag):
    return '<' + tag + '>\n'


def close_tag(tag):
    return '</' + tag + '>\n'


def get_tag(tag, content=''):
    return open_tag(tag) + content + close_tag(tag)


def get_open_a_tag(href):
    return '<a href='+href+'>'


def get_link(href, content):
    return get_open_a_tag(href) + content + close_tag('a')


def get_submit_link():
    return '<a href="https://goo.gl/forms/nGh9zTTwLzmrVdSd2">Submit Your Ghost Sighting</a>'


def get_place_img(img_name, place_name):
    thumb = img_name.replace('gimg', 'tgimg')
    return '<a href="' + img_name + '" target="blank"><img src="' + thumb + '" alt="'+place_name+'" class="thumbnail"/img></a>'


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
    <script async src='//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'></script>\n\
    <script>\n\
    (adsbygoogle = window.adsbygoogle || []).push({\n\
    google_ad_client: 'ca-pub-8138649344789982',\n\
    enable_page_level_ads: true\n\
    });\n\
    </script>\n\
    <title>" + SITE_TITLE + "</title>\n\
    </head>\n"


def write_line(f, line):
    f.write(line + '\n')


def write_index(all_props, name_to_images):
    with open("../index.html", 'w') as f:
        f.write(get_css(False))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link('./', SITE_TITLE_WITH_LOGO)))

        write_line(f, get_tag('p', "The below map tracks ghosts and haunted places in Massachusetts. Click on a location for more information. To report a ghost sighting in MA, <a href='https://goo.gl/forms/nGh9zTTwLzmrVdSd2'>click here.</a>"))

        write_line(f, get_tag('h2', 'Map of Ghost Sightings'))

        write_line(f, '<iframe src="https://www.google.com/maps/d/embed?mid=1L5_PGGQLr11iCM2b7mwZQD-8mSiTj7Jy&hl=en" width="640" height="480"></iframe>')

        write_line(f, get_tag('h2', 'All Ghost Sightings'))

        cities_to_props_list = {}
        for props in all_props:
            city = props.get('city')[0]
            if not cities_to_props_list.get(city):
                cities_to_props_list[city] = []
                cities_to_props_list[city].append(props)
            else:
                cities_to_props_list[city].append(props)

        write_line(f, open_tag('ul'))
        for city, props_list in sorted(cities_to_props_list.items()):
            write_line(f, get_tag('li', get_link('./c/'+city.lower()+'.html', city + ', MA')))

            write_line(f, open_tag('ul'))

            for props in props_list:
                write_line(f, get_tag('li', get_link('./g/'+props.get('fname'), props.get('title')[0])))
            write_line(f, close_tag('ul'))
            write_city(city, props_list)

        write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        f.write(get_submit_link())
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))


def write_page(f_name, props, images):
    f_name = f_name.replace('properties', 'html')
    with open("../g/" + f_name, 'w') as f:
        f.write(get_css(True))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link(UP_INDEX, SITE_TITLE_WITH_LOGO_UP)))

        # Page title
        write_line(f, get_tag('h2', get_link('./'+f_name, props.get('title')[0])))

        # Location
        write_line(f, get_link('../c/'+props.get('city')[0].lower()+'.html', props.get('city')[0] + ', MA'))

        # Overview
        write_line(f, get_tag('h3', 'Overview'))
        write_line(f, get_tag('p', props.get('overview')[0]))

        # Images
        if len(images) > 0:
            write_line(f, get_tag('h3', 'Images'))
            for image in images:
                write_line(f, get_place_img('../gimg/'+image, props.get('title')[0]))

        # Sources title
        write_line(f, get_tag('h3', 'Sources'))

        write_line(f, open_tag('ul'))

        source_props = props.get("source")

        for source in source_props:
            write_line(f, get_tag('li', get_link(source.split('>')[1], source.split('>')[0])))

        write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        f.write(get_submit_link())
        write_line(f, open_tag('br'))
        write_line(f, get_link('..', 'Back to ' + SITE_TITLE))
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))


def write_city(city_name, all_location_props):
    with open("../c/" + city_name.lower() + '.html', 'w') as f:
        f.write(get_css(True))
        f.write(get_font())

        f.write(get_head())

        write_line(f, open_tag('body'))

        # Site title
        write_line(f, get_tag('h1', get_link(UP_INDEX, SITE_TITLE_WITH_LOGO_UP)))

        # Page title
        write_line(f, get_tag('h2', get_link('./'+city_name.lower() + '.html', city_name.title() + ', MA')))

        write_line(f, get_tag('h3', "Reported Ghosts and Hauntings"))

        write_line(f, open_tag('ul'))

        for props in all_location_props:
            write_line(f, get_tag('li', get_link('../g/'+props.get('fname'), props.get('title')[0])))

        write_line(f, close_tag('ul'))

        write_line(f, open_tag('footer'))
        f.write(get_submit_link())
        write_line(f, open_tag('br'))
        write_line(f, get_link('..', 'Back to ' + SITE_TITLE))
        write_line(f, close_tag('footer'))

        write_line(f, close_tag('body'))

if __name__ == '__main__':
    gen_thumbs()
    all_props = []
    name_to_images = {}
    for name in os.listdir("../input"):
        name_to_images[name.replace('.properties', '')] = []
    for img_name in os.listdir('../gimg'):
        for place_name in name_to_images.keys():
            if img_name.find(place_name) >= 0:
                name_to_images[place_name].append(img_name)

    for name in os.listdir("../input"):
        props = read_properties_file("../input/" + name)
        props['fname'] = name.replace('.properties', '.html')
        all_props.append(props);
        write_page(name, props, name_to_images[name.replace('.properties', '')])

    write_index(all_props, name_to_images)
