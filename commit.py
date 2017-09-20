import gitlab


def main():
    gl = gitlab.Gitlab.from_config('credentials', ['conf.cfg'])
    gl.auth()

main()