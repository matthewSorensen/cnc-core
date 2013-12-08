class GcodeEmitter:
    def __init__(self, stream, **config):
        default = dict(number_lines = False, 
                       integer_format = "{}", 
                       floating_format = "{0:.4f}", 
                       line_ending = '\n',
                       space = True,
                       program_number = None)
        default.update(config)
        self.configuration = default
        self.stream = stream
        self.state = dict()
        self.count = 1

    def __enter__(self):
        number = self.configuration['program_number']
        if not number is None:
            self.stream.write('O' + number + self.configuration['line_ending'])
        return self

    def __exit__(self, *ignore):
        self.emit('M30')
        self.emit('M05')

    def at(self,coords):
        self.state.update(dict(X = coords[0], y = coords[1], z = coords[2]))

    def emit(self, *args):
        s = self.stream
        if self.configuration['number_lines']:
            s.write('N')
            s.write(str(self.count))

            if self.configuration['space']:
                s.write(' ')

        for register in args:
            if register is None:
                continue
            if isinstance(register, str):
                s.write(register)

                if self.configuration['space']:
                    s.write(' ')
                continue

            axis, value = register
            formatter = self.configuration['integer_format' if isinstance(value, int) else 'floating_format']
            s.write(str(axis))
            s.write(formatter.format(value))

            if self.configuration['space']:
                s.write(' ')

        s.write(self.configuration['line_ending'])
        self.count += 1

    def different(self, axis, value):
        if value is not None and self.state.get(axis) != value:
            self.state[axis] = value
            return (axis, value)
        return None


    def go(self, x, y, z, feed = None, rapid = False, modal = False):
        nx = self.different('X', x)
        ny = self.different('Y', y)
        nz = self.different('Z', z)
        nf = self.different('F', feed)
            
        self.emit('G01' if not rapid else 'G00', nx, ny, nz, nf)
