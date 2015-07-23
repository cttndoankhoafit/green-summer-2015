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
                ('identify', models.CharField(unique=True, max_length=40, db_index=True)),
                ('first_name', models.CharField(default=None, max_length=8, null=True, verbose_name='T\xean', blank=True)),
                ('last_name', models.CharField(default=None, max_length=128, null=True, verbose_name='H\u1ecd', blank=True)),
                ('gender', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Gi\u1edbi t\xednh', choices=[(0, 'Nam'), (1, 'N\u1eef')])),
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
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['identify'],
            },
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='T\xean ho\u1ea1t \u0111\u1ed9ng')),
                ('start_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('end_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('register_start_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('register_end_time', models.DateTimeField(default=None, null=True, blank=True)),
                ('register_state', models.PositiveSmallIntegerField(default=3, null=True, choices=[(0, '\u0110\u0103ng k\xfd tham gia'), (1, '\u0110\u0103ng k\xfd r\xe8n luy\u1ec7n \u0110o\xe0n vi\xean'), (2, '\u0110\u0103ng k\xfd r\xe8n luy\u1ec7n H\u1ed9i vi\xean'), (3, 'Ho\xe3n \u0111\u0103ng k\xfd')])),
                ('published', models.BooleanField(default=False)),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
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
                ('identify', models.CharField(unique=True, max_length=50, db_index=True)),
                ('name', models.CharField(default=None, max_length=128, null=True, verbose_name='T\xean lo\u1ea1i ho\u1ea1t \u0111\u1ed9ng', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(default=7, null=True, verbose_name='Tr\u1ea1ng th\xe1i', choices=[(0, 'Qu\u1ea3n tr\u1ecb'), (1, '\u0110i\u1ec1u h\xe0nh'), (2, 'C\u1ed9ng t\xe1c vi\xean'), (3, '\u0110\xe3 tham gia'), (4, '\u0110\xe3 \u0111\u0103ng k\xfd'), (5, 'R\xe8n luy\u1ec7n \u0110o\xe0n vi\xean'), (6, 'R\xe8n luy\u1ec7n H\u1ed9i vi\xean'), (7, 'Kh\xf4ng tham gia')])),
                ('activity', models.ForeignKey(to='mms_backoffice.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identify', models.CharField(unique=True, max_length=50, db_index=True)),
                ('name', models.CharField(max_length=128, verbose_name='T\xean t\u1ed5 ch\u1ee9c')),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('manager_organization', models.ForeignKey(default=None, blank=True, to='mms_backoffice.Organization', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identify', models.CharField(unique=True, max_length=50, db_index=True)),
                ('name', models.CharField(max_length=128, verbose_name='Lo\u1ea1i t\u1ed5 ch\u1ee9c')),
                ('management_level', models.PositiveIntegerField()),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(default=3, null=True, choices=[(0, 'Qu\u1ea3n tr\u1ecb ch\xednh'), (1, 'Qu\u1ea3n tr\u1ecb'), (2, '\u0110i\u1ec1u h\xe0nh'), (3, 'Th\xe0nh vi\xean')])),
                ('details', models.CharField(default=None, max_length=2048, null=True, blank=True)),
                ('organization', models.ForeignKey(to='mms_backoffice.Organization')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(default=None, to='mms_backoffice.OrganizationType', null=True),
        ),
        migrations.AddField(
            model_name='activityorganization',
            name='organization',
            field=models.ForeignKey(to='mms_backoffice.Organization'),
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.ForeignKey(to='mms_backoffice.ActivityType'),
        ),
        migrations.AlterUniqueTogether(
            name='organizationuser',
            unique_together=set([('organization', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityuser',
            unique_together=set([('user', 'activity', 'state')]),
        ),
        migrations.AlterUniqueTogether(
            name='activityorganization',
            unique_together=set([('activity', 'organization')]),
        ),
    ]
