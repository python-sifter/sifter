import sieve.commands.discard
import sieve.commands.fileinto
import sieve.commands.if_cmd
import sieve.commands.keep
import sieve.commands.redirect
import sieve.commands.require
import sieve.commands.stop

import sieve.tests.address
import sieve.tests.allof
import sieve.tests.anyof
import sieve.tests.exists
import sieve.tests.header
import sieve.tests.false
import sieve.tests.not_test
import sieve.tests.size
import sieve.tests.true

import sieve.comparators.ascii_casemap
import sieve.comparators.octet

import sieve.handler
sieve.handler.register('extension', 'fileinto', True)
sieve.handler.register('extension', 'comparator-i;ascii-casemap', True)
sieve.handler.register('extension', 'comparator-i;octet', True)
