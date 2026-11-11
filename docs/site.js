const versionSelect = document.querySelector('#minecraft-version');
const loaderSelect = document.querySelector('#mod-loader');
const release = '1.0.0-beta.3';
const english = document.documentElement.lang === 'en';
const targets = {
  '1.21.1': { java: '21+', fabricApi: '0.116.17+1.21.1', lithostitched: '1.8.0', neoForge: '21.1.256' },
  '1.21.11': { java: '21+', fabricApi: '0.141.6+1.21.11', lithostitched: '1.7.2', neoForge: '21.11.48' },
  '26.2': { java: '25+', fabricApi: '0.161.0+26.2', lithostitched: '1.8.0', neoForge: '26.2.0.88' },
  '26.3': { java: '25+', fabricApi: '0.165.2+26.3', lithostitched: '2.0.6', neoForge: '26.3.0.101' }
};

function updateDownload() {
  const game = versionSelect.value;
  const loader = loaderSelect.value;
  const target = targets[game];
  const file = `relics-${release}+mc${game}${loader === 'neoforge' ? '-neoforge' : ''}.jar`;
  document.querySelector('#jar-download').href = `https://github.com/Auda29/Titan-Relics/releases/download/v${release}/${encodeURIComponent(file)}`;
  const loaderName = loader === 'fabric' ? 'Fabric' : 'NeoForge';
  document.querySelector('#jar-download').setAttribute('aria-label', english
    ? `Download Titan Relics ${release} for Minecraft ${game} with ${loaderName}`
    : `Titan Relics ${release} für Minecraft ${game} mit ${loaderName} herunterladen`);
  document.querySelector('#file-name').textContent = file;
  document.querySelector('#java-requirement').textContent = `Java ${target.java} · ${loader === 'fabric' ? 'Fabric Loader 0.19.5+' : `NeoForge ${target.neoForge}`}`;
  const dependencies = document.querySelector('#dependencies');
  dependencies.replaceChildren();
  const addDependency = (name, url) => {
    const link = document.createElement('a');
    link.href = url;
    link.textContent = name;
    dependencies.append(link);
  };
  if (loader === 'fabric') {
    addDependency(`Fabric API ${target.fabricApi}`, 'https://modrinth.com/mod/fabric-api');
    dependencies.append(english ? ' and ' : ' und ');
  }
  addDependency(`Lithostitched ${target.lithostitched}`, 'https://modrinth.com/mod/lithostitched');
  dependencies.append(english
    ? `, each for ${game} / ${loaderName}.`
    : `, jeweils für ${game} / ${loaderName}.`);
}
versionSelect.addEventListener('change', updateDownload);
loaderSelect.addEventListener('change', updateDownload);
updateDownload();

// Each relic owns a separate slideshow; captions come from the shared manifest.
const lightbox = document.querySelector('#lightbox');
const groups = new Map();
let activeGroup = null;
let returnFocus = null;

function stopSlideshow(group) {
  clearInterval(group.timer);
  group.timer = null;
  group.play.setAttribute('aria-pressed', 'false');
  group.play.setAttribute('aria-label', english ? 'Play slideshow' : 'Slideshow abspielen');
  group.play.querySelector('[data-play-icon]').textContent = '▶';
  group.play.querySelector('[data-play-label]').textContent = english ? 'Play' : 'Abspielen';
  group.caption.setAttribute('aria-live', 'polite');
}

function showSlide(group, index) {
  group.index = (index + group.links.length) % group.links.length;
  group.links.forEach((link, position) => { link.hidden = position !== group.index; });
  const current = group.links[group.index];
  group.count.textContent = `${group.index + 1} / ${group.links.length}`;
  group.caption.textContent = `${current.dataset.title} · ${current.dataset.capture}`;
}

function startSlideshow(group) {
  group.play.setAttribute('aria-pressed', 'true');
  group.play.setAttribute('aria-label', english ? 'Pause slideshow' : 'Slideshow pausieren');
  group.play.querySelector('[data-play-icon]').textContent = 'Ⅱ';
  group.play.querySelector('[data-play-label]').textContent = 'Pause';
  group.caption.setAttribute('aria-live', 'off');
  group.timer = setInterval(() => {
    const bounds = group.root.getBoundingClientRect();
    if (!document.hidden && !lightbox.open && bounds.bottom > 0 && bounds.top < window.innerHeight) {
      showSlide(group, group.index + 1);
    }
  }, 5000);
}

function showLightboxImage(group, index) {
  showSlide(group, index);
  const link = group.links[group.index];
  const image = link.querySelector('img');
  const expandedImage = document.querySelector('#lightbox-image');
  expandedImage.src = link.href;
  expandedImage.alt = image.alt;
  document.querySelector('#lightbox-title').textContent = link.dataset.title;
  document.querySelector('#lightbox-count').textContent = `${group.index + 1} / ${group.links.length} · ${link.dataset.capture}`;
}

function openLightbox(event, group, index, link) {
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof lightbox.showModal !== 'function') return;
  event.preventDefault();
  if (performance.now() < group.suppressClickUntil) return;
  groups.forEach(stopSlideshow);
  returnFocus = link;
  activeGroup = group;
  showLightboxImage(group, index);
  lightbox.showModal();
  document.body.classList.add('modal-open');
}

document.querySelectorAll('[data-slideshow]').forEach(root => {
  const group = {
    root,
    links: [...root.querySelectorAll('[data-gallery]')],
    index: 0,
    timer: null,
    caption: root.querySelector('.slide-caption'),
    count: root.querySelector('.slide-count'),
    play: root.querySelector('[data-slide-play]'),
    suppressClickUntil: 0
  };
  groups.set(root.dataset.slideshow, group);
  const move = delta => {
    stopSlideshow(group);
    showSlide(group, group.index + delta);
  };
  root.querySelector('[data-slide-prev]').addEventListener('click', () => move(-1));
  root.querySelector('[data-slide-next]').addEventListener('click', () => move(1));
  group.play.addEventListener('click', () => group.timer ? stopSlideshow(group) : startSlideshow(group));
  root.addEventListener('focusin', () => stopSlideshow(group));
  root.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      move(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  group.links.forEach((link, index) => {
    link.addEventListener('click', event => openLightbox(event, group, index, link));
  });
  const viewport = root.querySelector('.slideshow-viewport');
  let start = null;
  viewport.addEventListener('pointerdown', event => {
    if (event.isPrimary && (event.pointerType === 'touch' || event.pointerType === 'pen')) {
      start = { x: event.clientX, y: event.clientY, id: event.pointerId };
    }
  });
  viewport.addEventListener('pointerup', event => {
    if (!start || start.id !== event.pointerId) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    start = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.2) {
      group.suppressClickUntil = performance.now() + 500;
      move(dx < 0 ? 1 : -1);
    }
  });
  viewport.addEventListener('pointercancel', () => { start = null; });
  showSlide(group, 0);
  root.querySelector('.slideshow-controls').hidden = false;
});

// The expedition photograph opens the Colossus carousel at the matching view.
document.querySelectorAll('[data-gallery]').forEach(link => {
  if (link.closest('[data-slideshow]')) return;
  for (const group of groups.values()) {
    const index = group.links.findIndex(slide => slide.href === link.href);
    if (index !== -1) {
      link.addEventListener('click', event => openLightbox(event, group, index, link));
      break;
    }
  }
});

document.querySelector('#lightbox-close').addEventListener('click', () => lightbox.close());
document.querySelector('#lightbox-prev').addEventListener('click', () => {
  if (activeGroup) showLightboxImage(activeGroup, activeGroup.index - 1);
});
document.querySelector('#lightbox-next').addEventListener('click', () => {
  if (activeGroup) showLightboxImage(activeGroup, activeGroup.index + 1);
});
lightbox.addEventListener('keydown', event => {
  if (activeGroup && (event.key === 'ArrowLeft' || event.key === 'ArrowRight')) {
    event.preventDefault();
    showLightboxImage(activeGroup, activeGroup.index + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
lightbox.addEventListener('click', event => {
  if (event.target !== lightbox) return;
  const bounds = lightbox.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) lightbox.close();
});
lightbox.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  // The selected slide may have changed while the modal was open.
  if (returnFocus?.hidden) returnFocus = activeGroup?.links[activeGroup.index];
  returnFocus?.focus({ preventScroll: true });
});
