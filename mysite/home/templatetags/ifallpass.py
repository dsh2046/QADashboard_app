from django import template
register = template.Library()

@register.filter
def ifallpass(pass_num, total_num):
    try:
        if (pass_num/total_num)*100 < 100:
            return True  # red
        else:
            return False   # not red
    except (ValueError, ZeroDivisionError):
        return True
