from collections import OrderedDict

from django.shortcuts import render
from django.views import View

from contents.models import ContentCategory
from goods.models import GoodsChannel


class IndexView(View):
    def get(self, request):
        """提供首页广告页面"""
        categories = OrderedDict()
        channels = GoodsChannel.objects.all().order_by('group_id', 'sequence')

        for channel in channels:
            group_id = channel.group_id
            if group_id not in categories:
                categories[group_id] = {
                    'channels': [],
                    'sub_cats': [],
                }
            cat1 = channel.category
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })
            # 查询二级和三级
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)
                # 将二级类别添加到一级类别的sub_cats
                categories[group_id]['sub_cats'].append(cat2)

        # 查询所有的广告类别
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()

        for content_category in content_categories:
            contents[content_category.key] = \
                content_category.content_set.filter(
                    status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)
