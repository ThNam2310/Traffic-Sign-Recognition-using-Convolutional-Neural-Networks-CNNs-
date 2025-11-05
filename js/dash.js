import trafficSigns from './data.js';

let currentPage = 1;
const itemsPerPage = 12;
let filteredSigns = [];

// Initialize dashboard
function initDashboard() {
  if (!Array.isArray(trafficSigns) || trafficSigns.length === 0) {
    console.error('Dữ liệu trafficSigns không hợp lệ hoặc rỗng.');
    document.getElementById('signsContainer').innerHTML = '<p class="text-muted">Không có dữ liệu.</p>';
    return;
  }

  // Normalize some fields to avoid case/spacing issues (optional)
  trafficSigns.forEach(s => {
    if (s.type) s._typeNorm = s.type.toString().trim().toLowerCase();
    else s._typeNorm = '';
    if (s.code) s._code = s.code.toString().trim();
    else s._code = '';
    if (!s.image) s.image = `image/${s.code}.png`;
  });

  filteredSigns = [...trafficSigns];
  updateStatistics();
  displaySigns();
  setupEventListeners();
}

// Update statistics
function updateStatistics() {
  const total = trafficSigns.length;
  const prohibition = trafficSigns.filter(s => s._typeNorm.includes('cấm')).length;
  const warning = trafficSigns.filter(s => s._typeNorm.includes('nguy')).length;
  const mandatory = trafficSigns.filter(s => s._typeNorm.includes('hiệu')).length;
  const guide = trafficSigns.filter(s => s._typeNorm.includes('chỉ dẫn') || s._typeNorm.includes('chỉ-dẫn')).length;

  document.getElementById('totalSigns').textContent = total;
  document.getElementById('prohibitionSigns').textContent = prohibition;
  document.getElementById('warningSigns').textContent = warning;
  document.getElementById('mandatorySigns').textContent = mandatory;
  document.getElementById('guideSigns').textContent = guide;
}

// Display signs with pagination
function displaySigns() {
  const container = document.getElementById('signsContainer');
  const startIndex = (currentPage - 1) * itemsPerPage;
  const signsToDisplay = filteredSigns.slice(startIndex, startIndex + itemsPerPage);

  if (!container) return;

  if (signsToDisplay.length === 0) {
    container.innerHTML = `
      <div class="col-12">
        <div class="empty-state text-center py-5">
          <i class="fas fa-search fa-2x"></i>
          <h4 class="mt-3" style="color: #333;">Không tìm thấy biển báo nào</h4>
          <p style="color: #333333ba;">Thử thay đổi từ khóa tìm kiếm hoặc bộ lọc</p>
        </div>
      </div>`;
    updatePagination();
    return;
  }

  container.innerHTML = signsToDisplay.map(sign => `
    <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
      <a href="detail.html?code=${encodeURIComponent(sign._code)}" class="text-decoration-none d-block h-100">
        <div class="sign-card h-100 d-flex flex-column justify-content-between">
          <div>
            <div class="card-img-wrap mb-3 bg-light p-3 rounded">
              <img src="${sign.image}" alt="${sign.name}" class="sign-image img-fluid" 
                   onerror="this.src='https://via.placeholder.com/300x200?text=${encodeURIComponent(sign._code)}'">
            </div>
            <div class="sign-code fw-bold text-primary">${sign._code}</div>
            <div class="sign-name text-dark">${sign.name}</div>
          </div>
          <div class="mt-3">
            <span class="sign-type ${getTypeClass(sign.type)}">${sign.type}</span>
          </div>
        </div>
      </a>
    </div>`).join('');

  updatePagination();
}

// Get type class for styling
function getTypeClass(type) {
  const t = (type || '').toString().toLowerCase();
  if (t.includes('cấm')) return 'cam';
  if (t.includes('nguy')) return 'nguy-hiem';
  if (t.includes('hiệu')) return 'hieu-lenh';
  if (t.includes('chỉ dẫn') || t.includes('chỉ-dẫn')) return 'chi-dan';
  return '';
}

// Update pagination (unchanged)
function updatePagination() {
  const totalPages = Math.max(1, Math.ceil(filteredSigns.length / itemsPerPage));
  const pagination = document.getElementById('pagination');
  if (!pagination) return;

  let paginationHTML = '';
  paginationHTML += `
    <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" data-page="${currentPage - 1}">
        <i class="fas fa-chevron-left"></i>
      </a>
    </li>`;

  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
      paginationHTML += `
        <li class="page-item ${i === currentPage ? 'active' : ''}">
          <a class="page-link" href="#" data-page="${i}">${i}</a>
        </li>`;
    } else if (i === currentPage - 2 || i === currentPage + 2) {
      paginationHTML += `
        <li class="page-item disabled"><span class="page-link">...</span></li>`;
    }
  }

  paginationHTML += `
    <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" data-page="${currentPage + 1}">
        <i class="fas fa-chevron-right"></i>
      </a>
    </li>`;

  pagination.innerHTML = paginationHTML;

  pagination.querySelectorAll('a.page-link').forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const page = parseInt(this.dataset.page);
      if (page > 0 && page <= totalPages) {
        currentPage = page;
        displaySigns();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });
}

// Setup event listeners
function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      filterSigns();
    });
  }

  const filterTypeEl = document.getElementById('filterType');


  if (filterTypeEl) {
    filterTypeEl.addEventListener('change', function () {
      filterSigns();
    });
  }
}

// Filter signs based on search and type
function filterSigns() {
  const searchTermEl = document.getElementById('searchInput');
  const filterTypeEl = document.getElementById('filterType');
  const searchTerm = searchTermEl ? (searchTermEl.value || '').toLowerCase() : '';
  const filterType = filterTypeEl ? (filterTypeEl.value || 'all') : 'all';

  filteredSigns = trafficSigns.filter(sign => {
    const matchesSearch = (sign._code || '').toLowerCase().includes(searchTerm) ||
      (sign.name || '').toLowerCase().includes(searchTerm);
    const matchesType = filterType === 'all' || (sign._typeNorm || '').includes(filterType.toLowerCase());
    return matchesSearch && matchesType;
  });

  currentPage = 1;
  displaySigns();
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', initDashboard);
