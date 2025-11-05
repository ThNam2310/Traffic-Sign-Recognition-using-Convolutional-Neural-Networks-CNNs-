
// Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewArea = document.getElementById('previewArea');
const previewImage = document.getElementById('previewImage');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultArea = document.getElementById('resultArea');
const resetBtn = document.getElementById('resetBtn');

// Kéo thả file handler
uploadArea.addEventListener('dragover', function (e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', function (e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', function (e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleImageUpload(files[0]);
    }
});

// File input handler
imageInput.addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

// Handle image upload
function handleImageUpload(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Vui lòng chọn file ảnh!');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('Kích thước ảnh không được vượt quá 10MB!');
        return;
    }

    // Read and display image
    const reader = new FileReader();
    reader.onload = function (e) {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewArea.style.display = 'block';

        // Call API CNN
        recognizeSign(file);
    };
    reader.readAsDataURL(file);
}

// Call Flask API to recognize sign
function recognizeSign(file) {
    loadingSpinner.style.display = 'block';
    resultArea.style.display = 'none';

    const formData = new FormData();
    formData.append('image', file);  // phải trùng với tên input trên Flask

    fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json().catch(() => {
            throw new Error('Không thể parse JSON');
        }))
        .then(data => {
            if (!data.success) {
                alert(data.error);
            } else {
                const pred = data.prediction;
                displayResult({
                    code: pred.label,
                    name: pred.ten_bien,
                    type: pred.loai_bien,
                    detail: pred.tom_tat
                }, pred.confidence);
            }
        })
        .catch(err => {
            console.error("API error:", err);
            alert('Lỗi khi kết nối API. Vui lòng thử lại.');
        });
}

// Display recognition result
function displayResult(sign, confidence) {
    loadingSpinner.style.display = 'none';
    resultArea.style.display = 'block';

    document.getElementById('resultCode').textContent = sign.code;
    document.getElementById('resultName').textContent = sign.name;
    document.getElementById('resultDescription').textContent = sign.detail;

    const typeSpan = document.getElementById('resultType');
    typeSpan.textContent = sign.type;
    typeSpan.className = 'badge';

    // Set badge color based on type
    if (sign.type.includes('cấm')) {
        typeSpan.classList.add('bg-danger', 'text-light');
    } else if (sign.type.includes('nguy hiểm')) {
        typeSpan.classList.add('bg-warning', 'text-dark');
    } else if (sign.type.includes('hiệu lệnh')) {
        typeSpan.classList.add('bg-info', 'text-light');
    } else if (sign.type.includes('chỉ dẫn')) {
        typeSpan.classList.add('bg-success', 'text-light');
    }

    // Update confidence bar
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceText = document.getElementById('confidenceText');

    confidenceBar.style.width = confidence + '%';
    confidenceText.textContent = confidence + '%';

    // Change color based on confidence
    if (confidence >= 90) {
        confidenceBar.className = 'progress-bar bg-success';
        confidenceText.style.color = 'white';
    } else if (confidence >= 75) {
        confidenceBar.className = 'progress-bar bg-info';
        confidenceText.style.color = 'white';
    } else {
        confidenceBar.className = 'progress-bar bg-warning';
        confidenceText.style.color = 'black';
    }
}

// Tải ảnh khác (giữ nguyên folder)
resetBtn.addEventListener('click', function () {
    previewArea.style.display = 'none';
    uploadArea.style.display = 'block';
    previewImage.src = '';

    imageInput.value = '';

    imageInput.click();
});

// Gắn sự kiện click cho nút Chi tiết
document.querySelector('.btn-detail').addEventListener('click', () => {
    const code = document.getElementById('resultCode').textContent.trim();
    if (code) {
        window.location.href = `detail.html?code=${encodeURIComponent(code)}`;
    } else {
        alert('Không tìm thấy mã biển báo để hiển thị chi tiết!');
    }
});

