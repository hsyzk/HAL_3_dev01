// function switchTab(tabNumber) {
//   // 選択されたタブのコンテンツを表示し、他のタブを非表示にする
//   for (let i = 1; i <= 2; i++) {
//     const tabContent = document.getElementById('tab' + i);
//     const tabButton = document.getElementById('tab-button').children[i - 1];

//     if (i === tabNumber) {
//       tabContent.classList.add('active-tab');
//       tabButton.classList.add('active-tab');
//     } else {
//       tabContent.classList.remove('active-tab');
//       tabButton.classList.remove('active-tab');
//     }
//   }
// }
function switchTab(tabNumber) {
  console.log('Switching to tab', tabNumber);

  // Get tab contents and buttons
  const tabContents = document.querySelectorAll('.tab-content');
  const tabButtons = document.querySelectorAll('.tab-button');

  if (tabContents.length === 0 || tabButtons.length === 0) {
    console.error('No tab contents or buttons found');
    return;
  }

  // Loop through and show/hide tab content
  tabContents.forEach((tabContent, index) => {
    if (index + 1 === tabNumber) {
      tabContent.classList.add('active-tab');
    } else {
      tabContent.classList.remove('active-tab');
    }
  });

  // Loop through and activate/deactivate tab buttons
  tabButtons.forEach((tabButton, index) => {
    if (index + 1 === tabNumber) {
      tabButton.classList.add('active');
    } else {
      tabButton.classList.remove('active');
    }
  });
}




$(".slider").slick({
    autoplay: true, // 自動再生
    arrows: true, // 矢印
    dots: true, // インジケーター
    prevArrow: '<img src="../../static/images/slick_prevI.png" class="prev-arrow">',
    nextArrow: '<img src="../../static/images/slick_nextI.png" class="next-arrow">',
    slidesToShow: 1,
    centerMode: true,
    centerPadding: '200px',
    focusOnSelect: true,
  });



