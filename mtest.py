import re
ph1 = "+380968793084"
ph2 = "0968793084"
ph3 = "380131231313"
rule = re.compile(r'^\+?(38)?(0)\d{9,13}$')
if rule.search(ph1):
    print("Yeah")
else:
    print("Bad")
if rule.search(ph2):
    print("Yeah")
else:
    print("Bad")
if rule.search(ph3):
    print("Yeah")
else:
    print("Bad")