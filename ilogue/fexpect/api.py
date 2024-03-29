import fabric.api
from ilogue.fexpect.internals import wrapExpectations, wrapExpectationsLocal, ExpectationContext


def expect(promptexpr, response, exitAfter=-1):
    if not exitAfter == -1:
        return [(promptexpr, response, exitAfter)]
    return [(promptexpr, response)]

# Use inside an expect(), like:  `expect('>>>', controlchar('D'))`
def controlchar(char):
    char = char.lower()
    a = ord(char)
    if a >= 97 and a <= 122:
        a = a - ord('a') + 1
        return chr(a)
    d = {'@': 0, '`': 0,
        '[': 27, '{': 27,
        '\\': 28, '|': 28,
        ']': 29, '}': 29,
        '^': 30, '~': 30,
        '_': 31,
        '?': 127}
    if char not in d:
        return 0
    return chr(d[char])

def expecting(e):
    return ExpectationContext(e)

def run(cmd, **kwargs):
    #run wrapper 
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd, script, remote_pexpect = wrapExpectations(cmd)
    ret = fabric.api.run(cmd, **kwargs)
    fabric.api.run('rm %s' % script)
    fabric.api.sudo('rm %s' % remote_pexpect)
    return ret

def sudo(cmd, **kwargs):
    #sudo wrapper
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd, script, remote_pexpect = wrapExpectations(cmd)
    ret = fabric.api.sudo(cmd, **kwargs)
    fabric.api.sudo('rm %s' % script)
    fabric.api.sudo('rm %s' % remote_pexpect)
    return ret

def local(cmd, **kwargs):
    #local wrapper
    if 'expectations' in fabric.state.env and \
        len(fabric.state.env.expectations) > 0:
        cmd, script = wrapExpectationsLocal(cmd)
    ret = fabric.api.local(cmd, **kwargs)
    fabric.api.local('rm %s' % script)
    return ret


