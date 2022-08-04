import contextlib
from box import *

products = get_products_by_group(get_group_id("Pizza"))
for a in products:
    print(a.name)