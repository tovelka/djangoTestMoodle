document.addEventListener('DOMContentLoaded', function() {
    const closeBtn = document.querySelector('.close');
    const photoBtns = document.querySelectorAll('.photo');
    const photoContainer = document.querySelector('.openedPhotoContainer');
    const openedImg = document.querySelector('.openedPhoto img');
    const leftBtn = document.getElementById('toLeftPhoto');
    const rightBtn = document.getElementById('toRightPhoto');
    
    let currentPhotoIndex = 0;
    let photos = []; // Массив путей фото

    // фото -> массив фото
    photoBtns.forEach((btn, index) => {
        const img = btn.querySelector('img');
        photos.push(img.src);
        
        btn.addEventListener('click', () => {
            currentPhotoIndex = index;
            openPhoto(currentPhotoIndex);
        });
    });

    function openPhoto(index) {
        openedImg.src = photos[index];
        photoContainer.classList.remove('closedPhotoContainer');
    }

    function closePhoto() {
        photoContainer.classList.add('closedPhotoContainer');
    }

    function navigatePhotos(direction) {
        currentPhotoIndex += direction;
        
        // Зацикливание
        if (currentPhotoIndex >= photos.length) currentPhotoIndex = 0;
        if (currentPhotoIndex < 0) currentPhotoIndex = photos.length - 1;
        
        openPhoto(currentPhotoIndex);
    }

    closeBtn.addEventListener('click', closePhoto);
    leftBtn.addEventListener('click', () => navigatePhotos(-1));
    rightBtn.addEventListener('click', () => navigatePhotos(1));

    // Клавиатура
    document.addEventListener('keydown', (e) => {
        if (!photoContainer.classList.contains('closedPhotoContainer')) {
            if (e.key === 'ArrowLeft') navigatePhotos(-1);
            if (e.key === 'ArrowRight') navigatePhotos(1);
            if (e.key === 'Escape') closePhoto();
        }
    });
});