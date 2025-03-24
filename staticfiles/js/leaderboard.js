document.addEventListener('DOMContentLoaded', function() {
  const categorySelect = document.getElementById('category-select');
  
  // 取得所有類別
  fetch('/api/category/')
    .then(response => response.json())
    .then(categories => {
      categories.results.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
      });
    })
    .catch(error => console.error('Error fetching categories:', error));

  // 取得排行榜資料
  function fetchLeaderboard(categoryId = '') {
    let url = '/api/post/leaderboard/';
    if (categoryId) {
      url += `?category=${categoryId}`;
    }
    fetch(url)
      .then(response => response.json())
      .then(data => {
        const leaderboardList = document.getElementById('leaderboard-list');
        leaderboardList.innerHTML = '';
        data.forEach((item, index) => {
          const row = document.createElement('tr');
          let rowClass = '';
          if (index === 0) {
            rowClass = 'table-warning'; // 金色
          } else if (index === 1) {
            rowClass = 'table-secondary'; // 銀色
          } else if (index === 2) {
            rowClass = 'table-danger'; // 銅色
          }
          row.className = rowClass;
          row.innerHTML = `
            <th scope="row">${index + 1}</th>
            <td>${item.profile.studient_id || item.profile.username}</td>
            <td>${item.title}</td>
            <td>${item.category.name}</td>
            <td>${item.likes_count || 0} 讚</td>
            <td>${item.views || 0} 觀看</td>

          `;
          leaderboardList.appendChild(row);
        });
      })
      .catch(error => console.error('Error fetching leaderboard data:', error));
  }

  // 初次載入排行榜資料
  fetchLeaderboard();

  // 當類別選擇改變時，更新排行榜資料
  categorySelect.addEventListener('change', function() {
    fetchLeaderboard(this.value);
  });
});