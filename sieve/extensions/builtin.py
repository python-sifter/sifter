import extensions

# commands
import rules.discard
import rules.fileinto
import rules.if_cmd
import rules.keep
import rules.redirect
import rules.require
import rules.stop

# tests
import rules.allof
import rules.anyof
import rules.exists
import rules.false
import rules.not_test
import rules.size
import rules.true

extensions.register('fileinto')
