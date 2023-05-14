from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环modelform中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            # 若字段中有属性，保留原来的属性；若没有属性，则增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                }
