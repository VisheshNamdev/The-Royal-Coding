window.addEventListener('DOMContentLoaded', event => {

// Toggle the side navigation
const sidebarToggle = document.body.querySelector('#sidebarToggle');
if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
        event.preventDefault();
        document.body.classList.toggle('sb-sidenav-toggled');
        localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
}

});



//Slideshow of photos
function scrollSlider(direction) {
  const sliders = document.querySelectorAll('.slider');
  sliders.forEach(slider => {
    const cardWidth = slider.querySelector('.card').offsetWidth;
    slider.scrollBy({
      left: direction * (cardWidth + 10), // 10 is the margin-right
      behavior: 'smooth'
    });
  });
}

function autoScroll() {
  const sliders = document.querySelectorAll('.slider');
  sliders.forEach(slider => {
    const cardWidth = slider.querySelector('.card').offsetWidth;
    if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
      slider.scrollTo({ left: 0, behavior: 'smooth' });
    } else {
      slider.scrollBy({ left: cardWidth + 10, behavior: 'smooth' });
    }
  });
  setTimeout(autoScroll, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(autoScroll, 3000);
});


      function toggleEditInfo() {
        var formElements = document.querySelectorAll('#infoForm input');
        var saveButton = document.getElementById('saveButton');
        formElements.forEach(function (element) {
            if (element.readOnly) {
                element.readOnly = false;
                saveButton.classList.remove('hidden');
            } else {
                element.readOnly = true;
                saveButton.classList.add('hidden');
            }
        });
    }

    function toggleEditExperience() {
        const experienceList = document.getElementById('experienceList');
        const editExperienceFields = document.getElementById('editExperienceFields');

        if (editExperienceFields.classList.contains('hidden')) {
            experienceList.classList.add('hidden');
            editExperienceFields.classList.remove('hidden');
        } else {
            experienceList.classList.remove('hidden');
            editExperienceFields.classList.add('hidden');
        }
    }

    function toggleEditBio() {
        var bioBlock = document.getElementById('bioblock');
        var bioForm = document.getElementById('bioForm');
        if (bioBlock.classList.contains('hidden')) {
            bioBlock.classList.remove('hidden');
            bioForm.classList.add('hidden');
        } else {
            bioBlock.classList.add('hidden');
            bioForm.classList.remove('hidden');
        }
    }

    let slideIndex = 0;
    const slides = document.getElementsByClassName("mySlides");
    
    // Function to show initial slide and start slideshow
    function startSlideShow() {
        showSlides();
        setInterval(showSlides, 5000); // Automatic slideshow every 4 seconds
    }
    
    // Function to show slides
    function showSlides() {
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";  // Hide all slides initially
        }
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1;  // Reset slideIndex if it exceeds the number of slides
        }
        slides[slideIndex - 1].style.display = "block";  // Display the current slide
    }
    
    // Function to change slides on button click
    function plusSlides(n) {
        slideIndex += n;
        if (slideIndex < 1) {
            slideIndex = slides.length;  // Loop back to the last slide if at the beginning
        } else if (slideIndex > slides.length) {
            slideIndex = 1;  // Loop back to the first slide if at the end
        }
        showSlides();  // Display the slide based on updated slideIndex
    }
    
    // Start slideshow when the page loads
    window.onload = startSlideShow;
