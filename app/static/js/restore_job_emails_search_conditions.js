// 求人関係メール詳細画面から一覧画面へ戻る際に、セッションストレージから検索条件を復元する
document.querySelector('#backToList').addEventListener('click', (event) => {
    const conditions = JSON.parse(sessionStorage.getItem('jobEmailsSearchParams')) || {};
    const params = new URLSearchParams(conditions).toString();

    // URLにクエリパラメータを追加
    event.target.href = `${event.target.href}?${params}`;
});
