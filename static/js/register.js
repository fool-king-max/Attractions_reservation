
$(document).ready(function () {
    // 为所有表单元素添加样式
    $(".load-form")
        .find("input, select")
        .each(function () {
            $(this).addClass("form-control");
        });

    $(".load-form")
        .find("label")
        .each(function () {
            $(this).addClass("ml-2");
            $(this).css({
                "font-size": "20px",
                "color": "#8a8a8a",
                "display": "block",
            });
            var raw = $(this).html();
            $(this).html(ChangeLabel(raw));
        });

    // 监听表单提交按钮
    $("#signup-button").click(function (event) {
        event.preventDefault(); // 防止表单默认提交

        // 获取表单数据
        var formData = {
            username: $("#id_username").val(),
            password1: $("#id_password1").val(),
            password2: $("#id_password2").val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        };

        // AJAX 提交表单数据到后端
        $.ajax({
            type: "POST",
            url: "/users/signup/",
            data: formData,
            success: function (response) {
                alert("注册成功！");
                window.location.href = "/users/signin/"; // 跳转到登录页面
            },
            error: function (xhr) {
                alert("注册失败，请检查您的输入。");
                console.log(xhr.responseText);
            },
        });
    });
});

// 标签转换函数
function ChangeLabel(label) {
    var labels = {
        "Gender:": "性别",
        "Born date:": "出生日期",
        "Phone:": "联系方式",
        "Address:": "地址",
        "Price:": "价格",
        "Username:": "用户名:",
        "Password:": "密码:",
        "Password confirmation:": "再次输入密码:",
    };
    return labels[label] !== undefined ? labels[label] : label;
}
