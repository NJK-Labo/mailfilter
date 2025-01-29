// すべての削除ボタンにイベントリスナーを追加
document.querySelectorAll('[id^="delete-button-"]').forEach((button) => {
    button.addEventListener('click', (event) => {
        const mailId = event.currentTarget.id.split('-').pop();
        openDeleteModal(mailId);
    });
});

// 削除用モーダル
const openDeleteModal = (mailId) => {
    const deleteModal = new bootstrap.Modal(document.querySelector('#deleteModal'));
    const confirmDeleteBtn = document.querySelector('#confirmDeleteBtn');

    confirmDeleteBtn.onclick = () => {
        document.querySelector(`#delete-form-${mailId}`).submit();
    };

    deleteModal.show();
};
