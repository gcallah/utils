
MAX_FLDS = 5  # type: int

SEP = '\t'  # type: str
COMMENT = "#"

INDENT1 = "    "

LEVEL = 0  # type: int
TITLE = 1  # type: int
URL = 2  # type: int
SHORT_TITLE = 3  # type: int
GLYPHICON = 4  # type: int
LINK_INSERT = 5  # type: int
DOC_TXT = 6  # type: int
HW_TXT = 7  # type: int
LINT_TXT = 8
MAX_FLD = LINT_TXT  # type: int

UNSET = -999999999  # topic level not yet set

try:
    from typing import List
except ImportError:
    print("Warning: could not import List or Any")


class IndentError(Exception):
    def __init__(self, level, line):
        self.msg = "Invalid jump to indent level %d at line %d" % (level, line)

    def __str__(self):
        return self.msg


class InputError(Exception):
    def __init__(self, value: str, msg: str)->None:
        self.value = value
        self.msg = msg

    def __str__(self):
        return self.msg


class Topic:
    def __init__(self, flds: List[str])->None:
        # make sure indent level is present and has a valid value
        if flds[LEVEL] is None:
            flds = ["" if fld is None else fld for fld in flds]
            raise InputError(SEP.join(flds), "Indent level is required.")
        else:
            try:
                # if flds[LEVEL] is not a number
                # this will raise a ValueError
                level = int(flds[LEVEL])
                if level < 0:
                    raise ValueError
            except ValueError:
                flds = ["" if fld is None else fld for fld in flds]
                raise InputError(SEP.join(flds),
                                 "Indent level is " + flds[LEVEL] +
                                 "; it must be a non-negative integer.")
        while len(flds) < MAX_FLD + 1:
            flds.append(None)

        # make sure title is present
        if flds[TITLE] is None:
            raise InputError(flds, "Title is required.")
        self.level = int(flds[LEVEL])
        self.title = flds[TITLE]
        self.url = flds[URL]
        self.short_title = flds[SHORT_TITLE]
        self.glyphicon = flds[GLYPHICON]
        self.link_insert = flds[LINK_INSERT]
        self.doc_txt = flds[DOC_TXT]
        self.hw_txt = flds[HW_TXT]
        self.lint_txt = flds[LINT_TXT]
        self.subtopics = None
        self.str_indent = self.level * INDENT1

    def set_subtopics(self, sub):
        self.subtopics = sub

    def to_string_just_me(self)->str:
        # when we don't want to recursively print the subtopics!
        s = self.str_indent
        s += str(self.level)
        s += "; " + self.title
        if self.url is not None:
            s += "; " + self.url
        if self.short_title is not None:
            s += "; " + self.short_title
        if self.glyphicon is not None:
            s += "; " + self.glyphicon
        return s

    def __str__(self)->str:
        s = self.to_string_just_me()
        s += "\n"
        if self.subtopics is not None:
            for t in self.subtopics:
                s += str(t)
        return s


class LevelState():
    def __init__(self, topic, topic_list):
        self.topic = topic
        self.topic_list = topic_list


def restore_state(stack, curr_tlist):
    level_state = stack.pop()
    upper_topic = level_state.topic
    upper_topic.set_subtopics(curr_tlist)
    return level_state.topic_list


def parse_site(file):
    title = None
    curr_level = UNSET
    with open(file) as f:
        lines = f.readlines()  # type: List[str]

    lines = [line.rstrip('\n') for line in lines]
    lines = [line.rstrip('\r') for line in lines]  # for windows machines

    stack = []
    curr_topic_list = []  # type: List[Any]
    prev_topic = None
    line_no = 0
    for line in lines:
        line_no += 1

        # skip empty lines and comments
        if not line.strip():
            continue
        if line.startswith(COMMENT):
            continue

        # split with separator
        flds = line.split(SEP)
        for i in range(0, len(flds)):
            if not flds[i].strip():
                flds[i] = None
        for i in range(len(flds), MAX_FLDS):
            flds.append(None)

        # create a Topic object
        if title is None:
            title = Topic(flds)
            continue
        else:
            t = Topic(flds)
        # and get it at the right level of nesting:
        if curr_level != UNSET:
            if t.level > curr_level:
                if t.level > curr_level + 1:
                    # can't skip indent levels going out:
                    raise IndentError(t.level, line_no)
                stack.append(LevelState(prev_topic, curr_topic_list))
                curr_topic_list = []
            elif t.level < curr_level:
                pops = curr_level - t.level
                # pop stack and connect list to popped item
                for i in range(0, pops):
                    curr_topic_list = restore_state(stack, curr_topic_list)
        curr_level = t.level

        curr_topic_list.append(t)
        prev_topic = t

    while len(stack) > 0:
        curr_topic_list = restore_state(stack, curr_topic_list)

    return (title, curr_topic_list)


def test_parse_site(file):
    try:
        (title, topics) = parse_site(file)
        print(title)
        for t in topics:
            print(t)
    except Exception as e:
        print(e)
