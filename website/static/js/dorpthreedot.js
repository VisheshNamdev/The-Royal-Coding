document.addEventListener('DOMContentLoaded', function () {
  // Code for handling report popups
  const openReportPopupBtns = document.querySelectorAll('.report');
  const reportPopup = document.getElementById('reportPopup');
  const closeReportPopupBtn = document.getElementById('closeReportPopupBtn');
  const reportForm = document.getElementById('reportForm');
  const blogIdInput = document.getElementById('blogId');

  openReportPopupBtns.forEach(btn => {
    btn.addEventListener('click', (event) => {
      const postId = event.currentTarget.getAttribute('id').replace('report-', '');
      openReportPopup(postId);
    });
  });

  function openReportPopup(blogId) {
    blogIdInput.value = blogId;
    reportPopup.classList.remove('hidden');
  }

  closeReportPopupBtn.addEventListener('click', () => {
    reportPopup.classList.add('hidden');
  });

  // Close the popup when clicking outside of the popup content
  window.addEventListener('click', (event) => {
    if (event.target === reportPopup) {
      reportPopup.classList.add('hidden');
    }
  });

  // Add event listeners to links inside the dropdown menu
  const dropdownLinks = document.querySelectorAll('.dropdownMenu a');
  dropdownLinks.forEach(link => {
    link.addEventListener('click', function () {
      dropdownMenu.classList.add('hidden'); // Hide the dropdown menu after clicking a link
    });
  });

  // Close the dropdown menu if clicked outside
  document.addEventListener('click', function (event) {
    if (!kebabMenuButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
      dropdownMenu.classList.add('hidden');
    }
  });

  reportForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(reportForm);
    try {
      const response = await fetch('/url/to/submit/report', {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        alert('Report submitted successfully!');
        reportPopup.classList.add('hidden');
        // You may want to refresh or update the UI here if needed
      } else {
        alert('Failed to submit report. Please try again later.');
      }
    } catch (error) {
      console.error('Error submitting report:', error);
      alert('An error occurred. Please try again later.');
    }
  });

  document.querySelectorAll('.kebabMenuButton').forEach(button => {
    button.addEventListener('click', (event) => {
      event.stopPropagation();
      const dropdownMenu = button.nextElementSibling;
      document.querySelectorAll('.dropdownMenu').forEach(menu => {
        if (menu !== dropdownMenu) {
          menu.style.display = 'none';
        }
      });
      dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.thumb')) {
      document.querySelectorAll('.dropdownMenu').forEach(menu => {
        menu.style.display = 'none';
      });
    }
  });

  // Close dropdown menu when the report button is clicked
  const reportButtons = document.querySelectorAll('.report-button');
  reportButtons.forEach(button => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.dropdownMenu').forEach(menu => {
        menu.style.display = 'none';
      });
    });
  });

  // Delete modal functionality
  const deleteButtons = document.querySelectorAll('.delete-button');
  const deleteModal = document.getElementById('deleteModal');
  const confirmDeleteButton = document.getElementById('confirmDeleteButton');
  const cancelButton = document.getElementById('cancelButton');
  let postIdToDelete = null;

  deleteButtons.forEach(button => {
    button.addEventListener('click', (event) => {
      const postId = button.getAttribute('data-post-id');
      postIdToDelete = postId;
      deleteModal.style.display = 'block';
    });
  });

  confirmDeleteButton.addEventListener('click', () => {
    if (postIdToDelete) {
      window.location.href = `/delete/${postIdToDelete}`;
    }
  });

  cancelButton.addEventListener('click', () => {
    deleteModal.style.display = 'none';
    postIdToDelete = null;
  });

  // Close delete modal when clicking outside of the modal content
  window.addEventListener('click', (event) => {
    if (event.target === deleteModal) {
      deleteModal.style.display = 'none';
      postIdToDelete = null;
    }
  });
});
