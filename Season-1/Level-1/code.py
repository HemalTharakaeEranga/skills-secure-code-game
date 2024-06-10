'''
Welcome to Secure Code Game Season-1/Level-1!

Follow the instructions below to get started:

1. tests.py is passing but code.py is vulnerable
2. Review the code. Can you spot the bug?
3. Fix the code but ensure that tests.py passes
4. Run hack.py and if passing then CONGRATS!
5. If stuck then read the hint
6. Compare your solution with solution.py
'''

from collections import namedtuple

Order = namedtuple('Order', 'id, items')
Item = namedtuple('Item', 'type, description, amount, quantity')

def validorder(order: Order):
    net = 0
    total_amount = 0
    max_amount_limit = 1e6  # The value 1e6 (which is equivalent to 1,000,000) is arbitrarily chosen as a high limit to prevent potential misuse,
                            # such as attempts to exploit the system with unrealistically large orders.

    for item in order.items:
        if item.type == 'payment':
            net += item.amount
        elif item.type == 'product':
            net -= item.amount * item.quantity
            total_amount += item.amount * item.quantity
        else:
            return "Invalid item type: %s" % item.type

        # Check if the total amount exceeds the limit
        if abs(total_amount) > max_amount_limit:
            return 'Total amount payable for an order exceeded'

    # Handle floating point precision issues by rounding
    net = round(net, 2)

    if net != 0:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
    else:
        # Check for potentially malicious transactions
        for item in order.items:
            if item.type == 'payment' and item.amount > max_amount_limit:
                return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net - total_amount)
        return "Order ID: %s - Full payment received!" % order.id

