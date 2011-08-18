# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Position'
        db.create_table('dart_position', (
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('dart', ['Position'])

        # Adding model 'Zone'
        db.create_table('dart_zone', (
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=765)),
        ))
        db.send_create_signal('dart', ['Zone'])

        # Adding model 'Custom_Ad'
        db.create_table('dart_custom_ad', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('embed', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('cropduster.models.CropDusterField')(to=orm['cropduster.Image'], null=True, db_column='image_id')),
        ))
        db.send_create_signal('dart', ['Custom_Ad'])

        # Adding model 'Zone_Position'
        db.create_table('dart_zone_position', (
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Position'])),
            ('custom_ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Custom_Ad'], null=True, blank=True)),
            ('image', self.gf('cropduster.models.CropDusterField')(to=orm['cropduster.Image'], null=True, db_column='image_id')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dart.Zone'])),
        ))
        db.send_create_signal('dart', ['Zone_Position'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Position'
        db.delete_table('dart_position')

        # Deleting model 'Zone'
        db.delete_table('dart_zone')

        # Deleting model 'Custom_Ad'
        db.delete_table('dart_custom_ad')

        # Deleting model 'Zone_Position'
        db.delete_table('dart_zone_position')
    
    
    models = {
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cropduster.image': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'Image'},
            '_extension': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_column': "'extension'"}),
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'crop_h': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_w': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_x': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'crop_y': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'default_thumb': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'thumbs': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'thumbs'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cropduster.Thumb']"})
        },
        'cropduster.thumb': {
            'Meta': {'object_name': 'Thumb'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'dart.custom_ad': {
            'Meta': {'object_name': 'Custom_Ad'},
            'embed': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('cropduster.models.CropDusterField', [], {'to': "orm['cropduster.Image']", 'null': 'True', 'db_column': "'image_id'"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '765'}),
            'position': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dart.Position']", 'through': "orm['dart.Zone_Position']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'dart.zone_position': {
            'Meta': {'object_name': 'Zone_Position'},
            'custom_ad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Custom_Ad']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('cropduster.models.CropDusterField', [], {'to': "orm['cropduster.Image']", 'null': 'True', 'db_column': "'image_id'"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Position']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dart.Zone']"})
        }
    }
    
    complete_apps = ['dart']
