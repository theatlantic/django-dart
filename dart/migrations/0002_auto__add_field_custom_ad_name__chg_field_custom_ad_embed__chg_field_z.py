# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Custom_Ad.name'
        db.add_column('dart_custom_ad', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Changing field 'Custom_Ad.embed'
        db.alter_column('dart_custom_ad', 'embed', self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Changing field 'Zone.slug'
        db.alter_column('dart_zone', 'slug', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Zone.name'
        db.alter_column('dart_zone', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Custom_Ad.name'
        db.delete_column('dart_custom_ad', 'name')

        # Changing field 'Custom_Ad.embed'
        db.alter_column('dart_custom_ad', 'embed', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Zone.slug'
        db.alter_column('dart_zone', 'slug', self.gf('django.db.models.fields.CharField')(max_length=765))

        # Changing field 'Zone.name'
        db.alter_column('dart_zone', 'name', self.gf('django.db.models.fields.CharField')(max_length=765))
    
    
    models = {
        'dart.custom_ad': {
            'Meta': {'object_name': 'Custom_Ad'},
            'embed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'dart.position': {
            'Meta': {'object_name': 'Position'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dart.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dart.Position']", 'through': "orm['dart.Zone_Position']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dart.zone_position': {
            'Meta': {'object_name': 'Zone_Position'},
            'custom_ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Custom_Ad']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Position']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Zone']"})
        }
    }
    
    complete_apps = ['dart']
