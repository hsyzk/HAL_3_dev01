const dateTabs = document.querySelectorAll('#scheduleday .day'); 
const showtimeSections = document.querySelectorAll('.showtime-section');

dateTabs.forEach(tab => {
  tab.addEventListener('click', (event) => {
    event.preventDefault(); // <a> タグのデフォルト動作をキャンセル

    const clickedDate = event.target.textContent.trim(); // 空白を除去して日付を取得

    // 全てのタブを非アクティブに、選択された日付のタブをアクティブに
    dateTabs.forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');

    // 全ての上映時間セクションを非表示に、選択された日付のセクションを表示
    showtimeSections.forEach(section => {
      // 日付の書式を合わせて比較
      section.style.display = section.dataset.date.trim() === clickedDate ? 'block' : 'none'; 
    });
  });
});

// 初期表示は最初のタブの内容を表示
const firstTab = dateTabs[0];
if (firstTab) {
  firstTab.classList.add('active');
  const firstDate = firstTab.dataset.date;
  document.querySelector(`.showtime-section[data-date="${firstDate}"]`).style.display = 'block';
}