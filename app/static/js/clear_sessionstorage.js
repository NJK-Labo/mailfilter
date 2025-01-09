// 不要なセッションストレージのクリア
// 検索画面での条件の復元などに使うセッションストレージを、対象の画面でのみ使用するため
const currentPath = window.location.pathname;
const contactEmailsPagePattern = /^\/contact-emails\/\d+$/; // 「問い合わせメール詳細」画面のパスパターン

if (!contactEmailsPagePattern.test(currentPath)) {
    // 現在のパスが「問い合わせメール詳細」画面ではない場合、問い合わせメール用のセッションストレージを削除
    sessionStorage.removeItem('contactEmailsSearchParams');
}
