document.addEventListener('DOMContentLoaded', () => {
  const readMoreButtons = document.querySelectorAll('.read-more-button');

  readMoreButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const postID = button.dataset.postid;
      window.location.href = `/post/${postID}`;
    });
  });
});