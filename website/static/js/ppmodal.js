const profileImage = document.getElementById('profileImage');
const imageUploadModal = document.getElementById('imageUploadModal');
const uploadInput = document.getElementById('upload');
const filenameLabel = document.getElementById('filename');
const imagePreview = document.getElementById('image-preview');
const cancelButton = document.getElementById('cancelButton');

profileImage.addEventListener('click', () => {
    imageUploadModal.classList.remove('hidden');
});

imageUploadModal.addEventListener('click', (event) => {
    if (event.target === imageUploadModal) {
        imageUploadModal.classList.add('hidden');
    }
});

let isEventListenerAdded = false;

uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file) {
        filenameLabel.textContent = file.name;

        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.innerHTML =
                `<img src="${e.target.result}" class="max-h-48 rounded-lg mx-auto" alt="Image preview" />`;
            imagePreview.classList.remove('border-dashed', 'border-2', 'border-gray-400');

            if (!isEventListenerAdded) {
                imagePreview.addEventListener('click', () => {
                    uploadInput.click();
                });

                isEventListenerAdded = true;
            }
        };
        reader.readAsDataURL(file);
    } else {
        filenameLabel.textContent = '';
        imagePreview.innerHTML =
            `<div class="bg-gray-200 h-48 rounded-lg flex items-center justify-center text-gray-500">No image preview</div>`;
        imagePreview.classList.add('border-dashed', 'border-2', 'border-gray-400');

        if (isEventListenerAdded) {
            imagePreview.removeEventListener('click', () => {
                uploadInput.click();
            });

            isEventListenerAdded = false;
        }
    }
});

uploadInput.addEventListener('click', (event) => {
    event.stopPropagation();
});

cancelButton.addEventListener('click', function() {
    imageUploadModal.classList.add('hidden');
});



const uploadButton = document.querySelector('.upload_label');

uploadButton.addEventListener('click', () => {
    const fileInput = document.getElementById('upload');
    const file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('profile_picture', file);

        fetch('/uploadprofilepic', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Handle success, like updating UI or showing a message
                console.log('Profile picture uploaded successfully');
            } else {
                // Handle error response from server
                console.error('Failed to upload profile picture');
            }
        })
        .catch(error => {
            // Handle network errors or other errors
            console.error('Error uploading profile picture:', error);
        });
    } else {
        console.error('No file selected');
    }
});
