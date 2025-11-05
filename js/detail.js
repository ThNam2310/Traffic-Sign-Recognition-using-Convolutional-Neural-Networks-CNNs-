import trafficSigns from "./data.js";

function getQueryParam(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
}

function renderDetail(sign) {
    const notFound = document.getElementById("notFound");
    const content = document.getElementById("detailContent");

    if (!sign) {
        notFound.style.display = "block";
        content.style.display = "none";
        return;
    }

    notFound.style.display = "none";
    content.style.display = "block";

    // Hình ảnh
    const img = document.getElementById("detailImage");
    img.src = sign.image || `image/${sign.code}.png`;
    img.onerror = () => {
        img.src = `https://via.placeholder.com/600x400?text=${encodeURIComponent(sign.code)}`;
    };

    // Thông tin cơ bản
    document.getElementById("detailCode").textContent = sign.code;
    document.getElementById("detailName").textContent = sign.name;
    document.getElementById("detailType").textContent = sign.type;
    document.getElementById("detailFull").textContent = sign.detail;

    // Nội dung chi tiết (cho phép xuống dòng)
    const detailText = document.getElementById("detailFull");
    detailText.innerHTML = sign.detail.replace(/\n/g, "<br>");
}

document.addEventListener("DOMContentLoaded", () => {
    const code = getQueryParam("code");
    if (!code) {
        renderDetail(null);
        return;
    }

    const sign = trafficSigns.find(s => s.code === code || s.code === decodeURIComponent(code));
    renderDetail(sign);
});
