from subprocess import Popen, PIPE


def mer(query):
    command1 = "bash"
    directory = "OutServices/MER"
    command2 = "get_entities.sh"
    text = str('nicotinic acid')
    lexicon = "lexicon"

    sreturn = ''

    with Popen([command1, command2, text, lexicon], cwd='OutServices/MER', stdout=PIPE, bufsize=1, universal_newlines=True) as process:
        for line in process.stdout:  # b'\n', b'\r\n', b'\r' are recognized as newline
            sreturn += line


    return sreturn