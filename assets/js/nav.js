/* KINGDAO 导航：移动端菜单 + 产品/业绩下拉子菜单（一处注入，全站生效） */
document.addEventListener('DOMContentLoaded', function () {
  var burger = document.querySelector('.burger');
  var nav = document.querySelector('nav.links');

  /* ---------- 1. 构建下拉菜单 ---------- */
  if (nav && !nav.dataset.menuBuilt) {
    var links = Array.prototype.slice.call(nav.querySelectorAll(':scope > a'));
    var pLink = links.filter(function (a) { return /products\.html/.test(a.getAttribute('href') || ''); })[0];
    var jLink = links.filter(function (a) { return /projects\.html/.test(a.getAttribute('href') || ''); })[0];
    // 相对前缀：products 页里导航写成 ../products.html
    var base = pLink ? (pLink.getAttribute('href') || '').replace('products.html', '') : '';
    var pUrl = base ? base : '';

    var PRODUCTS = [
      ['Screens & grilles', [
        ['products/mechanical-bar-screen.html', 'Mechanical bar screen'],
        ['products/fine-bar-screen.html', 'Fine bar screen'],
        ['products/coarse-manual-screen.html', 'Coarse & manual bar screen'],
        ['products/rotary-drum-screen.html', 'Rotary drum screen'],
        ['products/screw-screen.html', 'Screw screen'],
        ['products/crushing-grille.html', 'PG tubular crushing grille'],
        ['products/channel-crushing-grille.html', 'PZG / PZGD drum crushing grille']
      ]],
      ['Sludge & dewatering', [
        ['products/screw-press.html', 'Multi-disc screw press'],
        ['products/sludge-scraper.html', 'Sludge scraper']
      ]],
      ['Mixing & aeration', [
        ['products/mixers.html', 'Submersible mixers'],
        ['products/propellers.html', 'Propellers & thrusters'],
        ['products/aerators.html', 'Aerators & diffusers']
      ]],
      ['Dosing & process media', [
        ['products/dosing.html', 'Automatic dosing devices'],
        ['products/fillers.html', 'Fillers (elastic / rope)'],
        ['products/mbr.html', 'Membrane systems (MBR)']
      ]],
      ['Pumps & stations', [
        ['products/submersible-pumps.html', 'Submersible pumps'],
        ['products/frp-pumping-station.html', 'FRP pumping station']
      ]]
    ];

    var PROJECTS = [
      ['municipal', 'Municipal wastewater'],
      ['tannery', 'Tannery & leather'],
      ['textile', 'Textile, dyeing & printing'],
      ['pcb', 'PCB & electronics'],
      ['slaughterhouse', 'Slaughterhouse'],
      ['livestock', 'Livestock farming'],
      ['down-feather', 'Down & feather'],
      ['reuse', 'Water reuse'],
      ['water-supply', 'Water supply treatment'],
      ['river', 'River & waterbody rehabilitation']
    ];

    function buildMega() {
      var h = '<div class="dropdown mega">';
      PRODUCTS.forEach(function (grp) {
        h += '<div class="mh">' + grp[0] + '</div>';
        grp[1].forEach(function (it) {
          h += '<a href="' + pUrl + it[0] + '">' + it[1] + '</a>';
        });
      });
      h += '<a class="all" href="' + pUrl + 'products.html">All equipment →</a></div>';
      return h;
    }
    function buildTypes() {
      var h = '<div class="dropdown types">';
      PROJECTS.forEach(function (it) {
        h += '<a href="' + pUrl + 'projects.html#' + it[0] + '">' + it[1] + '</a>';
      });
      h += '<a class="all" href="' + pUrl + 'projects.html">All projects →</a></div>';
      return h;
    }

    function wrap(link, html) {
      if (!link) return;
      var item = document.createElement('div');
      item.className = 'nav-item';
      link.parentNode.insertBefore(item, link);
      item.appendChild(link);
      item.insertAdjacentHTML('beforeend', html);
      // 移动端：点第一下展开子菜单，第二下才跳转
      link.addEventListener('click', function (e) {
        if (window.innerWidth <= 900 && !item.classList.contains('open')) {
          e.preventDefault();
          item.classList.add('open');
        }
      });
    }
    wrap(pLink, buildMega());
    wrap(jLink, buildTypes());
    nav.dataset.menuBuilt = '1';
  }

  /* ---------- 2. 移动端汉堡菜单 ---------- */
  if (burger && nav) {
    burger.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) {
      if (nav.classList.contains('open') && !nav.contains(e.target) && e.target !== burger) {
        nav.classList.remove('open');
      }
    });
  }


  /* ---------- 4. 产品图框型自适应：竖长图用 3:4 竖框，避免两侧留白 ---------- */
  function fitFrames() {
    document.querySelectorAll('.img-grid figure').forEach(function (fig) {
      var img = fig.querySelector('img');
      if (!img || !img.naturalWidth) return;
      var ar = img.naturalWidth / img.naturalHeight;
      // 框型跟随图片比例（限幅 0.55~2.2，避免极端长条卡片）
      var ar2 = Math.min(2.0, Math.max(0.85, ar));
      fig.style.aspectRatio = ar2.toFixed(3);
      fig.classList.toggle('img-tall', ar2 < 0.95);
    });
  }
  document.querySelectorAll('.img-grid img').forEach(function (img) {
    if (img.complete) return;
    img.addEventListener('load', fitFrames, { once: true });
  });
  fitFrames();
  window.addEventListener('load', fitFrames);

  /* ---------- 3. 卡片点击兜底 ---------- */
  document.querySelectorAll('a.proj, a.prod, a.sol').forEach(function (card) {
    card.style.cursor = 'pointer';
    card.addEventListener('click', function (e) {
      if (e.target.tagName !== 'A' && e.currentTarget.tagName === 'A') {
        window.location.href = e.currentTarget.getAttribute('href');
      }
    });
  });
});
