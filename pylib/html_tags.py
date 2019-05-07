# a collection of functions for outputting HTML

INDENT1 = "    "
INDENT2 = INDENT1 + INDENT1
INDENT4 = INDENT2 + INDENT2


def include_tag(file_nm, django=True):
    return "{% include '" + file_nm + "' %}"


def par(text=None, indent=INDENT4):
    s = indent + '<p>\n'
    if text is not None:
        s += text + '\n'
    s += indent + '</p>\n'
    return s


def code(text=None):
    s = '<code>\n'
    if text is not None:
        s += text + '\n'
    s += '</code>\n'
    return s


def code_par(text=None, indent=INDENT4):
    s = indent + '<pre>\n'
    s += indent + code(text)
    s += indent + '</pre>\n'
    return s


def link(target, text):
    return '<a href="' + target + '">' + text + '</a>'


def figure(src="", caption=None, indent=INDENT4):
    # by default we get an empty figure tag
    s = indent + '<figure>\n'
    s += indent + INDENT1 + '<img src="' + src + '" width="40%">\n'
    s += indent + INDENT1 + '<figcaption>\n'
    if caption is not None:
        s += indent + INDENT1 + caption + "\n"
    s += indent + INDENT1 + '</figcaption>\n'
    s += indent + '</figure>\n'
    return s


def details(sumtext, level=1, indent=INDENT4, inc_par=False, inc_fig=False,
            inner_details=None):
    indent += INDENT1 * (level - 1)
    s = indent + '<details>\n'
    inner_indent = indent + INDENT1   # add one level indentation
    s += inner_indent + '<summary class="sum' + str(level) + '">\n'
    s += inner_indent + sumtext + "\n"
    s += inner_indent + '</summary>\n'
    if inc_fig:
        s += figure(indent=inner_indent)
    if inc_par:
        s += par(indent=inner_indent)
    if inner_details is not None:
        s += inner_details
    s += indent + '</details>\n'
    return s


def ulist(css_class=None, l=None, indent=INDENT4, level=1):  # noqa 741
    return html_list(css_class=css_class, l=l,  # noqa 741
                     indent=indent, level=level,
                     list_type='ul')


def olist(css_class=None, l=None, indent=INDENT4, level=1):  # noqa 741
    return html_list(css_class=css_class, l=l,  # noqa 741
                     indent=indent, level=level,
                     list_type='ol')


def html_list(css_class=None, l=None, indent=INDENT4, level=1,  # noqa 741
              list_type='ul'):
    # represents modules in homepage
    indent += INDENT1 * (level - 1)
    inner_indent = indent + INDENT1   # add one level indentation
    s = indent + "<" + list_type
    if css_class is not None:
        s += " class=\"" + css_class + "\""
    s += ">\n"
    for item in l:
        # l is the content within li tag (in this case, anchor tags)
        s += inner_indent
        s += "<li>\n"
        s += inner_indent
        s += item + "\n"
        s += inner_indent
        s += "</li>\n"
    s += indent + "</" + list_type + ">\n"
    return s


def image(indent=INDENT4, src="", alt="", other_attr=""):
    s = indent + "<img src=" + src + "alt=" + alt + other_attr + ">\n"
    return s


def head(indent=INDENT4, title="", cssFile=None):  # generate meta head
    s = "<head>\n"
    s += INDENT1 + "<title>\n\n"
    s += INDENT2 + title + "\n"
    s += INDENT1 + "</title>\n"
    if cssFile is not None:
        s += "<link rel='stylesheet' type='text/css' href="+cssFile+">\n"
    s += "</head>\n"
    return s


def sidebar_links(padding=INDENT1, topic=None, tot_submenus=0,
                  is_url=False):
    collapse_link = 'data-toggle="collapse" aria-expanded="false"'
    s = "%s<li>\n" % padding
    if is_url:
        s += '%s<a href="%s">\n' % (padding+INDENT1, topic.url)
    else:
        s += ('%s<a href="#Submenu%d" %s>\n'
              % (padding+INDENT1, tot_submenus, collapse_link))
    if topic.glyphicon:
        s += '%s<i class="glyphicon %s"></i>\n' % (padding+INDENT2,
                                                   topic.glyphicon)
    s += "%s%s\n" % (padding+INDENT2, topic.title)
    s += "%s</a>\n" % (padding+INDENT1)
    s += "%s</li>\n" % padding
    return s


def sidebar(title="", short_title="", menu_txt=""):  # for create_menu.py
    s = "<!-- Sidebar Holder -->\n"
    s += '<nav id=\"sidebar\">\n'
    s += '%s<div id=\"sidebarCollapse\">\n' % (INDENT1)
    s += '%s<div class=\"sidebar-header\">\n' % (INDENT2)
    s += '%s<h1>\n%s%s\n%s</h1>\n' % (INDENT2+INDENT1,
                                      INDENT4, title, INDENT2+INDENT1)
    s += '%s<strong>%s</strong>\n' % (INDENT2+INDENT1, short_title)
    s += '%s</div>\n%s</div>\n' % (INDENT2, INDENT1)
    s += menu_txt
    s += "</nav>\n"
    return s


def str_to_valid_id(key):
    if key.find('(') != -1:
        key = key[0:key.find('(')-1]
    return key.replace(" ", "_")
