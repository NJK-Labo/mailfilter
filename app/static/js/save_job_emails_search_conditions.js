// 問い合わせメール一覧画面から詳細画面へ遷移する際に、セッションストレージに検索条件を保存する
const detailsLinks = document.querySelectorAll('a[href*="/job-emails/"]');
const pattern = /^\/job-emails\/\d+$/; // 詳細画面に遷移するパターン

detailsLinks.forEach(link => {
    const href = new URL(link.href).pathname; // リンクのパス部分を取得

    if (pattern.test(href)) { // パターンに一致する場合のみ処理を実行
        link.addEventListener('click', (event) => {
            // URLパラメータをオブジェクトにしてからJSON形式に変換してセッションストレージに保存
            const urlParams = new URLSearchParams(window.location.search);
            let paramsObject = {};

            urlParams.forEach((value, key) => {
                paramsObject[key] = value;
            });
            
            sessionStorage.setItem('jobEmailsSearchParams', JSON.stringify(paramsObject));
        });
    }
});
