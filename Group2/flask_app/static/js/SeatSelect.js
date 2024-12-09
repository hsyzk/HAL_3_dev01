$(document).ready(function() {
    var selectedSeats = []; 

    // showingIdを正しい値で設定
    var showingId = document.getElementById('showing-id').value; 

    // 関数: 予約済み座席のスタイルを更新
    function updateReservedSeats() {
        $.ajax({
            url: '/views/SeatSelect',
            type: 'GET',
            data: { showing_id: showingId },
            dataType: 'json',
            success: function(response) {
                if (response.status === 'success') {
                     // response.seats を updateSeatStyles に渡す
                    updateSeatStyles(response.seats);
                } else {
                    console.error("Error from server:", response.message);
                    $('#error-message').text(response.message);
                }
            },
            error: function(error) {
                console.error("Failed to get reserved seats:", error);
                $('#error-message').text('座席情報の取得に失敗しました。しばらく時間をおいてから再度お試しください。');
            }
        });
    }

    // 関数: 座席のスタイルを更新
    function updateSeatStyles(seats) {
        $('.seat').each(function() {
            var seatId = $(this).data('seat-id');
            var seat = seats.find(seat => seat.id === seatId);

            if (seat && seat.reserved) {
                $(this).addClass('reserved')
                .css({
                    'background-color': 'darkgray',
                    'cursor': 'not-allowed'
                })
                .off('click');
            } else {
                $(this).removeClass('reserved')
                .css({
                    'background-color': '',
                    'cursor': 'pointer'
                })
                .on('click', function() {
                    var seatId = $(this).data('seat-id');
                    
                    if ($(this).hasClass('selected')) {
                        $(this).removeClass('selected');
                        selectedSeats = selectedSeats.filter(id => id !== seatId);
                    } else {
                        $(this).addClass('selected');
                        selectedSeats.push(seatId);
                    }

                    updateSelectedSeatDisplay();
                });
            }
        });
    }


    // 選択された座席の表示を更新
    function updateSelectedSeatDisplay() {
        var selectedSeatText = '選択された座席: ';
        if (selectedSeats.length > 0) {
            var selectedSeatNumbers = selectedSeats.map(function(seatId) {
                return $('.seat[data-seat-id="' + seatId + '"]').text().trim();
            });
            selectedSeatText += selectedSeatNumbers.join(', ');
        } else {
            selectedSeatText += 'なし';
        }
        $('#selected-seat').text(selectedSeatText);
    }

    // ページ読み込み時と定期的に予約状況を更新
    updateReservedSeats();
    // setInterval(updateReservedSeats, 5000); // 5秒ごとに更新
    // フォーム送信時の処理
    $('#seatForm').submit(function() {
        // フォームの隠しフィールドに選択された座席IDをセット
        $('#selected-seats').val(selectedSeats.join(','));
    });

    // 予約ボタンクリック処理
    $('#reserve-button').click(function() {
        if (selectedSeats.length === 0) {
            $('#error-message').text('座席を選択してください');
            return;
        } else {
            $('#error-message').text('');
        }

        console.log("Selected Seat IDs:", selectedSeats);

        $.ajax({
            url: '/views/reserve_seat',
            type: 'POST',
            data: { 
                'seat_ids[]': selectedSeats, 
                'showing_id': showingId 
            },
            traditional: true,
            success: function(response) {
                if(response.status === 'success') {
                    selectedSeats = [];
                    updateSelectedSeatDisplay();
                
                    window.location.href = response.redirect_url;
                } else {
                    alert(response.message);
                }
            },
            error: function(error) {
                console.error("Reservation failed:", error);
                $('#error-message').text('予約に失敗しました。しばらく時間をおいてから再度お試しください。');
            }
        });
    });
});
