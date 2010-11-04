# commands
import sieve.rules.discard
import sieve.rules.fileinto
import sieve.rules.if_cmd
import sieve.rules.keep
import sieve.rules.redirect
import sieve.rules.require
import sieve.rules.stop

# tests
import sieve.rules.allof
import sieve.rules.anyof
import sieve.rules.exists
import sieve.rules.false
import sieve.rules.not_test
import sieve.rules.size
import sieve.rules.true

import sieve.handler
sieve.handler.register('extension', 'fileinto')
