# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _

from shuup.front.apps.carousel.models import Carousel
from shuup.xtheme import TemplatedPlugin
from shuup.xtheme.plugins.forms import TranslatableField

from .forms import CarouselConfigForm


class CarouselPlugin(TemplatedPlugin):
    identifier = "shuup.front.apps.carousel.carousel"
    name = _("Carousel Plugin")
    template_name = "shuup/carousel/carousel.jinja"
    fields = [("carousel", None)]
    editor_form_class = CarouselConfigForm

    def get_context_data(self, context):
        """
        Use only slides that has translated image in current language

        :param context: current context
        :return: updated plugin context
        :rtype: dict
        """
        carousel_id = self.config.get("carousel")
        return {
            "request": context["request"],
            "carousel": Carousel.objects.filter(id=carousel_id).first() if carousel_id else None,
            "type": "carousel"
        }


class BannerBoxPlugin(CarouselPlugin):
    identifier = "shuup.front.apps.carousel.banner_box"
    name = _("Banner Box")
    editor_form_class = CarouselConfigForm
    fields = [
        ("title", TranslatableField(label=_("Title"), required=False, initial="")),
    ]

    def get_context_data(self, context):
        """
        Add title from config to context data

        :param context: Current context
        :return: updated Plugin context
        :rtype: dict
        """
        data = super(BannerBoxPlugin, self).get_context_data(context)
        data["title"] = self.get_translated_value("title")
        data["type"] = "banner_box"
        return data
