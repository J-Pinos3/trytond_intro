# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, Workflow, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.tools import grouped_slice, reduce_ids
from trytond.transaction import Transaction


class RevisionMixin:
    __slots__ = ()
    revision = fields.Integer(
        "Revision", required=True, readonly=True,
        states={
            'invisible': Eval('revision', 0) == 0,
            })

    @classmethod
    def default_revision(cls):
        return 0

    @property
    def full_number(self):
        number = super().full_number
        if number is not None and self.revision:
            number += '/%d' % self.revision
        return number

    @classmethod
    def copy(cls, records, default=None):
        default = default.copy() if default is not None else {}
        default.setdefault('revision', cls.default_revision())
        return super().copy(records, default=default)

    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(cls, records):
        cursor = Transaction().connection.cursor()
        table = cls.__table__()

        # Use SQL and before super to avoid two history entries
        for sub_records in grouped_slice(records):
            cursor.execute(*table.update(
                    [table.revision],
                    [table.revision + 1],
                    where=reduce_ids(table.id, sub_records)))

        super().draft(records)


class Sale(RevisionMixin, metaclass=PoolMeta):
    __name__ = 'sale.sale'
    _history = True


class Line(metaclass=PoolMeta):
    __name__ = 'sale.line'
    _history = True


class LineTax(metaclass=PoolMeta):
    __name__ = 'sale.line-account.tax'
    _history = True


class Subscription(RevisionMixin, metaclass=PoolMeta):
    __name__ = 'sale.subscription'
    _history = True


class SubscriptionLine(metaclass=PoolMeta):
    __name__ = 'sale.subscription.line'
    _history = True
