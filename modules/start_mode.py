def check_start_mode(argv):
    parameter = {}
    keys = ['path', 'password', 'row', 'col']
    if len(argv) > 1:
        index = -1
        del argv[0]
        for i in argv:
            index += 1
            parameter[keys[index]] = i
    return parameter
