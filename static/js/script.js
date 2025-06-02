console.log(Chart);  // 如果有載入成功，網頁的console會印出一個函式



// 宣告變數：儲存從後端 API 抓到的資料
let eraData = {
  labels: [],
  values: [],
  
};

// 先抓資料，然後呼叫畫圖＆更新趨勢指示
Promise.all([
  fetch('/api/era/').then(res => res.json()),
  fetch('/api/WL/').then(res => res.json())
]).then(([data, winLossData]) => {
  // 更新 ERA 圖表
  eraData.labels = data.labels;
  eraData.values = data.values;
  drawERAChart();
  updatePerformanceIndicator();

  // 更新統計卡片
  const statCards = document.querySelectorAll('.stat-card');
  statCards.forEach(card => {
    const title = card.querySelector('h3').innerText.trim();
    const valueDiv = card.querySelector('.stat-value');

    switch (title) {
      case '勝敗':
        valueDiv.innerText = `${winLossData.wins}-${winLossData.losses}`;
        break;
      case 'ERA':
        valueDiv.innerText = data.latest_era.toFixed(2);
        break;
      case 'WHIP':
        valueDiv.innerText = data.latest_whip.toFixed(2);
        break;
      case 'K/9':
        valueDiv.innerText = data.latest_k9.toFixed(2);
        break;
    }
  });
});



// 🎯 畫 ERA &FIP趨勢圖的函式
function drawERAChart() {
  const ctx = document.getElementById('performanceChart').getContext('2d');
  const fipValues = [1.77, 1.89, 2.17, 2.37, 3.02];
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: eraData.labels,
      datasets: [{
        label: 'ERA',
        data: eraData.values,
        borderColor: '#1a5fb4',
        backgroundColor: 'rgba(26, 95, 180, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
          label: 'FIP',
          data: fipValues,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          tension: 0.4,
          fill: false
        }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: false,
          ticks: {
            callback: value => value.toFixed(2)
          }
        }
      }
    }
  });
}

// 🎯 更新趨勢狀態（⬆️ / ⬇️）
function updatePerformanceIndicator() {
  const indicator = document.querySelector('.performance-indicator');
  const latest = eraData.values.at(-1);
  const previous = eraData.values.at(-2);
  if (latest < previous) {
    indicator.className = 'performance-indicator improving';
    indicator.textContent = '⬆️ Improving: Last 5 starts';
  } else {
    indicator.className = 'performance-indicator struggling';
    indicator.textContent = '⬇️ Struggling: Last 5 starts';
  }
}



window.addEventListener("DOMContentLoaded", () => {
  const pitchCtx = document.getElementById('pitchDistributionChart').getContext('2d');
  new Chart(pitchCtx, {
    type: 'doughnut',
    data: {
      labels: ['四縫線速球 (FA)', '指叉球 (FS)', '曲球 (CU)', '卡特球 (FC)', 'S伸卡球 (SI)'],
      datasets: [{
        data: [37, 28, 19, 8, 6],
        backgroundColor: [
          '#e63946', '#f1fa8c', '#577590', '#ffb703', '#8ac926'
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      cutout: '70%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `使用率: ${context.raw}%`;
            }
          }
        }
      }
    }
  });
});
