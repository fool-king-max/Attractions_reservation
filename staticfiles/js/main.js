// 监听点击省份的事件，加载对应省份的景点
document.querySelectorAll('.province-item').forEach(function(provinceItem) {
    provinceItem.addEventListener('click', function() {
        const provinceName = provinceItem.dataset.province;  // 获取省份名称
        console.log('Selected province:', provinceName);  // 调试信息
        loadAttractionsByProvince(provinceName);
    });
});

// 根据省份加载对应的景点，仅展示景点列表
function loadAttractionsByProvince(provinceId) {
    // 发起 AJAX 请求获取省份对应的景点数据
    fetch(`/attractions/${provinceId}/`)
        .then(response => response.json())
        .then(data => {
            const attractionsContainer = document.getElementById('attractions-placeholder');
            attractionsContainer.innerHTML = ''; // 清空当前展示的内容

            // 判断该省份是否有景点数据
            if (data.attractions.length === 0) {
                attractionsContainer.innerHTML = `<p>该省份没有景点。</p>`;
            } else {
                // 遍历景点并生成简单的列表，只展示名称和点击事件
                const attractionsHtml = data.attractions.map(attraction => {
                    return `
                    <div class="attraction-item" onclick="loadAttractionDetail(${attraction.id})">
                        <h3>${attraction.name}</h3>
                        <p>价格：${attraction.total_price} 位置：${attraction.location}</p>
                    </div>
                    `;
                }).join('');
                attractionsContainer.innerHTML = attractionsHtml;
            }
        })
        .catch(error => {
            console.error('Error fetching attractions:', error);
            document.getElementById('attractions-placeholder').innerHTML = `<p>加载景点数据失败，请稍后再试。</p>`;
        });
}

// 加载景点详情，展示详细信息、描述和图片
function loadAttractionDetail(attractionId) {
    fetch(`/attractions/detail/${attractionId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);  // 调试输出返回的数据

            // 更新右侧景点详情区域
            const attraction = data.attraction;
            document.getElementById('attraction-info').innerHTML = `
                <h3>${attraction.name}</h3>
                <img src="${attraction.image_url}" alt="${attraction.name}" class="attraction-image">
                <p>价格：${attraction.total_price}</p>
                <p>位置：${attraction.location}</p>
                <p>描述：${attraction.description || '暂无描述'}</p>
            `;

            // 填充隐藏的表单字段（例如用于提交预约）
            document.getElementById('attraction-id').value = attractionId;
            document.getElementById('reservation-form').style.display = 'block';

            // 更新评论列表
            const reviewsList = document.getElementById('reviews-list');
            const noReviewsMessage = document.getElementById('no-reviews-message');

            // 清空现有评论
            reviewsList.innerHTML = '';

            if (attraction.reviews && attraction.reviews.length > 0) {
                // 隐藏“暂无评论”信息
                if (noReviewsMessage) {
                    noReviewsMessage.style.display = 'none';
                }

                // 动态添加评论
                attraction.reviews.forEach(review => {
                    const [name, rating, comment, createdAt] = review;
                    const reviewItem = `
                        <div class="review-container">
                            <p class="review-name">${name}</p>
                            <p class="review-rating">Rating: ${'⭐'.repeat(rating)}</p>
                            <p class="review-comment">${comment}</p>
                            <p class="review-date">Date: ${createdAt}</p>

                        </div>
                    `;
                    reviewsList.innerHTML += reviewItem;
                });
            } else {
                // 显示“暂无评论”信息
                if (noReviewsMessage) {
                    noReviewsMessage.style.display = 'block';
                }
            }
        })
        .catch(error => {
            console.error('Error fetching attraction details:', error);
            document.getElementById('attraction-info').innerHTML = `<p>加载景点详情失败，请稍后再试。</p>`;
            alert(`Error: ${error.message}`);
        });
}

// 跳转到预约页面，URL 中包含景点ID
function redirectToReservationPage() {
    const attractionId = document.getElementById('attraction-id').value;
    window.location.href = `/reserve/${attractionId}/`;
}

//评论
document.getElementById('comment-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const attractionId = document.getElementById('attraction-id').value;
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;

    fetch(`/attractions/submit_review/${attractionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new URLSearchParams({ rating, comment })
    })

    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("评论提交成功！");
            window.location.reload();
        } else {
            alert(data.messsge);
        }
    })
    .catch(error => console.error('Error:', error));
    const attractionIdElement = document.getElementById('attraction-id');
    if (attractionIdElement) {
        const attractionId = attractionIdElement.value;
        // 使用 attractionId 进行操作
    } else {
        console.error("attraction-id element not found in DOM");
}

});
