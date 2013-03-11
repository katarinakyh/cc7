# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.time_from'
        db.delete_column('event_event', 'time_from')

        # Deleting field 'Event.date_to'
        db.delete_column('event_event', 'date_to')

        # Deleting field 'Event.time_to'
        db.delete_column('event_event', 'time_to')

        # Deleting field 'Event.date_from'
        db.delete_column('event_event', 'date_from')

        # Adding field 'Event.datetime_from'
        db.add_column('event_event', 'datetime_from',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.datetime_to'
        db.add_column('event_event', 'datetime_to',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.time_from'
        db.add_column('event_event', 'time_from',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.date_to'
        db.add_column('event_event', 'date_to',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.time_to'
        db.add_column('event_event', 'time_to',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.date_from'
        db.add_column('event_event', 'date_from',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 11, 0, 0)),
                      keep_default=False)

        # Deleting field 'Event.datetime_from'
        db.delete_column('event_event', 'datetime_from')

        # Deleting field 'Event.datetime_to'
        db.delete_column('event_event', 'datetime_to')


    models = {
        'account.association': {
            'Meta': {'object_name': 'Association'},
            'association': ('django.db.models.fields.CharField', [], {'max_length': '122'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_from': ('django.db.models.fields.DateTimeField', [], {}),
            'datetime_to': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organiser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Association']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['event']