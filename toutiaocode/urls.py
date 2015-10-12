from django.conf.urls import patterns, url, include
from crawl_data.djangosite.resys.views import source_view

from crawl_data.djangosite.resys.views import profile_view

urlpatterns = patterns('',
    url(r'^api/', include('crawl_data.djangosite.resys.urls_profile_api')),
    url(r'^article_search/', include('crawl_data.djangosite.resys.urls_article_search')),
    url(r'^boost_topic/', include('crawl_data.djangosite.resys.urls_boost_topic')),
    url(r'^source/', include('crawl_data.djangosite.resys.urls_source')),
    url(r'^test/$', source_view.test),
    url(r'^profile/$',profile_view.showProfile),
    url(r'^profile/(\w{1,})/$',profile_view.show_profile_detail),
    url(r'profile/ajaxvalue/ajax/$',profile_view.ajax_fun),
    url(r'^profile/add/new/$',profile_view.add_new),
    url(r'^profile/(\w{1,})/changedefine/$',profile_view.profile_detail_changedefine),
    url(r'^profile/(\w{1,})/changeregular/$',profile_view.profile_detail_changeregular),
    url(r'^profile/(\w{1,})/fix/parent/$',profile_view.profile_detail_fixparent),

    url(r'^profile/(\w{1,})/drawback/history/$',profile_view.drawback_history),
    url(r'^profile/profile_tree/ajax/$', profile_view.profile_ajax),

    #url(r'profile/concept_feature/ajax/$', profile_view.read_concept),

)

