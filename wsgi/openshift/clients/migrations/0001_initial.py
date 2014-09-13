# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dependent'
        db.create_table(u'clients_dependent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('lastName', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'clients', ['Dependent'])

        # Adding model 'Client'
        db.create_table(u'clients_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstName', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('lastName', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('postalCode', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('phoneNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=14, blank=True)),
            ('cellNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=14, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('healthcareNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
            ('employer', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('credit', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('referredBy', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'clients', ['Client'])

        # Adding M2M table for field dependents on 'Client'
        m2m_table_name = db.shorten_name(u'clients_client_dependents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm[u'clients.client'], null=False)),
            ('dependent', models.ForeignKey(orm[u'clients.dependent'], null=False))
        ))
        db.create_unique(m2m_table_name, ['client_id', 'dependent_id'])

        # Adding model 'Insurance'
        db.create_table(u'clients_insurance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'])),
            ('provider', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('coverageType', self.gf('django.db.models.fields.CharField')(default='', max_length=21, blank=True)),
            ('policyNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('contractNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True)),
            ('coveragePercent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('maxClaimAmount', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('totalClaimed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('period', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('billing', self.gf('django.db.models.fields.CharField')(default='', max_length=8, blank=True)),
        ))
        db.send_create_signal(u'clients', ['Insurance'])

        # Adding model 'Claim'
        db.create_table(u'clients_claim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'], null=True, blank=True)),
            ('insurance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Insurance'], null=True, blank=True)),
            ('submittedDate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('invoiceDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('paidDate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('amountClaimed', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('expectedBack', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('paymentType', self.gf('django.db.models.fields.CharField')(default='', max_length=6, blank=True)),
        ))
        db.send_create_signal(u'clients', ['Claim'])

        # Adding model 'Prescription'
        db.create_table(u'clients_prescription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['clients.Client'])),
            ('dateAdded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'clients', ['Prescription'])


    def backwards(self, orm):
        # Deleting model 'Dependent'
        db.delete_table(u'clients_dependent')

        # Deleting model 'Client'
        db.delete_table(u'clients_client')

        # Removing M2M table for field dependents on 'Client'
        db.delete_table(db.shorten_name(u'clients_client_dependents'))

        # Deleting model 'Insurance'
        db.delete_table(u'clients_insurance')

        # Deleting model 'Claim'
        db.delete_table(u'clients_claim')

        # Deleting model 'Prescription'
        db.delete_table(u'clients_prescription')


    models = {
        u'clients.claim': {
            'Meta': {'object_name': 'Claim'},
            'amountClaimed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']", 'null': 'True', 'blank': 'True'}),
            'expectedBack': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Insurance']", 'null': 'True', 'blank': 'True'}),
            'invoiceDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paidDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paymentType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'submittedDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'clients.client': {
            'Meta': {'object_name': 'Client'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'cellNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '14', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'credit': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'dependents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['clients.Dependent']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'firstName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'healthcareNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'phoneNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '14', 'blank': 'True'}),
            'postalCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'referredBy': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        u'clients.dependent': {
            'Meta': {'object_name': 'Dependent'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'firstName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'})
        },
        u'clients.insurance': {
            'Meta': {'object_name': 'Insurance'},
            'billing': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            'contractNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'coveragePercent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coverageType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '21', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxClaimAmount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'policyNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'totalClaimed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'clients.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['clients']