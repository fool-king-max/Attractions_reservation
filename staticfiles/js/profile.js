document.getElementById('profile-form').addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单默认提交

    const formData = new FormData(this);  // 获取表单数据

    fetch(window.location.href, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('信息更新成功');
            window.location.reload();  // 刷新页面以显示最新信息
        } else {
            alert('信息更新失败，请稍后再试');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('出现错误，请稍后再试！');
    });
});
