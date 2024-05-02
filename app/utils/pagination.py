# 页面跳转类
"""
1.根据自己的情况筛选数据，
    queryset = models.Mobel.objects.all()
2.实例化分页对象
    page_object = Pagination(request,queryset)
3.  page_size:每页显示多少数据
    page_param:分页参数
    plus：跨几页
4.html使用
    <ul class='pagination'>
    {{ page_string }}
    </ul>
"""




from django.utils.safestring import mark_safe


class Pagination(object):
    # 一、定义属性
    def __init__(self,request,queryset,page_size=10,page_param="page",plus=5):

        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 获取当前页码
        page = request.GET.get(page_param,"1")
        # 判断是否是十进制数字
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        # 每页显示的数据数量
        self.page_size = page_size
        # 每页的数据1-10   11-20  ......
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 分完页的数据
        self.page_queryset = queryset[self.start:self.end]

        # 数据的总条数
        self.total_count = queryset.count()

        # divmod 正除数和余数
        # 分页的总页码数量
        total_page_count, div = divmod(self.total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus
    # 二、定义方法
    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param,[1])

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(prev)
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            page_str_list.append(ele)

        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(next)
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            page_str_list.append(next)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                                <form method="get" style="float:left;">
                                    <div class="input-group" style="width:110px;">
                                        <input name="page" class="form-control" type="text" placeholder="page">
                                        <span class="input-group-btn">
                                        <button type="submit" class="btn btn-success">跳转</button>
                                    </span>
                                    </div>
                                </form>
                            </li>
            """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))

        return page_string

