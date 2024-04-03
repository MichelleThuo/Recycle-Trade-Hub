from django import template

register=template.Library()
@register.filter(name='rating_stars')
def rating_stars(rating):
    full_stars = int(rating)
    half_stars = float(rating) % 1 >= 0.5
    empty_stars = 5 - full_stars - half_stars
    return f"★"*full_stars + f"☆"*half_stars +f"☆"*empty_stars
