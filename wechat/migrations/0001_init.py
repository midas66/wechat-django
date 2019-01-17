# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-17 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('menuid', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('click', 'CLICK'), ('miniprogram', 'MINIPROGRAM'), ('view', 'VIEW')], max_length=20, null=True)),
                ('content', jsonfield.fields.JSONField()),
                ('ext_info', jsonfield.fields.JSONField()),
                ('weight', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageHandler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='名称')),
                ('src', models.PositiveSmallIntegerField(choices=[(0, 'wechat'), (2, 'self'), (1, 'menu')], default=2, editable=False)),
                ('strategy', models.CharField(choices=[('reply_all', 'reply_all'), ('random_one', 'random_one')], default='random_one', max_length=10, verbose_name='strategy')),
                ('starts', models.DateTimeField(blank=True, null=True, verbose_name='starts')),
                ('ends', models.DateTimeField(blank=True, null=True, verbose_name='ends')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('weight', models.IntegerField(default=0, verbose_name='weight')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
            ],
            options={
                'ordering': ('-weight', '-created'),
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(choices=[('custom', 'CUSTOM'), ('forward', 'FORWARD'), ('image', 'IMAGE'), ('music', 'MUSIC'), ('news', 'NEWS'), ('text', 'TEXT'), ('video', 'VIDEO'), ('voice', 'VOICE')], max_length=16, verbose_name='type')),
                ('content', jsonfield.fields.JSONField()),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='wechat.MessageHandler')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('all', 'ALL'), ('contain', 'CONTAIN'), ('equal', 'EQUAL'), ('event', 'EVENT'), ('eventkey', 'EVENTKEY'), ('msg_type', 'MSGTYPE'), ('regex', 'REGEX')], max_length=16, verbose_name='type')),
                ('rule', jsonfield.fields.JSONField(blank=True)),
                ('weight', models.IntegerField(default=0, verbose_name='weight')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('handler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='wechat.MessageHandler')),
            ],
            options={
                'ordering': ('-weight',),
            },
        ),
        migrations.CreateModel(
            name='WechatApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='title')),
                ('name', models.CharField(help_text='公众号标识', max_length=16, unique=True, verbose_name='名称')),
                ('desc', models.TextField(blank=True, default='', verbose_name='description')),
                ('appid', models.CharField(max_length=32, unique=True, verbose_name='AppId')),
                ('appsecret', models.CharField(max_length=64, verbose_name='AppSecret')),
                ('token', models.CharField(blank=True, max_length=32, null=True)),
                ('encoding_aes_key', models.CharField(blank=True, max_length=43, null=True, verbose_name='EncodingAESKey')),
                ('encoding_mode', models.PositiveSmallIntegerField(choices=[(0, 'plain'), (2, 'safe')], default=0, verbose_name='encoding mode')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
            ],
        ),
        migrations.AddField(
            model_name='messagehandler',
            name='app',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='message_handlers', to='wechat.WechatApp'),
        ),
        migrations.AddField(
            model_name='menu',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='wechat.WechatApp'),
        ),
        migrations.AddField(
            model_name='menu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_button', to='wechat.Menu'),
        ),
        migrations.AlterIndexTogether(
            name='messagehandler',
            index_together=set([('app', 'weight', 'created')]),
        ),
    ]