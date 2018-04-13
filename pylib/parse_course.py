class CourseItem:
    def __init__(self, ind_level, title, url, short_title, glyphicon):
        self.ind_level = ind_level
        self.title = title
        self.url = url
        self.short_title = short_title
        self.glyphicon = glyphicon

    # for debug
    def print_item(self):
        print_list = [self.ind_level, self.title, self.url, self.short_title, self.glyphicon]
        print print_list

class InputError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message

def parse_course(file):
    separator = '^'
    min_length = 2
    max_length = 5
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
            splitted_line = line.split(separator)
            for i in range(0, len(splitted_line)):
                if not splitted_line[i].strip():
                    splitted_line[i] = None
            # make sure length of splitted line is in valid range
            if len(splitted_line) < min_length or len(splitted_line) > max_length:
                raise InputError(line, "Wrong number of arguments. Your input should have [%d, %d] arguments separated by %s." % (min_length, max_length, separator))
            else:
                # make sure indent level is present and has a valid value
                if splitted_line[0] is None:
                    raise InputError(line, "Indent level is required.")
                else:
                    try:
                        ind_level = int(splitted_line[0])
                        if ind_level < 0:
                            raise ValueError
                    except ValueError:
                        raise InputError(line, "Indent level must be a non-negative integer.")
                # make sure title is present
                if splitted_line[1] is None:
                    raise InputError(line, "Title is required.")
                # create a CourseItem object
                if len(splitted_line) == 3:
                    course_items.append(CourseItem(int(splitted_line[0]), splitted_line[1], splitted_line[2], None, None))
                elif len(splitted_line) == 4:
                    course_items.append(CourseItem(int(splitted_line[0]), splitted_line[1], splitted_line[2], splitted_line[3], None))
                else:
                    course_items.append(CourseItem(int(splitted_line[0]), splitted_line[1], splitted_line[2], splitted_line[3], splitted_line[4]))

    return course_items
