Django-DART
===========
DoubleClick Ad Generator
------------------------

A simple Django application for generating DoubleClick adtags inside of Djanog tempaltes.

###Defaults
Defaults are set inside of settings.py, and should at a minimum contain the 'site' and a default fallback zone

    DART_AD_DEFAULTS = {
        'site':'wiretest',
        'zone':'misc'
        # etc...
    }


###In the views
In the view, you can set ad variables for all the ads that will show up on that page

    Ad.set(by="Josh West", tag="white house")


###In a templates
In the templates you can use the ad_tag tempalte tag

    {% load ad_tags %}

    {{ "pos=promo size=336x90 other=sample"|ad_tag }}


###Structure

- The base python Ad class is dart.ads.Ad
- The django-template tag is located in dart.templatetags.ad_tags
- The HTML is dart/templates/ad.html

