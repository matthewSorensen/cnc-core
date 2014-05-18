import re

class ParseError(Exception):
    def __init__(self,number,line,rest):
        print number, line
        pass

code = re.compile('\s*([A-Z])(-?[0-9]+\.?[0-9]*)')
comment = re.compile('\(.*\)')
end_comment = re.compile('([^)]*\))')

def parse(lines):
    line_number = 0
    multiline = False
    for line in lines:
        line_number += 1
        if multiline:
            match = end_comment.match(line)
            if match:
                line = line[len(match.group(0)):]
                multiline = False
        while not multiline and line != '':
            match = code.match(line)
            if match:
                line = line[len(match.group(0)):]
                yield match.group(1), match.group(2)
            else:
                # We have something weird at the end 
                line = line.lstrip()
                # In the case of whitespace, we've rememoved everything
                # otherwise, we have a line ending comment
                if line == '' or line[0] == ';':
                    yield '\n'
                    break
                # In the case of a single line parenthetical comment
                # remove it
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
                raise ParseError(line_number,line,lines)
