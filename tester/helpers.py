class Command:

    """Command class for the CLI script"""

    def __init__(self, name, opts):
        """
        Command objects are loaded at run-time and injected into command parser.
        *name* denotes the name of the sub-command parser.
        *opts* must be an argparse-compatible dictionary of command options.
        """
        self.name = name
        self.opts = opts

    def run(self, *args, **kwargs):
        """Run the command"""
        raise NotImplementedError
