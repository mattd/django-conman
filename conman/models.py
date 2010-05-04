from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
import mptt


class PageManager(models.Manager):
    def get_page_by_uri_or_404(self, uri):
        uri_frags = uri.strip('/').split('/')
        slug = uri_frags[-1]
        pages = Page.objects.filter(slug=slug)
        for page in pages:
            frags = [p.slug for p in page.get_ancestors()]
            frags.append(page.slug)
            if frags == uri_frags:
                return page
        raise Http404


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

    objects = PageManager()

    @property
    def uri(self):
        uri = '/'
        for ancestor in self.get_ancestors():
            uri += ancestor.slug + '/'
        uri += self.slug + '/'
        return uri 

    def save(self):
        if self.id:
            self.creation_date = self.creation_date
            self.last_modification_date = datetime.now()
        super(Page,self).save()

    class Meta:
        ordering = ('tree_id','level',)

    def __unicode__(self):
        level_marker = ''
        for i in range(1, self.level + 1):
            level_marker += '-'
        return u'%s' % level_marker + self.title

mptt.register(Page)
