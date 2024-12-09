$(document).ready(function() {
  var trigger = $('.modal__trigger'),
      wrapper = $('.modal__wrapper'),
      layer = $('.modal__layer'),
      container = $('.modal__container'),
      close = $('.modal-close');

  // flatpickrで年月選択ピッカーを作成
  flatpickr("#cardExpiry", {
    locale: "ja",  // 日本語ロケール
    plugins: [new monthSelectPlugin({
      shorthand: true, // 月を短縮形式で表示（例：1月→Jan）
      dateFormat: "m/y",  // 表示フォーマット：MM/YY
      altFormat: "m/y",   // 入力フィールドに表示されるフォーマット：MM/YY
      theme: "light"      // テーマの設定
    })],
    maxDate: new Date().fp_incr(365 * 10) // 10年後まで選択可能
  });

  // モーダル表示のトリガー
  trigger.click(function() {
    if (validateInput()) {
      // 入力内容をモーダルに反映
      $('#confirmName').val($('input[placeholder="カード名義"]').val());
      $('#confirmCardnum').val($('input[placeholder="カード番号（-無し16桁）"]').val());
      $('#confirmCarddate').val($('#cardExpiry').val());
      $('#confirmCardcode').val($('input[placeholder="セキュリティコード"]').val());

      // モーダルを表示
      wrapper.fadeIn(400);
      $('html, body').css('overflow', 'hidden');  // 背景スクロールを無効化
    }
  });

  // モーダル閉じる処理
  layer.add(close).click(function() {
    wrapper.fadeOut(400);
    $('html, body').css('overflow', '');  // 背景スクロールを有効化
  });

  // バリデーション関数
  function validateInput() {
    var name = $('input[placeholder="カード名義"]').val().trim();
    var cardnum = $('input[placeholder="カード番号（-無し16桁）"]').val().trim();
    var carddate = $('#cardExpiry').val().trim();
    var cardcode = $('input[placeholder="セキュリティコード"]').val().trim();
    var isValid = true;

    // カード名義のバリデーション
    if (name === '') {
      showErrorMessage($('input[placeholder="カード名義"]').closest('.cp_iptxt').find('.error-message'), '※カード名義を入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="カード名義"]').closest('.cp_iptxt').find('.error-message'));
    }

    // カード番号のバリデーション...桁数は{16}
    if (cardnum === '') {
      showErrorMessage($('input[placeholder="カード番号（-無し16桁）"]').closest('.cp_iptxt').find('.error-message'), '※カード番号を入力してください。');
      isValid = false;
    } else if (!/^\d{16}$/.test(cardnum)) {
      showErrorMessage($('input[placeholder="カード番号（-無し16桁）"]').closest('.cp_iptxt').find('.error-message'), '※正しい形式で入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="カード番号（-無し16桁）"]').closest('.cp_iptxt').find('.error-message'));
    }

    // カード有効期限のバリデーション
    if (carddate === '') {
      showErrorMessage($('#cardExpiry').closest('.cp_iptxt').find('.error-message'), '※カード有効期限を入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('#cardExpiry').closest('.cp_iptxt').find('.error-message'));
    }

    // セキュリティコードのバリデーション3桁or4桁
    if (cardcode === '') {
      showErrorMessage($('input[placeholder="セキュリティコード"]').closest('.cp_iptxt').find('.error-message'), '※セキュリティコードを入力してください。');
      isValid = false;
    } else if (!/^\d{3,4}$/.test(cardcode)) {
      showErrorMessage($('input[placeholder="セキュリティコード"]').closest('.cp_iptxt').find('.error-message'), '※セキュリティコードは3桁または4桁で入力してください。');
      isValid = false;
    } else {
      hideErrorMessage($('input[placeholder="セキュリティコード"]').closest('.cp_iptxt').find('.error-message'));
    }

    return isValid;  // バリデーション結果を返す
  }

  // エラーメッセージを表示する関数
  function showErrorMessage(element, message) {
    element.text(message).show();
  }

  // エラーメッセージを非表示にする関数
  function hideErrorMessage(element) {
    element.text('').hide();
  }
});
