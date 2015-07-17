# -*- coding: utf-8 -*-
"""
    Forms for sources.
"""
from django.utils.translation import ugettext as _
from django import forms

from libs.ocl import OCLapi

from apps.core.views import _get_source_type_list, _get_locale_list


class SourceCreateForm(forms.Form):
    """
        source create form
    """
    required_css_class = 'required'

    short_name = forms.CharField(
        label=_('Source Short Name'),
        max_length=128,
        required=True,
        help_text=_('Your new source will live at: https://OpenConceptLab.org/[:OwnerType]/[:Owner]/sources/<span id="source-name">[:SourceName]</span>'),
        widget=forms.TextInput(attrs={'placeholder': "Short Name (e.g. ICD-10)"}))
    full_name = forms.CharField(
        label=_('Source Full Name'),
        max_length=256,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "Full Name (e.g. International Classification for Diseases v10)"}))
    website = forms.URLField(
        label=_('Website'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "Website (e.g. http://apps.who.int/classifications/icd10/)"}))
    source_type = forms.ChoiceField(
        choices=[(v, v) for v in _get_source_type_list()], label=_('Source Type'), required=False)
    public_access = forms.ChoiceField(
        label=_('Public Access'), required=False, initial='View',
        choices=(('View', 'View (default)'), ('Edit', 'Edit'), ('None', 'None')))
    supported_locales = forms.CharField(
        max_length=30,
        label=_('Supported Locales'),
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "e.g. en,fr,es"}))
    default_locale = forms.ChoiceField(
        label=_('Default Locale'),
        choices=[(d['code'], d['name']+' ('+d['code']+')') for d in _get_locale_list()],
        required=True)
    description = forms.CharField(
        max_length=512,
        label=_('Description'),
        required=False)
    external_id = forms.CharField(
        label=_('External ID'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': "e.g. UUID from external system"}))

    # TODO(paynejd@gmail.com): Is this mis-named or not used?
    def clean_concept_id(self):
        """ concept ID must be unique """
        concept_id = self.cleaned_data['concept_id']
        source = self.initial['source']
        request = self.initial['request']
        api = OCLapi(request, debug=True)
        result = api.get('orgs', source['owner'], 'sources', source['id'], 'concepts', concept_id)
        if result.status_code == 200:
            raise forms.ValidationError(_('This Concept ID is already used.'))
        return concept_id


class SourceEditForm(SourceCreateForm):

    def __init__(self, *args, **kwargs):
        """ Dirty trick to delete one field for edit form. django 1.6 lets you do this
            officially.
        """
        super(SourceEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('short_name')


class SourceVersionAddForm(forms.Form):
    """
        TODO: Removed. Not used. Now json/angular.
        Add a source version form
    """
    required_css_class = 'required'

    id = forms.CharField(max_length=30, label=_('ID'), required=True)
    description = forms.CharField(max_length=80, label=_('Description'), required=False)
    released = forms.BooleanField(required=False, label=_('Released'))
