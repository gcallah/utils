
MAX_FLDS = 5 # type: int

SEP = '^' # type: str
COMMENT = "#"

INDENT1 = "    "

LEVEL = 0 # type: int
TITLE = 1 # type: int
URL = 2 # type: int
SHORT_TITLE = 3 # type: int
GLYPHICON = 4 # type: int

UNSET = -999999999  # topic level not yet set

try:
    from typing import List,Any
except ImportError:
    print("WARNING!")

class Topic:
    def __init__(self, flds:List[str])->None:
        # make sure indent level is present and has a valid value
        if flds[LEVEL] is None:
            flds = ["" if fld is None else fld for fld in flds]
            raise InputError(SEP.join(flds), "Indent level is required.")
        else:
            try:
                level = int(flds[LEVEL]) # if flds[LEVEL] is not a number, say 'a' or '!', this will raise a ValueError
                if level < 0:
                    raise ValueError
            except ValueError:
                flds = ["" if fld is None else fld for fld in flds]
                raise InputError(SEP.join(flds),
                                 "Indent level is " + flds[LEVEL] +
                                 "; it must be a non-negative integer.")
        # make sure title is present
        if flds[TITLE] is None:
            raise InputError(flds, "Title is required.")
        self.level = int(flds[LEVEL])
        self.title = flds[TITLE]
        self.url = flds[URL]
        self.short_title = flds[SHORT_TITLE]
        self.glyphicon = flds[GLYPHICON]
        self.subtopics = None
        self.str_indent = self.level * INDENT1

    def set_subtopics(self, sub):
        self.subtopics = sub

    def __str__(self)->object:
        s = self.str_indent
        s += str(self.level)
        s += "; " + self.title
        if self.url is not None:
            s += "; " + self.url
        if self.short_title is not None:
            s += "; " + self.short_title
        if self.glyphicon is not None:
            s += "; " + self.glyphicon
        s += "\n"
        if self.subtopics is not None:
            for t in self.subtopics:
                s += str(t)
        return s


class InputError(Exception):
    def __init__(self, value:str, message:str)->None:
        self.value = value
        self.message = message

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
    curr_level = UNSET
    with open(file) as f:
        lines = f.readlines() # type: List[str]

    lines = [line.rstrip('\n') for line in lines]
    lines = [line.rstrip('\r') for line in lines] # for windows machines

    stack = []
    curr_topic_list = [] # type: List[Any]
    prev_topic = None
    for line in lines:
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
        t = Topic(flds)
        # and get it at the right level of nesting:
        if curr_level != UNSET:
            if t.level > curr_level:
                stack.append(LevelState(prev_topic, curr_topic_list))
                curr_topic_list = []
            elif t.level < curr_level:
                # pop stack and connect list to popped item
                curr_topic_list = restore_state(stack, curr_topic_list)
        curr_level = t.level
        
        curr_topic_list.append(t)
        prev_topic = t

    while len(stack) > 0:
        curr_topic_list = restore_state(stack, curr_topic_list)

    return curr_topic_list


def test_parse_site(file):
    topics = parse_site(file)
    for t in topics:
        print(t)
