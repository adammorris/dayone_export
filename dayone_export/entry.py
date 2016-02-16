# Copyright (c) 2012, Nathan Grigg
# All rights reserved.
# BSD License
import plistlib
import pytz
from dayone_export import compat


class PlistError(Exception):
    pass


class Entry(object):
    """Parse a single journal entry.

    :raises: IOError, KeyError

    Acts like a read-only dictionary.
    The keys are as defined in the plist file by the Day One App, with
    minor exceptions:

    - What Day One calls "Entry Text", we call "Text".
    - The "Location", "Weather", "Creator", and "Music" dictionaries are
      flattened, so that their subkeys are accessible as keys of the main
      dictionary.
    - The "Photo" key is added and contains the path to attached photo.
    - The "Date" key is added and contains the localized date.

    Note that the "Creation Date" contains a naive date (that is, with no
    attached time zone) corresponding to the UTC time.
    """

    def __init__(self, filename):
        try:
            self.data = plistlib.readPlist(filename)
        except AttributeError as err:  # See #25.
            if str(err) == "'NoneType' object has no attribute 'groupdict'":
                raise PlistError(
                    'Unable to parse {} due to invalid ISO 8601 date.'
                    .format(filename))
            raise
        except IOError as err:
            raise PlistError('Unable to read {}: {}'.format(filename, repr(err)))

        # Required fields
        if "Creation Date" not in self.data:
            raise KeyError("Creation Date")

        # aliases and flattening
        self.data['Text'] = self.data.pop('Entry Text', "")
        for key in ['Location', 'Weather', 'Music', 'Creator']:
            if key in self.data:
                new_keys = ((k, v) for k, v in self.data[key].items()
                            if k not in self.data) # prevent overwrite
                self.data.update(new_keys)

    def set_photo(self, filename):
        """Set the filename of the photo"""
        self.data['Photo'] = filename

    def set_localized_date(self, timezone):
        """Set the localized date (the "Date" key)"""
        try:
            tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            tz = pytz.utc

        localized_utc = pytz.utc.localize(self["Creation Date"])
        self.data["Date"] = localized_utc.astimezone(tz)

    def set_time_zone(self, timezone):
        """Set the time zone"""
        self.data["Time Zone"] = timezone

    def place(self, levels=4, ignore=None):
        """Format entry's location as string, with places separated by commas.

        :param levels: levels of specificity to include
        :type levels: list of int
        :keyword ignore: locations to ignore
        :type ignore: string or list of strings

        The *levels* parameter should be a list of integers corresponding to
        the following levels of specificity defined by Day One.

        - 0: Place Name
        - 1: Locality (e.g. city)
        - 2: Administrative Area (e.g. state)
        - 3: Country

        Alternately, *levels* can be an integer *n* to specify the *n*
        smallest levels.

        The keyword argument *ignore* directs the method to ignore one
        or more place names. For example, you may want to ignore
        your home country so that only foreign countries are shown.
        """

        # deal with the arguments
        if isinstance(levels, int):
            levels = list(range(levels))
        if ignore is None:
            ignore = []
        if isinstance(ignore, compat.string_types):
            ignore = [ignore]

        # make sure there is a location set
        if not 'Location' in self:
            return "" # fail silently

        # mix up the order
        order = ['Place Name', 'Locality', 'Administrative Area', 'Country']
        try:
            order_keys = [order[n] for n in levels]
        except TypeError:
            raise TypeError("'levels' argument must be an integer or list")

        # extract keys
        names = (self[key] for key in order_keys if key in self)

        # filter
        try:
            names = [name for name in names if len(name) and name not in ignore]
        except TypeError:
            raise TypeError("'ignore' argument must be a string or list")

        return ", ".join(names)

    def weather(self, temperature_type):
        if not 'Weather' in self:
            return "" # fail silently

        if temperature_type.lower() == 'celsius' or temperature_type.lower() == 'c':
            temperature = self.data['Celsius']
        else:
            temperature = self.data['Fahrenheit']

        weather = "{0}&deg; {1}".format(temperature, self.data['Description'])
        return weather

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        """List all keys."""
        return list(self.data.keys())

    def __repr__(self):
        return "<Entry at {0}>".format(self['Creation Date'])
