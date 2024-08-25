from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

# @register.filter
def floate_redefined(value):
    try:
        c ='%.2f' %float(value)
        a = str(c).split(".")
        b = intcomma(int(a[0])).replace(',', ' ')
        d = str(b)+'.'+str(a[1])
        return d
    except Exception:
        pass

def taxednumber(value):
    try:
        total = value+value*0.19
        return floate_redefined(total)
    except Exception:
        pass


def Date_redefined(value):
    c =str(value)
    a = str(c).split("-")

    return a[0]+a[1]+a[2]


register.filter('floate_redefined', floate_redefined)
register.filter('taxednumber', taxednumber)
register.filter('Date_redefined', Date_redefined)