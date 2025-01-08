// 検索クリアボタンの処理
// ボタンを<input type="reset">にしても既に表示されている入力値はクリアできないので
// javascriptで入力域を直接リセット
document.querySelector('#clear').addEventListener('click', () => {
    const form = document.querySelector('#searchForm');
    
    // input要素をクリア（type="submit"以外）
    const inputs = form.querySelectorAll('input');
    inputs.forEach((input) => { 
        input.type !== 'submit' ? input.value = '' : null;
    });

    // select要素の選択をクリア
    const selects = form.querySelectorAll('select');
    selects.forEach((select) => {
        select.selectedIndex = 0;
    });
});
