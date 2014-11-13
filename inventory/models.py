"""Models for the inventory app.

The following tables will be contained within:
- Inventory
- Orders
- Invoicing

"""

from django.db import models

"""
Table: Invoicing
Fields:
Invoice #
Date created
Date submitted
Saved invoices
"""

"""
Table: Orders
Fields:
Order type (orthotics, shoes, etc)
Client (or their dependent)
order date
arrival date
dispensing date
Reports: to place orders for orthotics, compression stockings, shoes
-Orders for ortho, comp and shoes will not be ordered on the spot so we will to have a report the let’s us know when we have placed the order and when we actually submitted the order.
"""

"""
* This is an important table, i want to know as much as i can about the reports you want to generate to make sure we ahve all the fields we will need in here.
"""

"""
* using shoes as a first example
Table: Inventory
Fields:
Brand
Name of shoe
Style
SKU
size
Color
Price
notes/details
"""


"""
Reports:
1)how much shoes that is in inventory
- separate by Brands, style, sku
2)how much money is invested in inventory
-separate by brands, style, sku
3)Best sellers
4)best sizes sellers
5)size curve
6) low inventory notifications
- sent by notification can be sent by email
"""
