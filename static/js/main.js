// Auto-hide flash messages after 3 seconds
document.querySelectorAll('.alert').forEach(function (el) {
  setTimeout(function () {
    el.style.opacity = '0';
    setTimeout(function () { el.remove(); }, 400);
  }, 3000);
});
