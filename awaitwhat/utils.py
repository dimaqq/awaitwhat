import re


def concise_stack_trace(trace):
    def clean(line):
        if line.startswith("Stack for "):
            return
        if '"<Sentinel>"' in line:
            return
        if re.search('File ".*/site-packages/.*"', line):
            line = re.sub('[^"]*/site-packages/', "", line)
        if re.search('File ".*/lib/python[0-9][.][0-9]/.*"', line):
            line = re.sub('[^"]*/lib/python[0-9][.][0-9]/', "", line)
        return line

    return '\n'.join(filter(None, (clean(line) for line in trace.split('\n'))))
