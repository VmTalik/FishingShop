const commentRatings = document.querySelectorAll('.comment_rating');

for (let commentRating of commentRatings){
    let commentRatingStars = commentRating.querySelectorAll('span');
    for (let i = 0; i < commentRating.dataset.comment_rating; i++) {
        commentRatingStars[i].style.color = 'orange';
    }
}