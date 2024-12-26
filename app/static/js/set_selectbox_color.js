// セレクトボックスの選択肢の文字色を変更する
// CSSで指定が難しかったため、JavaScriptで実装
const selectElement = document.getElementById('type');

// 文字色の設定
const updateColor = () => {
    // 選択された値の文字色を設定（値が空白の選択肢はグレー表示）
    // #212529はBootstrapの文字色
    selectElement.style.color = selectElement.value === '' ? 'gray' : '#212529';

    // リストの各選択肢の文字色を設定（先頭の選択肢のみグレー表示）
    Array.from(selectElement.options).forEach((option, index) => {
        option.style.color = index === 0 ? 'gray' : '#212529';
    });
}

// 初期状態のチェック
updateColor();

// 選択変更時に色を更新
selectElement.addEventListener('change', updateColor);
