/* KINGDAO 移动端导航 + 通用交互 */
document.addEventListener('DOMContentLoaded', function () {
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('nav.links');

  if (burger && nav) {
    burger.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
    // 点菜单外关闭
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target) && e.target !== burger) {
        nav.classList.remove('open');
      }
    });
  }

  // 移动端：产品/项目卡片如果被子元素遮挡，强制冒泡到 <a>
  document.querySelectorAll('a.proj, a.prod, a.sol').forEach(function (card) {
    card.style.cursor = 'pointer';
    card.addEventListener('click', function (e) {
      if (e.target.tagName !== 'A' && e.currentTarget.tagName === 'A') {
        window.location.href = e.currentTarget.getAttribute('href');
      }
    });
  });
});
