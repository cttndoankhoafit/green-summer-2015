# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=40, db_index=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='T\xean ho\u1ea1t \u0111\u1ed9ng')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='T\xean s\u1ef1 ki\u1ec7n')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('activity', models.ForeignKey(to='mms_backoffice.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityEventMemberParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=False)),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('event', models.ForeignKey(to='mms_backoffice.ActivityEvent')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.ForeignKey(to='mms_backoffice.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Lo\u1ea1i ho\u1ea1t \u0111\u1ed9ng')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityUserManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=0, max_length=8, null=True, verbose_name='Quy\u1ec1n h\u1ea1n', choices=[('\u0110\u1ecdc', '\u0110\u1ecdc'), ('Ghi', 'Ghi'), ('Qu\u1ea3n tr\u1ecb', 'Qu\u1ea3n tr\u1ecb')])),
                ('activity', models.ForeignKey(to='mms_backoffice.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('identify', models.CharField(max_length=20, serialize=False, verbose_name='M\xe3 s\u1ed1', primary_key=True)),
                ('first_name', models.CharField(max_length=8, verbose_name='T\xean')),
                ('last_name', models.CharField(max_length=128, verbose_name='H\u1ecd')),
                ('gender', models.CharField(default=0, max_length=3, null=True, verbose_name='Gi\u1edbi t\xednh', choices=[('Nam', 'Nam'), ('N\u1eef', 'N\u1eef')])),
                ('date_of_birth', models.DateField(default=None, null=True, verbose_name='Ng\xe0y sinh', blank=True)),
                ('place_of_birth', models.CharField(default=None, max_length=128, null=True, verbose_name='N\u01a1i sinh', blank=True)),
                ('folk', models.CharField(default=None, max_length=32, null=True, verbose_name='D\xe2n t\u1ed9c', blank=True)),
                ('religion', models.CharField(default=None, max_length=32, null=True, verbose_name='T\xf4n gi\xe1o', blank=True)),
                ('address', models.CharField(default=None, max_length=128, null=True, verbose_name='\u0110\u1ecba ch\u1ec9 th\u01b0\u1eddng tr\xfa', blank=True)),
                ('ward', models.CharField(default=None, max_length=128, null=True, verbose_name='X\xe3/Ph\u01b0\u1eddng/Th\u1ecb tr\u1ea5n', blank=True)),
                ('district', models.CharField(default=None, max_length=128, null=True, verbose_name='Qu\u1eadn/Huy\u1ec7n/Th\xe0nh ph\u1ed1 thu\u1ed9c t\u1ec9nh', blank=True)),
                ('province', models.CharField(default=None, max_length=128, null=True, verbose_name='T\u1ec9nh/Th\xe0nh ph\u1ed1', blank=True)),
                ('temporary_address', models.CharField(default=None, max_length=128, null=True, verbose_name='\u0110\u1ecba ch\u1ec9 t\u1ea1m tr\xfa', blank=True)),
                ('home_phone', models.CharField(default=None, max_length=32, null=True, verbose_name='\u0110i\u1ec7n tho\u1ea1i', blank=True)),
                ('mobile_phone', models.CharField(default=None, max_length=32, null=True, verbose_name='\u0110i\u1ec7n tho\u1ea1i di \u0111\u1ed9ng', blank=True)),
                ('email', models.EmailField(default=None, max_length=128, null=True, verbose_name='Email', blank=True)),
                ('details', models.CharField(default=None, max_length=2048, null=True, verbose_name='Th\xf4ng tin kh\xe1c', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='T\xean t\u1ed5 ch\u1ee9c')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('organization_managed', models.ForeignKey(related_name='organization_managed', to='mms_backoffice.Organization')),
                ('organization_manager', models.ForeignKey(related_name='organization_manager', to='mms_backoffice.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('member', models.ForeignKey(to='mms_backoffice.Member')),
                ('organization', models.ForeignKey(to='mms_backoffice.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Lo\u1ea1i t\u1ed5 ch\u1ee9c')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationUserManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permission', models.CharField(default=0, max_length=8, null=True, verbose_name='Quy\u1ec1n h\u1ea1n', choices=[('\u0110\u1ecdc', '\u0110\u1ecdc'), ('Ghi', 'Ghi'), ('Qu\u1ea3n tr\u1ecb', 'Qu\u1ea3n tr\u1ecb')])),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('organization', models.ForeignKey(to='mms_backoffice.Organization')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(to='mms_backoffice.OrganizationType'),
        ),
        migrations.AddField(
            model_name='activityorganization',
            name='organization',
            field=models.ForeignKey(to='mms_backoffice.Organization'),
        ),
        migrations.AddField(
            model_name='activityeventmemberparticipation',
            name='member',
            field=models.ForeignKey(to='mms_backoffice.Member'),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(to='mms_backoffice.ActivityType'),
        ),
        migrations.AddField(
            model_name='user',
            name='member',
            field=models.ForeignKey(default=None, blank=True, to='mms_backoffice.Member', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationusermanager',
            unique_together=set([('organization', 'user', 'permission')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationmember',
            unique_together=set([('organization', 'member')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationmanager',
            unique_together=set([('organization_manager', 'organization_managed')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityusermanager',
            unique_together=set([('activity', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityorganization',
            unique_together=set([('activity', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityeventmemberparticipation',
            unique_together=set([('member', 'event')]),
        ),
    ]
