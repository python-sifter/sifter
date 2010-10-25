import extensions

# commands
import rules.if_cmd
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

extensions.register('builtin')
