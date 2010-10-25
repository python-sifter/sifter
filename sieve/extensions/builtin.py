import rules.base

# commands
import rules.if_cmd
import rules.require

# tests
import rules.exists
import rules.false
import rules.not_test
import rules.size
import rules.true

rules.base.register_sieve_extension("builtin")
