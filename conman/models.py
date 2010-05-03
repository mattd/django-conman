from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

import mptt

class Page(models.Model):
    DRAFT = 0
    PUBLISHED = 1
    HIDDEN = 2
    STATUSES = (
        (PUBLISHED, _('Published')),
        (HIDDEN, _('Hidden')),
        (DRAFT, _('Draft')),
    )

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'))
    author = models.ForeignKey(User, verbose_name=_('author'), blank=True, 
        null=True)
    body = models.TextField(_('body'))
    parent = models.ForeignKey('self', null=True, blank=True, 
        related_name='children', verbose_name=_('parent'))
    sites = models.ManyToManyField(Site, default=[settings.SITE_ID], 
        verbose_name=_('sites'))
    creation_date = models.DateTimeField(_('creation date'), 
        default=datetime.now)
    last_modification_date = models.DateTimeField(_('last modification date'), 
        null=True, blank=True)

    @property
    def url(self):
        url = '/'
        for ancestor in self.get_ancestors():
            url += ancestor.slug + '/'
        url += self.slug + '/'
        return url 

    def save(self):
        if self.id:
            self.creation_date = self.creation_date
            self.last_modification_date = datetime.now()
        super(Page,self).save()

    class Meta:
        ordering = ('tree_id','level',)

    def __unicode__(self):
        return u'%s' % self.title

mptt.register(Page)
