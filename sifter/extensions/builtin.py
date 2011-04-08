import sifter.commands.discard
import sifter.commands.fileinto
import sifter.commands.if_cmd
import sifter.commands.keep
import sifter.commands.redirect
import sifter.commands.require
import sifter.commands.stop

import sifter.tests.address
import sifter.tests.allof
import sifter.tests.anyof
import sifter.tests.exists
import sifter.tests.header
import sifter.tests.false
import sifter.tests.not_test
import sifter.tests.size
import sifter.tests.true

import sifter.comparators.ascii_casemap
import sifter.comparators.octet

import sifter.extension
map(sifter.extension.register,
    ('fileinto',
     'comparator-i;ascii-casemap',
     'comparator-i;octet',
     ))
