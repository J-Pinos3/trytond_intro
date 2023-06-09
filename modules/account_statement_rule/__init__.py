# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool

from . import account

__all__ = ['register']


def register():
    Pool.register(
        account.Statement,
        account.StatementOrigin,
        account.StatementRule,
        account.StatementRuleInformation,
        account.StatementRuleLine,
        module='account_statement_rule', type_='model')
    Pool.register(
        module='account_statement_rule', type_='wizard')
    Pool.register(
        module='account_statement_rule', type_='report')
