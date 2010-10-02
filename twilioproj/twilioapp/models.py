from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import twilio

METHOD_CHOICES = (
    ('G', 'GET'),
    ('P', 'POST'),
)

class Response(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def to_xml(self):
        response = twilio.Response()
        verbs = TwilioVerb.objects.filter(response=self).order_by('order')

        for verb in verbs:
            verb.cast().add_to_response(response)

        return response

class TwilioNumber(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    response = models.ForeignKey(Response)

class TwilioWord(models.Model):
    order = models.PositiveIntegerField()
    final_type = models.ForeignKey(ContentType)

    def add_to_response(self, response):
        raise Exception('Method not implemented')

    def save(self, *args, **kwargs):
        if not self.id:
            self.final_type = ContentType.objects.get_for_model(type(self))
            super(TwilioWord, self).save(*args, **kwargs)

    def cast(self):
        return self.final_type.get_object_for_this_type(id=self.id)

    class Meta:
        abstract = True

class TwilioVerb(TwilioWord):
    response = models.ForeignKey(Response)
    
class TwilioNoun(TwilioWord):
    pass

class Gather(TwilioVerb):
    method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    url = models.URLField(verify_exists=False, max_length=200)
    timeout = models.PositiveIntegerField(default=5)
    finish_on_key = models.CharField(max_length=100)
    number_of_digits = models.PositiveIntegerField()

    def add_to_response(self, response):
        gather = response.append(twilio.Gather(url, method,
            number_of_digits, timeout, finish_on_key))

        children = GatherChild.objects.filter(parent=self).order_by('order')

        for child in children:
            child.cast().add_to_response(gather)

class GatherChild(TwilioVerb):
    parent = models.ForeignKey(Gather, null=True)

    class Meta:
        abstract = True

class Say(GatherChild):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    LANGUAGE_CHOICES = (
        ('E', 'English'),
        ('S', 'Spanish'),
        ('F', 'French'),
        ('G', 'German'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    langauge = models.CharField(max_length=1, choices=LANGUAGE_CHOICES)
    loop = models.IntegerField()
    text = models.CharField(max_length=500)

    def add_to_response(self, response):
        response.append(twilio.Say(text, gender, language, loop))

class Play(GatherChild):
    loop = models.IntegerField()
    url = models.URLField(verify_exists=False, max_length=200)

    def add_to_response(self, response):
        response.append(twilio.Play(url, loop))

class Pause(GatherChild):
    length = models.PositiveIntegerField()

    def add_to_response(self, response):
        response.append(twilio.Pause(length))

class Redirect(TwilioVerb):
    method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    url = models.URLField(verify_exists=False, max_length=200)
   
    def add_to_response(self, response):
        response.append(twilio.Redirect(url, method))

class Hangup(TwilioVerb):
    def add_to_response(self, response):
        response.append(twilio.Hangup())

class Sms(TwilioVerb):
    to_number = models.CharField(max_length=100)
    from_number = models.CharField(max_length=100)
    method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    url = models.URLField(verify_exists=False, max_length=200)
    status_callback = models.URLField(verify_exists=False, max_length=200)
    message = models.CharField(max_length=140)

    def add_to_response(self, response):
        response.append(twilio.Sms(message, to_number, from_number, 
            method, url, status_callback))

class Dial(TwilioVerb):
    method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    url = models.URLField(verify_exists=False, max_length=200)
    timeout = models.PositiveIntegerField(default=30)
    hangup_on_star = models.BooleanField(default=False)
    time_limit = models.PositiveIntegerField()
    caller_id = models.CharField(max_length=100)

    def add_to_response(self, response):
        dial = response.append(twilio.Dial(action=url, method=method))

        children = DialChild.objects.filter(parent=self).order_by('order')

        for child in children:
            child.cast().add_to_response(dial)

class DialChild(TwilioNoun):
    parent = models.ForeignKey(Dial)
    class Meta:
        abstract = True

class Number(DialChild):
    number = models.CharField(max_length=100)
    send_digits = models.CharField(max_length=100)
    url = models.URLField(verify_exists=False, max_length=200)

    def add_to_response(self, response):
        response.append(twilio.Number(number, send_digits))

class Conference(DialChild):
    name = models.CharField(max_length=100)
    muted = models.BooleanField()
    beep = models.BooleanField()
    start_conference_on_enter = models.BooleanField()
    end_conference_on_exit = models.BooleanField()
    wait_method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    wait_url = models.URLField(verify_exists=False, max_length=200)

    def add_to_response(self, response):
        response.append(twilio.Conference(name, muted, beep, 
            start_conference_on_enter, end_conference_on_exit, 
            wait_url, wait_method))

class Record(TwilioVerb):
    method = models.CharField(max_length=1, choices=METHOD_CHOICES)
    url = models.URLField(verify_exists=False, max_length=200)
    timeout = models.PositiveIntegerField(default=5)
    #finish_on_key = models.CharField(max_length=20)
    max_length_seconds = models.PositiveIntegerField(default=3600)
    #transcribe = models.BooleanField(default=False)
    #transcribe_callback = models.URLField(verify_exists=False, max_length=200)
    #play_beep = models.BooleanField(default=True)

    def add_to_response(self, response):
        response.append(twilio.Record(url, method, max_length, 
            timeout))

class Reject(TwilioVerb):
    REASON_CHOICES = (
        ('R', 'Rejected'),
        ('B', 'Busy'),
    )
    reason = models.CharField(max_length=1, choices=REASON_CHOICES)

    def add_to_response(self, response):
        response.append(twilio.Reject(reason))

