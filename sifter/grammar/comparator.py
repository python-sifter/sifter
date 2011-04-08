import sifter.comparator

__all__ = ('Comparator',)

# The official definition of comparators is in RFC 4790
class Comparator(object):

    @classmethod
    def register(cls):
        try:
            sifter.comparator.register(cls.COMPARATOR_ID, cls)
        except AttributeError:
            # this method should only be called on sub-classes that define an
            # identifier
            raise NotImplementedError

    @classmethod
    def sort_key(cls, s):
        return s

    # draft-ietf-sieve-regex-01: according to section 5, the :regex match type
    # is available to all comparators. furthermore, string normalization (aka
    # sort_key() above) is only applied to the string to be matched against,
    # not to the regular expression string.
    @classmethod
    def cmp_regex(cls, s, pattern, state):
        # section 4: must be used as an extension named 'regex'
        state.check_required_extension('regex', ':regex')
        # TODO: cache compiled pattern for more efficient execution across
        # multiple strings and messages
        # TODO: make sure the specified pattern is allowed by the standard
        # (which allows only extended regular expressions from IEEE Standard
        # 1003.2, 1992): 1) disallow python-specific features, along with word
        # boundaries and backreferences, 2) double-check that python supports
        # all ERE features.
        compiled_re = re.compile(pattern)
        return compiled_re.search(cls.sort_key(s))

