import sys
from engine import recognizer
from argparse import ArgumentParser

class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.
    """
    pass

class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """
    def __init__(self, *, missing_args_message=None, called_from_command_line=None, **kwargs):
        self.missing_args_message = missing_args_message
        self.called_from_command_line = called_from_command_line
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (self.missing_args_message and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)


class ManagementUtility:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        '''
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m django'
        self.settings_exception = None
        '''
        pass
    def fetch_command(self, subcommand):
        """
        Try to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            if os.environ.get('DJANGO_SETTINGS_MODULE'):
                # If `subcommand` is missing due to misconfigured settings, the
                # following line will retrigger an ImproperlyConfigured exception
                # (get_commands() swallows the original one) so the user is
                # informed about it.
                settings.INSTALLED_APPS
            else:
                sys.stderr.write("No Django settings specified.\n")
            possible_matches = get_close_matches(subcommand, commands)
            sys.stderr.write('Unknown command: %r' % subcommand)
            if possible_matches:
                sys.stderr.write('. Did you mean %s?' % possible_matches[0])
            sys.stderr.write("\nType '%s help' for usage.\n" % self.prog_name)
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass
    def execute(self):
        try:
            subcommand = sys.argv[1]
        except:
            subcommand = 'help'
        '''
        parser = CommandParser(usage='%(prog)s subcommand [options] [args]', add_help=False, allow_abbrev=False)
        parser.add_argument('--settings')
        parser.add_argument('--pythonpath')
        parser.add_argument('args', nargs='*')  # catch-all
        '''
        parser = ArgumentParser()
        #parser.add_argument('args', nargs='*') # catch-all
        parser.add_argument('-t', metavar='<gesturefile>', dest='gesturefile', help="Adds the gesture file to the list of gesture templates.") # adds the gesture file to the list of gesture template
        parser.add_argument('-r', action='store_const', const='clear', dest='clear', help="Clears the templates.") #clears the templates
        parser.add_argument('EVENTSTREAM', nargs='?', metavar='<eventstream>', help="Prints the name of gestures as they are recognized from the event stream.")
        #parser.add_argument
        #args = parser.parse_args(self.argv[1:])
        #options, args = parser.parse_known_args(self.argv[1:])
        self.parser = parser
        try:
            options, args = parser.parse_known_args(self.argv[1:])
        except:
            print("error solved?")
            pass  # Ignore any option errors at this point.

        # print(options.args)
        # print(options.template)
        # print(options.remove)
        # print(args)

        if subcommand == 'help' or self.argv[1:] in (['--help'], ['-h']):
            parser.print_help()
        else:
            if subcommand == '-r':
                print(options.clear)
                # Clears the template
            elif subcommand == '-t':
                print(options.gesturefile)
            else:
                # <eventstream>
                # Prints the name of gestures as they are recognized from the event stream
                print(options.EVENTSTREAM)
            #self.fetch_command(subcommand).run_from_argv(self.argv)

if __name__ == "__main__":
    #print(sys.argv[:])
    utility = ManagementUtility(sys.argv)
    utility.execute()
    print(recognizer.Point(1,2,1))
    pass