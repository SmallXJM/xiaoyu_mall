from collections import OrderedDict

from django.shortcuts import render
from django.views import View

from xiaoyu_mall.apps.goods.models import GoodsChannel


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
        # 渲染模板的上下文
        context = {
            'categories': categories,
        }
        return render(request, 'index.html', context)
