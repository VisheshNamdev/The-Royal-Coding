
  document.addEventListener('DOMContentLoaded', (event) => {
      const shareBtn = document.getElementById('shareBtn');
      const shareDialogue = document.getElementById('shareDialogue');

      // Function to open or close the dialogue
      const toggleDialogue = () => {
          shareDialogue.classList.toggle('hidden');
      };

      // Toggle dialogue visibility on button click
      shareBtn.addEventListener('click', () => {
          toggleDialogue();
      });

      // Close dialogue when clicking outside of it
      document.addEventListener('click', (event) => {
          if (!shareBtn.contains(event.target) && !shareDialogue.contains(event.target)) {
              shareDialogue.classList.add('hidden');
          }
      });

      // Copy link functionality
      const copyLink = document.getElementById('copyLink');
      copyLink.addEventListener('click', (event) => {
          event.preventDefault(); // Prevent default link behavior
          const link = window.location.href;
          navigator.clipboard.writeText(link).then(() => {
              alert('Link copied to clipboard');
              shareDialogue.classList.add('hidden');
          }).catch(err => {
              alert('Failed to copy the link');
          });
      });

      // Share on Twitter
      const shareTwitter = document.getElementById('shareTwitter');
      shareTwitter.addEventListener('click', (event) => {
          event.preventDefault(); // Prevent default link behavior
          const link = window.location.href;
          window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(link)}`, '_blank');
          shareDialogue.classList.add('hidden');
      });

      // Share on Facebook
      const shareFacebook = document.getElementById('shareFacebook');
      shareFacebook.addEventListener('click', (event) => {
          event.preventDefault(); // Prevent default link behavior
          const link = window.location.href;
          window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(link)}`, '_blank');
          shareDialogue.classList.add('hidden');
      });

      // Share on LinkedIn
      const shareLinkedIn = document.getElementById('shareLinkedIn');
      shareLinkedIn.addEventListener('click', (event) => {
          event.preventDefault(); // Prevent default link behavior
          const link = window.location.href;
          window.open(`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(link)}`, '_blank');
          shareDialogue.classList.add('hidden');
      });
  });
