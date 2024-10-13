document.addEventListener("DOMContentLoaded", function () {
  
  const devoteButtons = document.querySelectorAll(".devote-button");
  const bookmarkButtons = document.querySelectorAll(".bookmark-button");

  const upvoteButtons = document.querySelectorAll(".upvote-button");

  upvoteButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const blogId = this.getAttribute("data-post-id");
      await toggleUpvote(blogId);
    });
  });

  devoteButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const blogId = this.getAttribute("data-post-id");
      await handleDevote(blogId);
    });
  });

  bookmarkButtons.forEach((button) => {
    button.addEventListener("click", async function () {
      const blogId = this.getAttribute("data-post-id");
      await handleBookmark(blogId);
    });
  });

  
});

async function toggleUpvote(blogId) {
  try {
      const response = await fetch(`/upvote/${blogId}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
      });

      const result = await response.json();

      if (response.ok) {
          const upvoteCountSpan = document.getElementById(`upvote-count-${blogId}`);
          upvoteCountSpan.textContent = result.No_upvote;
          // Optionally, change the button color or icon based on the like/unlike status
          const button = document.querySelector(`.upvote-button[data-post-id="${blogId}"]`);
          if (result.success === 'Blog liked') {
              button.classList.add('liked');
          } else {
              button.classList.remove('liked');
          }
      } else {
          alert(result.error);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}







async function handleDevote(blogId) {
  try {
    const response = await fetch(`/devote/${blogId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (response.ok) {
      const devoteCountSpan = document.getElementById(`devote-count-${blogId}`);
      devoteCountSpan.textContent = result.No_devote;
    } else {
      alert(result.error);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function handleBookmark(blogId) {
  try {
    const response = await fetch(`/bookmark/${blogId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (response.ok) {
      const bookmarkCountSpan = document.getElementById(
        `bookmark-count-${blogId}`
      );
      bookmarkCountSpan.textContent = result.No_bookmark;
    } else {
      alert(result.error);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
