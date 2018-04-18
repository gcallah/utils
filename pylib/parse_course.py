
MIN_FLDS = 2
MAX_FLDS = 5
SEP = '^'
INDENT_LEVEL = 0
TITLE = 1
URL = 2
SHORT_TITLE = 3
GLYPHICON = 4

class CourseItem:
    def __init__(self, flds):
        self.ind_level = int(flds[INDENT_LEVEL])
        self.title = flds[TITLE]
        self.url = flds[URL]
        self.short_title = flds[SHORT_TITLE]
        self.glyphicon = flds[GLYPHICON]

    # for debug
    def print_item(self):
        print_list = [self.ind_level, self.title, self.url,
                      self.short_title, self.glyphicon]
        print(print_list)

class InputError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message

def parse_course(file):
    with open(file) as f:
        lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        lines = [line.rstrip('\r') for line in lines] # for windows machines

        course_items = []
        for line in lines:
            # skip empty lines
            if not line.strip():
                continue
            # split with separator
            flds = line.split(SEP)
            for i in range(0, len(flds)):
                if not flds[i].strip():
                    flds[i] = None
            for i in range(len(flds), MAX_FLDS):
                flds.append(None)

            num_flds = len(flds)
            # make sure # of fields is in valid range
            if num_flds < MIN_FLDS or num_flds > MAX_FLDS:
                raise InputError(line,
                                 "You have %d fields. Your input \
should have between %d and %d fields \
separated by %s."
                                 % (num_flds, MIN_FLDS, MAX_FLDS, SEP))
            else:
                # make sure indent level is present and has a valid value
                if flds[INDENT_LEVEL] is None:
                    raise InputError(line, "Indent level is required.")
                else:
                    ind_level = int(flds[INDENT_LEVEL])
                    if ind_level < 0:
                        raise InputError(line,
                                         "Indent level is " + str(ind_level) +
                                         "; it must be a non-negative integer.")
                # make sure title is present
                if flds[TITLE] is None:
                    raise InputError(line, "Title is required.")
                # create a CourseItem object
                course_items.append(CourseItem(flds))
    return course_items
