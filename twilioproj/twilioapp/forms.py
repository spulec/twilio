from django.forms import ModelForm
from twilioapp.models import *

class TwilioNumberForm(ModelForm):
    class Meta:
        model = TwilioNumber

class ResponseForm(ModelForm):
    class Meta:
        model = Response

class TwilioWordForm(ModelForm):
    class Meta:
        exclude = ('response', 'final_type')

class GatherForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Gather

class SayForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Say

class PlayForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Play

class PauseForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Pause

class RedirectForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Redirect

class HangupForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Hangup

class SmsForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Sms

class DialForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Dial

class NumberForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Number

class ConferenceForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Conference

class RecordForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Record

class RejectForm(TwilioWordForm):
    class Meta(TwilioWordForm.Meta):
        model = Reject

class FormUtilities:
    @staticmethod
    def get_form(verb):
        class_name = verb.cast().__class__.__name__
        form_map = {
            'Gather': GatherForm,
            'Say': SayForm,
            'Play': PlayForm,
            'Pause': PauseForm,
            'Redirect': RedirectForm,
            'Hangup': HangupForm,
            'Number': NumberForm,
            'Sms': SmsForm,
            'Conference': ConferenceForm,
            'Dial': DialForm,
            'Record': RecordForm,
            'Reject': RejectForm,
        }
        form = form_map.get(class_name)(instance=verb)
        return form


