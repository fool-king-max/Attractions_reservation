window.onload = function() {
    const dailyReservationsData = document.getElementById('daily_reservations_data').textContent.trim();

    try {
        const dailyReservations = JSON.parse(dailyReservationsData);
        console.log(dailyReservations);  // 在控制台输出解析后的数据

        // 生成图表
        const dates = Object.keys(dailyReservations);
        const counts = Object.values(dailyReservations);

        const ctx = document.getElementById('reservationChart').getContext('2d');
        const reservationChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,  // x轴日期
                datasets: [{
                    label: '每日预约人数',
                    data: counts,  // y轴预约人数
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: '日期'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: '预约人数'
                        },
                        beginAtZero: true,

                        }
                }
            }
        });
    } catch (error) {
        console.error("Error parsing JSON:", error);
    }
};
function toggleNote(button) {
    const container = button.parentElement;
    const shortNote = container.querySelector('.short-note');
    const fullNote = container.querySelector('.full-note');

    if (fullNote.style.display === 'none') {
        shortNote.style.display = 'none';  // 隐藏短内容
        fullNote.style.display = 'block';  // 显示完整内容
        button.innerText = '收起';  // 修改按钮为“收起”
    } else {
        shortNote.style.display = 'block';  // 显示短内容
        fullNote.style.display = 'none';  // 隐藏完整内容
        button.innerText = '展开';  // 修改按钮为“展开”
    }
}

