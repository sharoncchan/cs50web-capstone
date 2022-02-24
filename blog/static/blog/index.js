document.addEventListener("DOMContentLoaded", function(){

    // User bookmark a post(in index page or category or user profile)
    const bookmark_button = document.querySelectorAll(".bookmark");
    bookmark_button.forEach(bookmark_button => {
        bookmark_button.addEventListener("click", () => bookmark_post(bookmark_button));
    })

    // User like a post(in the individual post)
    const like_image = document.querySelectorAll(".like");
    like_image.forEach(like_image => {
        like_image.addEventListener("click", () => like_post(like_image));
    })

    // User edit own post(in the individual post)
    const edit_button = document.querySelectorAll(".edit");
    edit_button.forEach(edit_button => {
        edit_button.addEventListener("click", () => edit_post(edit_button));
    })

    // User reply to comments (in the individual post)
    const reply_button = document.querySelectorAll(".reply-button");
    reply_button.forEach(reply_button =>{
        reply_button.addEventListener("click", () => reply_comment(reply_button));
    })

})


function bookmark_post(bookmark_button){
   
    // Get the post id
    const post_id = bookmark_button.dataset.bookmarkid;
  
    // Get the csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Pass a Post request to the bookmark route
    fetch(`/bookmark/${post_id}`,{
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: "same-origin",
        // data passed into web server must be in string
        body: JSON.stringify({
            post_id : post_id
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)
        if (result.bookmark === "True"){

            // Change the color of the bookmark button to a darker grey
            document.querySelector(`#bookmark-${post_id}`).title = "You have bookmarked this post";
            document.querySelector(`#bookmark-${post_id}`).classList.remove('btn-outline-secondary');
            document.querySelector(`#bookmark-${post_id}`).classList.add('btn-secondary');
        }
        else {
            // Revert back to the original color
            document.querySelector(`#bookmark-${post_id}`).title = "You have removed this post from your bookmarks";
            document.querySelector(`#bookmark-${post_id}`).classList.remove('btn-secondary');
            document.querySelector(`#bookmark-${post_id}`).classList.add('btn-outline-secondary');
        }
        
    })
}


function like_post(like_image){

    // Get the post id
    const post_id = like_image.dataset.likeid;

    // Get the csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
   
    // Pass a Post request to the like route
    fetch(`/like/${post_id}`,{
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: "same-origin",
        // data passed into web server must be in string
        body: JSON.stringify({
            post_id : post_id
        })
    })
    .then(response => response.json())
    .then(result => {
    
        if (result.like ==="True"){
            // Turn the thumbs up image blue
            document.querySelector(`#like-${post_id}`).style.color = "#1E90FF";
            document.querySelector(`#like-${post_id}`).title = "You have liked this post";

            // Update the like count displayed
            document.querySelector(`#likecount-${post_id}`).innerHTML = result.num_likes;
        }
        else {
            // Turn the like thumbs up image back to grey 
            document.querySelector(`#like-${post_id}`).style.color = "grey";
            document.querySelector(`#like-${post_id}`).title = "You have unliked this post";
            
            //  Update the like count displayed
            document.querySelector(`#likecount-${post_id}`).innerHTML = result.num_likes ;
        }
       
    })
}

function edit_post(edit_button){
    
    // Get the post id
    const post_id = edit_button.dataset.editid;
    
    // Hide the original post 
    document.querySelector(`#original-content-${post_id}`).style.display= "none";

    // Display the text area with the original post
    document.querySelector(`#edited-content-${post_id}`).style.display = "block";
    
    // Hide the edit button
    document.querySelector(`#edit-${post_id}`).style.display = "none";
    
    // Display the save button
    document.querySelector(`#save-${post_id}`).style.display = "block";
    
    // Get the csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
  
    // When user save the edited post
    const save_button = document.querySelector(`#save-${post_id}`)
    save_button.addEventListener("click",() =>{
        // get the value of the edited post
        const edited_content = document.querySelector(`#edited-content-${post_id}`).value;
       
        // Pass a Post request to the like route
        fetch(`/edit/${post_id}`,{
        method: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: "same-origin",
        // data passed into web server must be in string
        body: JSON.stringify({
            post_id : post_id,
            edited_content : edited_content

        })
    })
        .then(response => response.json())
        .then(result => {
        
             // Hide the edited post 
            document.querySelector(`#edited-content-${post_id}`).style.display = "none";
            
            // Show the edit button
            document.querySelector(`#edit-${post_id}`).style.display = "block";
            
            // Hide the save button
            document.querySelector(`#save-${post_id}`).style.display = "none";

            // Show the new content
            document.querySelector(`#original-content-${post_id}`).style.display= "block";

            // Use ShowdownJS to convert the edited markdown content to HTML
            var converter = new showdown.Converter();
            const edited_content_html = converter.makeHtml(edited_content);
        
            // Display the edited content
            document.querySelector(`#original-content-${post_id}`).innerHTML= edited_content_html;
        })
    })
}


function formExit(node_id){

    // Enable the reply button
    document.querySelector(`#reply-button-${node_id}`).disabled=false;

    // Remove the reply form 
    document.getElementById("newForm").remove();
}


function reply_comment(reply_button){

    // Get the node id
    const node_id = reply_button.dataset.replyid;
 
    // Get the div of the comment the user the replying to
    const comment_div = document.querySelector(`#div-${node_id}`);

    // Disable the reply button after the reply button is clicked
    document.querySelector(`#reply-button-${node_id}`).disabled=true;

    // Get the csrf token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');


    comment_div.insertAdjacentHTML('afterend',
    '<form id="newForm" class="form-insert py-2 ms-4" method="post"> \
            <div class="d-flex justify-content-between"><h4>Reply:</h4><div><button type="button" class="btn btn-outline-secondary mb-2"  onclick=formExit("' + node_id + '")>Close</button></div></div> \
              <select name="parent" class="d-none" id="id_parent"> \
              <option value="' + node_id + '" selected="' + node_id + '"></option> \</select> \
              <textarea name="content" placeholder="Join the discussion" cols="40" rows="4" class="form-control" required id="id_content"></textarea> \
              <input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"> \
              <button type="submit" class="btn btn-success btn-sm mt-2">Submit</button> \
            </form>');
}



 





