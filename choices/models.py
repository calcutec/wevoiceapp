# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.conf import settings
import os.path


class Admin(models.Model):
    username = models.TextField()
    password = models.TextField()

    class Meta:
        managed = True
        db_table = 'admin'


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    client = models.ForeignKey("Client")

    def first_name(self):
        return self.user.first_name
    first_name.short_description = 'First Name'

    def last_name(self):
        return self.user.last_name
    last_name.short_description = 'Last Name'

    def email(self):
        return self.user.email
    email.short_description = 'Email'

    def is_active(self):
        return self.user.is_active
    is_active.short_description = 'Active'

    def is_superuser(self):
        return self.user.is_superuser
    is_superuser.short_description = 'Superuser'

    def date_joined(self):
        return self.user.date_joined
    date_joined.short_description = 'Joined'

    def last_login(self):
        return self.user.last_login
    last_login.short_description = 'Last Login'

    def is_staff(self):
        return self.user.is_staff
    is_staff.short_description = 'Is Staff'

    def __unicode__(self):
        return self.user.username


class Anheuserbusch(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'anheuserbusch'


class Apple(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'apple'
        verbose_name = 'The Force'
        verbose_name_plural = 'The Force'


class Cisco(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'cisco'


class Client(models.Model):
    name = models.TextField()
    username = models.TextField()
    password = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'client'
        ordering = ['name']


class Esterline(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'esterline'


class Google(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'google'


class Gt(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'gt'


class Hd(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'hd'


class Jdeere(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'jdeere'


class Kornferry(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'kornferry'


class Language(models.Model):
    language = models.TextField()

    class Meta:
        managed = True
        db_table = 'language'


class Main(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'main'
        verbose_name = 'Main Talent'
        verbose_name_plural = 'Main Talents'


class Nrm(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'nrm'


class Rating(models.Model):
    rating = models.IntegerField(default=0, blank=True, null=True)
    talent = models.ForeignKey('Talent')
    rater = models.ForeignKey('UserProfile')

    class Meta:
        unique_together = ('talent', 'rater',)


class Resaas(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'resaas'
        verbose_name = 'Resaas'
        verbose_name_plural = 'Resaas'


class Thomsonreuters(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'thomsonreuters'


class Talent(models.Model):
    welo_id = models.TextField()
    vendor_id = models.TextField()
    vendor_name = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    audio_file = models.FileField(blank=True)
    times_rated = models.IntegerField(default=0, blank=True, null=True)
    total_rating = models.IntegerField(default=0, blank=True, null=True)

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = \
                '<div class="simple-player-container" style="background-color: #ffffff;">' \
                '<audio class="player" preload="none" src="%s"></audio>' \
                '</div>' % file_url
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = "Audio player"

    def average_rating(self):
        if self.times_rated > 0:
            return int(round(float(self.total_rating) / float(self.times_rated)))

    average_rating.short_description = "Rating"

    pre_approved = models.TextField()
    comment = models.TextField(null=True, blank=True)
    allclients = models.TextField()
    vmware = models.TextField()
    google = models.TextField()
    gt = models.TextField()
    nrm = models.TextField()
    hr = models.TextField()
    rate = models.TextField(null=True, blank=True)
    hd = models.TextField()
    workday = models.TextField()
    tts = models.TextField()
    cisco = models.TextField()
    kornferry = models.TextField()
    jdeere = models.TextField()
    anheuserbusch = models.TextField()
    apple = models.TextField()
    thomsonreuters = models.TextField()
    esterline = models.TextField()

    def __unicode__(self):
        return self.welo_id

    class Meta:
        managed = True
        db_table = 'talent'
        ordering = ['welo_id']


class Vendor(models.Model):
    name = models.TextField()
    username = models.TextField()
    password = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'vendor'


class Vmware(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'vmware'


class Workday(models.Model):
    talent = models.TextField()
    client = models.TextField()
    gender = models.TextField()
    age_range = models.TextField()
    language = models.TextField()
    sample_url = models.TextField()
    accepted = models.TextField()
    comment = models.TextField()

    class Meta:
        managed = True
        db_table = 'workday'


class Selection(models.Model):
    talent = models.ForeignKey(Talent)
    client = models.ForeignKey(Client)
    STATUS_CHOICES = (
        ("PREAPPROVED", "Pre_Approved"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected")
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="PREAPPROVED")

    def talent_language(self):
        return self.talent.language
    talent_language.short_description = 'Language'

    def talent_gender(self):
        return self.talent.gender
    talent_gender.short_description = 'Gender'

    def talent_age_range(self):
        return self.talent.age_range
    talent_age_range.short_description = 'Age Range'

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.talent.audio_file:
            file_url = settings.MEDIA_URL + str(self.talent.audio_file)
            player_string = \
                '<div class="simple-player-container" style="background-color: #ffffff;">' \
                '<audio class="player" preload="none" src="%s"></audio>' \
                '</div>' % file_url
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = "Audio player"

    class Meta:
        unique_together = ('talent', 'client',)

    def __unicode__(self):
        return self.talent.welo_id + ": " + self.client.username


class Comment(models.Model):
    post = models.ForeignKey(Selection, related_name='comments')
    author = models.ForeignKey(UserProfile)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
