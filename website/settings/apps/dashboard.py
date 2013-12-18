from django.utils.translation import ugettext_lazy as _

# to create a navigation menu:
#
# define a menu scheme in settings
#
# DASHBOARD_NAVIGATION = [
#     {
#         'label': _('Label with dropdown'),
#         'children': [
#             {
#                 'label': _('Sub label'),
#                 'url_name': 'namespace:sub-label',
#             },
#         ]
#     },
#     {
#         'label': _('Label with direct link'),
#         'url_name': 'namespace:link'
#     },
#
# ]
#
# in your templates {% load dashboard_tags %}
#
# you'll have the menu renderend with
#
# {% for item in nav_items %}
# <li class="{{ item.label }} dropdown"><a {% if item.is_heading %}href="#"{% else %}href="{{ item.url }}"{% endif %}><span class="icon-th-list"></span>{{ item.label }}</a>
# {% if item.has_children %}
#     <ul>
#         {% for subitem in item.children %}
#             <li><a href="{{ subitem.url }}">{{ subitem.label }}</a></li>
#         {% endfor %}
#     </ul>
# {% endif %}
# </li>
# {% endfor %}
#
#
# if you use a custom User object you can add a 'type' attribute to it
# (a CharField, you probably want to define some choices for it)
#
# then for every type of user a different menu will be rendered,
# for example if type == 'customer' name it DASHBOARD_NAVIGATION_CUSTOMER
#
