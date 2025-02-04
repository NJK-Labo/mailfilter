// 日付入力フィールドのプレースホルダー表示を実装するスクリプト
// 日付入力フィールドはプレースホルダーを表示できないため、
// 入力されていない時はtype=textに変えてプレースホルダーを表示する
const setupDateInput = (id, placeholderText) => {
    const dateInput = document.querySelector(`#${id}`);

    const toggleType = (isFocus) => {
        dateInput.type = isFocus ? 'date' : 'text';
        dateInput.placeholder = isFocus ? '' : placeholderText;
    };

    // 初期設定はtext（プレースホルダー表示）
    !dateInput.value && toggleType(false);

    // フォーカスされた時またはフォーカスが外れた時に設定
    dateInput.addEventListener('focus', () => toggleType(true));
    dateInput.addEventListener('blur', () => !dateInput.value && toggleType(false));
};

// 各日付フィールドに適用
setupDateInput('start_date', '検索対象期間（開始）');
setupDateInput('end_date', '検索対象期間（終了）');
