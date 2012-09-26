#!/usr/bin/env python
#
# Command line interface to dayone_export
#
# For help, run `dayone_export --help`

from . import dayone_export
import times
import jinja2
import argparse
import codecs
import os
import sys


def parse_args(args=None):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
      description="Export Day One entries using a Jinja template",
      usage="%(prog)s [--output FILE] [opts] journal",
      epilog="""If the Day One package has photos, you may need to copy
        the "photos" folder from the package into the same directory
        as the output file.""")
    parser.add_argument('journal', help="path to Day One journal package")
    parser.add_argument('--output', metavar="FILE",
      help="file to write (default print to stdout)")
    parser.add_argument('--format', metavar="FMT",
      help="output format (default guess from output file extension)")
    parser.add_argument('--template', metavar="NAME",
      help="name or file of template to use")
    parser.add_argument('--template-dir', metavar="DIR",
      help='location of templates (default ~/.dayone_export)')
    parser.add_argument('--tags',
      help='export entries with these comma-separated tags. Tag \'any\' has a special meaning.')
    parser.add_argument('--after', metavar='DATE',
      help='export entries published after this date')
    parser.add_argument('--reverse', action="store_true",
      help="display in reverse chronological order")
    return parser.parse_args(args)


# command line interface
def run(args=None):
    args = parse_args(args)

    # determine output format
    if args.format is None:
        args.format = os.path.splitext(args.output)[1][1:] if args.output \
                      else 'html'
    if args.format.lower() in ['md', 'markdown', 'mdown', 'mkdn']:
        args.format = 'md'

    # Check journal files exist
    args.journal = os.path.expanduser(args.journal)
    if not os.path.exists(args.journal):
        return "File not found: " + args.journal
    if not os.path.exists(os.path.join(args.journal, 'entries')):
        return "Not a valid Day One package: " + args.journal

    tags = args.tags
    if tags is not None:
        if tags != 'any':
            tags = [tag.strip() for tag in tags.split(',')]

    try:
        output = dayone_export(args.journal, template=args.template,
          reverse=args.reverse, tags=tags, after=args.after,
          format=args.format, template_dir=args.template_dir)
    except jinja2.TemplateNotFound as err:
        return "Template not found: {0}".format(err)

    if args.output:
        try:
            with codecs.open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
        except IOError as err:
            return str(err)
    else:
        sys.stdout.write(output.encode('utf-8') + "\n")


if __name__ == "__main__":
    sys.exit(run())
