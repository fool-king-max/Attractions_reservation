document.getElementById('reservation-form').addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单默认提交

    const formData = new FormData(this);  // 获取表单数据
    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // 如果提交成功，重定向到预约成功页面
            window.location.href = response.url;  // 使用 response.url 重定向
        } else {
            alert('预约失败，请稍后再试！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('出现错误，请稍后再试！');
    });
});
