def run():
    if len(inp.split('/')) == 2:
        m, f = inp.split('/')
        obj_module = __import__(m)
        getf(obj_module, f)
    elif len(inp.split('/')) == 3:
        p, m, f = inp.split('/')
        obj_module = __import__(p + '.' + m, fromlist=True)
        getf(obj_module, f)


def getf(m, f):
    if hasattr(m, f):
        func = getattr(m, f)
        func()
    else:
        print('404')

if __name__ == "__main__":
    inp = input('url>')
    run()