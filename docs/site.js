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

const lightbox = document.querySelector('#lightbox');
const galleryLinks = [...document.querySelectorAll('[data-gallery]')];
let activeIndex = 0;
let returnFocus = null;

function showImage(index) {
  activeIndex = (index + galleryLinks.length) % galleryLinks.length;
  const link = galleryLinks[activeIndex];
  const image = link.querySelector('img');
  document.querySelector('#lightbox-image').src = link.href;
  document.querySelector('#lightbox-image').alt = image.alt;
  document.querySelector('#lightbox-title').textContent = link.dataset.title;
  document.querySelector('#lightbox-count').textContent = `${activeIndex + 1} / ${galleryLinks.length} · ${english ? 'Beta 3 with shaders' : 'Beta 3 mit Shadern'}`;
}

galleryLinks.forEach((link, index) => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || typeof lightbox.showModal !== 'function') return;
    event.preventDefault();
    returnFocus = link;
    showImage(index);
    lightbox.showModal();
    document.body.classList.add('modal-open');
  });
});
document.querySelector('#lightbox-close').addEventListener('click', () => lightbox.close());
document.querySelector('#lightbox-prev').addEventListener('click', () => showImage(activeIndex - 1));
document.querySelector('#lightbox-next').addEventListener('click', () => showImage(activeIndex + 1));
lightbox.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    showImage(activeIndex + (event.key === 'ArrowLeft' ? -1 : 1));
  }
});
lightbox.addEventListener('click', event => {
  if (event.target !== lightbox) return;
  const rect = lightbox.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) lightbox.close();
});
lightbox.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  returnFocus?.focus({ preventScroll: true });
});
