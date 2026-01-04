from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Apply a CSS class to a single field."""
    return field.as_widget(attrs={**field.field.widget.attrs, "class": css_class})

@register.filter(name='add_form_control')
def add_form_control(bound_field):
    """Automatically add 'form-control' to all input fields."""
    widget = bound_field.field.widget
    classes = widget.attrs.get('class', '')
    if 'form-control' not in classes:
        classes += ' form-control'
    widget.attrs['class'] = classes.strip()
    return bound_field
