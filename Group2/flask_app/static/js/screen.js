// 変数に要素を入れる
var trigger = $('.modal__trigger'),
    wrapper = $('.modal__wrapper'),
    layer = $('.modal__layer'),
    container = $('.modal__container'),
    close = $('.modal__close');

// 『モーダルを開くボタン』をクリックしたら、『モーダル本体』を表示
$(trigger).click(function() {
  var index = trigger.index(this); // triggerのインデックスを取得
  $(wrapper).eq(index).fadeIn(400);

  // スクロール位置を戻す
  $(wrapper).eq(index).find(container).scrollTop(0);

  // サイトのスクロールを禁止にする
  $('html, body').css('overflow', 'hidden');
});

// 『背景』と『モーダルを閉じるボタン』をクリックしたら、『モーダル本体』を非表示
$(layer).add(close).click(function() {
  $(this).closest(wrapper).fadeOut(400);

  // サイトのスクロール禁止を解除する
  $('html, body').removeAttr('style');
});
