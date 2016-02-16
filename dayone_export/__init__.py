#! /usr/bin/env python
#
# Copyright (c) 2012, Nathan Grigg
# All rights reserved.
# BSD License

"""Export Day One journal entries using a Jinja template."""

from operator import itemgetter
from functools import partial
from . import compat
from . import filters
from .db import parse_db_journal
from .entry import Entry
from .version import VERSION
import jinja2
import os
import pytz
from collections import defaultdict
from datetime import datetime


def parse_journal(foldername):
    """Return a list of Entry objects, sorted by date"""

    journal = dict()
    for filename in os.listdir(os.path.join(foldername, 'entries')):
        if os.path.splitext(filename)[1] == '.doentry':
            try:
                entry = Entry(os.path.join(foldername, 'entries', filename))
            except KeyError as err:
                pass

            journal[entry['UUID']] = entry

    if len(journal) == 0:
        raise Exception("No journal entries found in " + foldername)

    try:
        photos = os.listdir(os.path.join(foldername, 'photos'))
    except OSError:
        pass
    else:
        for filename in photos:
            base = os.path.splitext(filename)[0]
            try:
                journal[base].set_photo(os.path.join('photos', filename))
            except KeyError:
                # ignore items in the photos folder with no corresponding entry
                pass

    # make it a list and sort
    journal = list(journal.values())
    journal.sort(key=itemgetter('Creation Date'))

    # add timezone info
    newest_tz = 'utc'
    for entry in reversed(journal):
        if "Time Zone" in entry:
            newest_tz = entry["Time Zone"]
            break

    tz = newest_tz
    for entry in reversed(journal):
        if "Time Zone" in entry:
            tz = entry["Time Zone"]
        else:
            entry.set_time_zone(tz)

        entry.set_localized_date(tz)

    return journal


def _determine_inheritance(template, template_dir, format):
    """Determines where to look for template based on user options"""

    # explicit path to template => only load that template
    if template is not None:
        path, base = os.path.split(template)
        if path:
            return jinja2.FileSystemLoader(path), base

    # template directory given => look there only
    if template_dir is not None:
        loader = jinja2.FileSystemLoader(template_dir)

    else:
        template_dir = os.path.expanduser('~/.dayone_export')
        # template is given => look in current directory, then defaults
        if template is not None:
            template_search_path = ['.', template_dir]
        # no template is given => don't look in current directory
        else:
            template_search_path = [template_dir]

        loader = jinja2.ChoiceLoader([
          jinja2.FileSystemLoader(template_search_path),
          jinja2.PackageLoader('dayone_export')
        ])

    # determine template if none is given
    if template is None:
        template = ("default." + format) if format else "default.html"

    return loader, template

def _filter_by_tag(journal, tags):
    """filter by list of tags. tags='any' allows any entry with some tag"""
    if tags == 'any':
        tag_filter = lambda item: 'Tags' in item
    else:
        tag_filter = lambda item: 'Tags' in item and set(item['Tags']).intersection(set(tags))

    return filter(tag_filter, journal)

def _exclude_tags(journal, tags):
    """remain only entries without specified tags"""

    remain_filter = lambda item: 'Tags' not in item or not set(item['Tags']).intersection(set(tags))

    return filter(remain_filter, journal)

def _filter_by_date(journal, after, before):
    """return a list of entries after date

    :param before: A naive datetime representing a UTC time.
    :param after: A naive datetime representing a UTC time
    """
    if after is None and before is None:
        return journal
    return [item for item in journal
            if (after is None or item['Creation Date'] >= after) and
               (before is None or item['Creation Date'] < before)]

def _convert_to_utc(date, default_tz):
    """Convert date to UTC, using default_tz if no time zone is set."""
    if date is None:
        return date
    if date.tzinfo is None:
        date = default_tz.localize(date)
    date.astimezone(pytz.utc)
    # strip timezone info
    return date.replace(tzinfo=None)


def dayone_export(dayone_folder, template=None, reverse=False, tags=None,
    exclude=None, before=None, after=None, format=None, template_dir=None, autobold=False,
    nl2br=False, filename_template=""):
    """Render a template using entries from a Day One journal.

    :param dayone_folder: Name of Day One folder; generally ends in ``.dayone``.
    :type dayone_folder: string
    :param reverse: If true, the entries are formatted in reverse chronological
                    order.
    :type reverse: bool
    :param tags: Only include entries with the given tags.
                 This paramater can also be the literal string ``any``,
                 in which case only entries with tags are included.
                 Tags are interpreted as words at the end of an entry
                 beginning with ``#``.
    :type tags: list of strings
    :param exclude: Exclude all entries with given tags.
    :type exclude: list of strings
    :param before: Only include entries on before the given date.
    :type before: naive datetime
    :param after: Only include entries on or after the given date.
    :type after: naive datetime
    :param format: The file extension of the default template to use.
    :type format: string
    :param template: Template file name.
                     The program looks for the template first
                     in the  current directory, then the template directory.
    :type template: string
    :param template_dir: Directory containing templates.
                         If not given, the program looks in
                         ``~/.dayone_export`` followed by the
                         dayone_export package.
    :type template_dir: string
    :param autobold: Specifies that the first line of each post should be
                     a heading
    :type autobold: bool
    :param nl2br:  Specifies that new lines should be translated in to <br>s
    :type nl2br: bool
    :type filename_template: string
    :param filename_template: An eventual filename, which can include strftime formatting codes.
                Each time the result of formatting an entry's timestamp with this changes,
                a new result will be returned.
    :returns: Iterator yielding (filename, filled_in_template) as strings on each iteration.
    """

    # figure out which template to use
    loader, template = _determine_inheritance(template, template_dir, format)

    # custom latex template syntax
    custom_syntax = {}
    if os.path.splitext(template)[1] == ".tex":
        custom_syntax = {'block_start_string': r'\CMD{',
                         'block_end_string': '}',
                         'variable_start_string': r'\VAR{',
                         'variable_end_string': '}',
                         }
    # define jinja environment
    env = jinja2.Environment(loader=loader, trim_blocks=True, **custom_syntax)

    # filters
    env.filters['markdown'] = filters.markdown_filter(autobold=autobold)
    env.filters['format'] = filters.format
    env.filters['escape_tex'] = filters.escape_tex
    env.filters['imgbase64'] = partial(filters.imgbase64,
      dayone_folder=dayone_folder)


    # load template
    template = env.get_template(template)

    # parse journal
    # TODO - Add parameter for setting sqlit_url instead of dayone_folder
    # j = parse_journal(dayone_folder)
    j = parse_db_journal(dayone_folder)

    # filter and manipulate based on options
    default_tz = j[-1]["Date"].tzinfo
    after = _convert_to_utc(after, default_tz)
    before = _convert_to_utc(before, default_tz)
    j = _filter_by_date(j, after=after, before=before)
    if tags is not None:
        j = _filter_by_tag(j, tags)
    if exclude is not None:
        j = _exclude_tags(j, exclude)
    if reverse:
        j.reverse()


    # Split into groups, possibly of length one
    # Generate a new output for each time the 'filename_template' changes.
    # Yield the resulting filename_template plus the output.
    # If the filename_template is an empty string (the default), we'll get
    # an empty grouper plus the rendering of the full list of entries.
    # This may throw an exception if the template is malformed.
    # The traceback is helpful, so I'm letting it through
    # it might be nice to clean up the error message, someday

    output_groups = defaultdict(list)
    for e in j:
        output_groups[e['Date'].strftime(filename_template)].append(e)

    today = datetime.today()
    for k in output_groups:
        yield k, template.render(journal=output_groups[k], today=today)
