from django.db import models


# Create your models here.

# 部门表
class Department(models.Model):
    title = models.CharField(verbose_name="名称", max_length=32)

    # 定制显示对象时的返回值
    def __str__(self):
        return self.title


# 用户表
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    gender = models.CharField(verbose_name="性别", max_length=4)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="创建时间")

    # 注意这里会自动加上_id,所以名字是department_id
    # 这里关联了用户表外键与部门表主键，所以在删除部门表数据时对应的用户也会级联删除
    department = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

# 靓号表
class PrettyNum(models.Model):
    mobile=models.CharField(verbose_name="手机号", max_length=11)
    price=models.IntegerField(verbose_name="价格")

    level_choices=(
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    )
    level=models.SmallIntegerField(verbose_name="级别", choices=level_choices,default=1)

    status_choices = (
        (1,"已占用"),
        (2,"未占用"),
    )
    status=models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=2)

# 管理员表
class Admin(models.Model):
    username=models.CharField(verbose_name="用户名",max_length=32)
    password=models.CharField(verbose_name="密码",max_length=64)
