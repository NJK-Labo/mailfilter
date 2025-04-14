/**
 * 汎用モーダルを起動し、確認ボタンに任意処理をバインドします。
 * @param {string} modalSelector - モーダル要素のセレクタ（例: "#deleteModal"）
 * @param {string} confirmButtonSelector - 確認ボタンのセレクタ（例: "#confirmDeleteBtn"）
 * @param {Function} onConfirm - 確認ボタンがクリックされたときに実行する関数
 */
function openModalWithAction(modalSelector, confirmButtonSelector, onConfirm) {
    const modalElement = document.querySelector(modalSelector);
    const modal = new bootstrap.Modal(modalElement);
    const confirmButton = document.querySelector(confirmButtonSelector);

    // すでにイベントが設定されている可能性があるため一度リセット
    confirmButton.onclick = () => {
        onConfirm();
        modal.hide(); // 確認後モーダルを閉じる（必要に応じて）
    };
    modal.show();
}

document.querySelectorAll('[data-modal-target]').forEach((button) => {
    button.addEventListener('click', (event) => {
        const formId = event.currentTarget.getAttribute('data-form-id');
        const formElement = document.getElementById(formId);

        // まずブラウザのバリデーションを実行する
        if (!formElement.checkValidity()) {
            // バリデーションエラーがあればエラーメッセージを表示
            formElement.reportValidity();
            return; // ここで処理を中断してダイアログは表示しない
        }
        
        // バリデーションOKの場合にのみ、ダイアログ（モーダル）を表示
        const targetModal = event.currentTarget.getAttribute('data-modal-target');
        const confirmTarget = event.currentTarget.getAttribute('data-confirm-target');

        openModalWithAction(targetModal, confirmTarget, () => {
            formElement.submit();
        });
    });
});
