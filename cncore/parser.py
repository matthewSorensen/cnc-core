import re

class ParseError(Exception):
    def __init__(self,number,line, error):
        self.number = number
        self.line = line
        self.error = error
        
    def position(self):
        return number, error

    def friendly_message(self):
        return 'Parse error in line number ' + str(self.number) + ' at "' + self.error[:10] + '"'

code = re.compile('\s*([A-Z])((-|\+)?[0-9]+\.?[0-9]*)')
comment = re.compile('\(.*\)')
end_comment = re.compile('([^)]*\))')

def parse(lines):
    # Context - line number, and overall line
    line_number = 0
    orignal = None
    # Are we currently in a multi-line comment?
    multiline = False

    for line in lines:
        # Save context so that we can print nice friendly
        # error messages when things go wrong
        line_number += 1
        original = line
        # If we're in a multiline comment, see if it closes.
        # If not, throw the line away, otherwise parse the rest.
        if multiline:
            match = end_comment.match(line)
            if match:
                line = line[len(match.group(0)):]
                multiline = False
        while not multiline and line != '':
            # First, check if we have a valid gcode statement
            match = code.match(line)
            if match:
                line = line[len(match.group(0)):]
                yield match.group(1), match.group(2)
            else:
                line = line.lstrip()
                # In the case of whitespace, we've rememoved everything
                # otherwise, we have a line ending comment
                if line == '' or line[0] == ';':
                    yield '\n'
                    break
                # In the case of a single line parenthetical comment
                # remove it and continue parsing
                match = comment.match(line)
                if match:
                    line = line[len(match.group(0)):]
                    continue
                # Otherwise, we have an incomplete comment
                elif line[0] == '(':
                    multiline = True
                    break
                # Otherwise, just a total parse error - indicate context
                # as best as possible
                raise ParseError(line_number,original,line)
