from django.conf import settings
from django.template.base import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.test import SimpleTestCase

from .test_extends import inheritance_templates
from .utils import render, setup


class ExceptionsTests(SimpleTestCase):

    @setup({'exception01': "{% extends 'nonexistent' %}"})
    def test_exception01(self):
        """
        Raise exception for invalid template name
        """
        with self.assertRaises(TemplateDoesNotExist):
            render('exception01')

    @setup({'exception02': '{% extends nonexistent %}'})
    def test_exception02(self):
        """
        Raise exception for invalid variable template name
        """
        if settings.TEMPLATE_STRING_IF_INVALID:
            with self.assertRaises(TemplateDoesNotExist):
                render('exception02')
        else:
            with self.assertRaises(TemplateSyntaxError):
                render('exception02')

    @setup(
        {'exception03': "{% extends 'inheritance01' %}"
                        "{% block first %}2{% endblock %}{% extends 'inheritance16' %}"},
        inheritance_templates,
    )
    def test_exception03(self):
        """
        Raise exception for extra {% extends %} tags
        """
        with self.assertRaises(TemplateSyntaxError):
            get_template('exception03')

    @setup(
        {'exception04': "{% extends 'inheritance17' %}{% block first %}{% echo 400 %}5678{% endblock %}"},
        inheritance_templates,
    )
    def test_exception04(self):
        """
        Raise exception for custom tags used in child with {% load %} tag in parent, not in child
        """
        with self.assertRaises(TemplateSyntaxError):
            get_template('exception04')

    @setup({'exception05': '{% block first %}{{ block.super }}{% endblock %}'})
    def test_exception05(self):
        """
        Raise exception for block.super used in base template
        """
        with self.assertRaises(TemplateSyntaxError):
            render('exception05')
