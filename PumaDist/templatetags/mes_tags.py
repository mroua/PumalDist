from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import json
from django.utils.safestring import mark_safe

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

def pretaxednumber(value):
    try:
        total = value/1.19
        return floate_redefined(total)
    except Exception:
        pass

def Date_redefined(value):
    c =str(value)
    a = str(c).split("-")

    return a[0]+a[1]+a[2]


def format_to_beautiful_dict(input_text):
    """
    Converts a string representation of a dictionary into a beautifully formatted string
    suitable for HTML display.
    """
    try:
        # Convert the string into a Python dictionary
        data_dict = eval(input_text)  # Replace eval with ast.literal_eval for safety
        formatted_dict = json.dumps(data_dict, indent=4, ensure_ascii=False)

        # Replace spaces and newlines with HTML-safe equivalents
        html_safe_dict = formatted_dict.replace("\n", "<br>").replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")

        # Mark as safe for rendering in templates
        return mark_safe(html_safe_dict)
    except Exception as e:
        return mark_safe(f"Error formatting dictionary: {str(e)}")

register.filter('floate_redefined', floate_redefined)
register.filter('taxednumber', taxednumber)
register.filter('pretaxednumber', taxednumber)
register.filter('Date_redefined', Date_redefined)
register.filter('format_to_beautiful_dict', format_to_beautiful_dict)