// Находим кнопку "Подписаться"
const btn = document.querySelector(".btn-primary");

// Переменная-флаг: подписан или нет
let isSubscribed = false;

// Обработчик клика
btn.addEventListener("click", function() {
  if (isSubscribed) {
    // Если уже подписан — отписываемся
    btn.textContent = "Подписаться";
    btn.style.background = "#667eea";
    btn.style.color = "#fff";
  } else {
    // Если не подписан — подписываемся
    btn.textContent = "Вы подписаны \u2714";
    btn.style.background = "#10b981";
    btn.style.color = "#fff";
  }
  // Переключаем флаг
  isSubscribed = !isSubscribed;
});
