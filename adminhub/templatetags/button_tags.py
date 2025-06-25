from django import template

register = template.Library()

@register.inclusion_tag('components/button.html')
def render_button(
    text,
    url=None,
    icon=None,
    variant="primary",
    disabled=False,
    loading=False,
    button_type="button",
    target="_self"
):
    css_class = get_variant_class(variant, disabled)
    return {
        'text': text,
        'url': url,
        'icon': icon,
        'css_class': css_class,
        'disabled': disabled,
        'loading': loading,
        'button_type': button_type,
        'target': target,
    }


def get_variant_class(variant, disabled):
    base_class = "inline-flex items-center gap-2 px-4 py-2 rounded-xl font-semibold transition duration-300"
    variants = {
        "primary": "bg-customPurple-700 text-white hover:bg-customPurple-900",
        "secondary": "bg-gray-200 text-gray-800 hover:bg-gray-300",
        "danger": "bg-red-600 text-white hover:bg-red-700",
        "cancel": "bg-yellow-500 text-white hover:bg-yellow-600",
        "disabled": "bg-gray-400 text-white cursor-not-allowed",
    }
    variant_class = variants.get(variant, variants["primary"])
    if disabled:
        variant_class += " opacity-60 cursor-not-allowed"
    return f"{base_class} {variant_class}"
