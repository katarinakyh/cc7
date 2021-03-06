# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.time'
        db.delete_column('event_event', 'time')

        # Deleting field 'Event.date'
        db.delete_column('event_event', 'date')

        # Adding field 'Event.date_from'
        db.add_column('event_event', 'date_from',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.time_from'
        db.add_column('event_event', 'time_from',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.date_to'
        db.add_column('event_event', 'date_to',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.time_to'
        db.add_column('event_event', 'time_to',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.time'
        db.add_column('event_event', 'time',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Event.date'
        db.add_column('event_event', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 12, 12, 0, 0)),
                      keep_default=False)

        # Deleting field 'Event.date_from'
        db.delete_column('event_event', 'date_from')

        # Deleting field 'Event.time_from'
        db.delete_column('event_event', 'time_from')

        # Deleting field 'Event.date_to'
        db.delete_column('event_event', 'date_to')

        # Deleting field 'Event.time_to'
        db.delete_column('event_event', 'time_to')


    models = {
        'account.association': {
            'Meta': {'object_name': 'Association'},
            'association': ('django.db.models.fields.CharField', [], {'max_length': '122'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'association'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organiser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Association']"}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time_from': ('django.db.models.fields.TimeField', [], {}),
            'time_to': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['event']