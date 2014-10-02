# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Claim.claimType'
        db.add_column(u'clients_claim', 'claimType',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=21, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Claim.claimType'
        db.delete_column(u'clients_claim', 'claimType')


    models = {
        u'clients.claim': {
            'Meta': {'object_name': 'Claim'},
            'amountClaimed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'claimType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '21', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']", 'null': 'True', 'blank': 'True'}),
            'expectedBack': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Insurance']", 'null': 'True', 'blank': 'True'}),
            'invoiceDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paidDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paymentType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '6', 'blank': 'True'}),
            'submittedDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
        u'clients.coveragetype': {
            'Meta': {'object_name': 'CoverageType'},
            'coveragePercent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coverageType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '21', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Insurance']"}),
            'maxClaimAmount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'totalClaimed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'gaitScan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insuranceCard': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'policyNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'blank': 'True'})
        },
        u'clients.insuranceclaim': {
            'Meta': {'object_name': 'InsuranceClaim'},
            'amountClaimed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Claim']"}),
            'coverageType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.CoverageType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'clients.prescription': {
            'Meta': {'object_name': 'Prescription'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clients.Client']"}),
            'dateAdded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['clients']