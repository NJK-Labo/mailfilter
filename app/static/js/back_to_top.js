const backToTopButton = document.querySelector('#backToTop');

// スクロール時のイベント
window.addEventListener('scroll', () => {
    // 画面のトップからの距離が300ピクセルを超えたらボタンを表示
    if (window.scrollY > 300) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});

// ボタンをクリックした時のイベント
backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});
