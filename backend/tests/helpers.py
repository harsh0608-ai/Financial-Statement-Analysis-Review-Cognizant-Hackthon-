class Item:
    """Lightweight stand-in for a FinancialLineItem ORM row, so rule
    checks (which only ever read attributes off the object) can be
    unit-tested without a real database."""

    def __init__(
        self, label, value, year, statement_type,
        page_number=1, table_id=1, order_index=0, is_total=False, group_id=0,
    ):
        self.label = label
        self.value = value
        self.year = year
        self.statement_type = statement_type
        self.page_number = page_number
        self.table_id = table_id
        self.order_index = order_index
        self.is_total = is_total
        self.group_id = group_id
