"""
自定义的分页组件，以下是使用该组件的方法示例：
def pretty_list(request):

    from app01.utils.Pagination import Pagination

    # 搜索
    data_dict = {}
    search_data = request.GET.get("search", '')
    if search_data:
        data_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request,queryset)
    page_queryset=page_object.page_queryset
    page_string=page_object.html()

    context={
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }

    return render(request, 'pretty_list.html', context)

In html:
    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
from django.utils.safestring import mark_safe

class Pagination(object):

    def __init__(self, request, queryset, list_size=10, page_param="page", plus=5):

        # 保留原来GET参数，例如进行了搜索+分页
        from django.http.request import QueryDict
        import copy
        query_dict=copy.deepcopy(request.GET)
        query_dict._mutable=True
        self.query_dict=query_dict
        self.page_param=page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = (int)(page)
        else:
            page = 1
        self.page = page
        self.list_size = list_size
        self.list_start = (page - 1) * list_size
        self.list_end = page * list_size

        self.page_queryset = queryset[self.list_start:self.list_end]

        # 计算总页码
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, list_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出显示当前页的前5页，后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库数据较少，都没有达到11页
            page_start = 1
            page_end = self.total_page_count
        else:
            # 数据库中的数据足够多
            if self.page <= self.plus:
                # 当前页小于5时
                page_start = 1
                page_end = 2 * self.plus + 1
            else:
                # 当前页大于5时
                if self.page + self.plus > self.total_page_count:
                    page_start = self.total_page_count - 2 * self.plus
                    page_end = self.total_page_count
                else:
                    page_start = self.page - self.plus
                    page_end = self.page + self.plus

        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页码
        for i in range(page_start, page_end + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 页码搜索
        # 注意这里html使用的是bootstrap3,根据自己的需求更改
        # 这里有bug,页码搜索会覆盖数据搜索的参数
        search_string = """
            <li>
                <form method="get" style="float: right;width:150px" class="input-group">
                    <input type="text" class="form-control" name="page" placeholder="页码">
                    <span class="input-group-btn"><button class="btn btn-default" type="submit">跳转</button>
                    </span>
                </form>
            </li>
            """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
