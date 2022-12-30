// Author: Przemyslaw Bil
// g00398317@atu.ie
// Javascript and ajax for Index.html

var active_user_id = 0;
//function to show Artist search dialog
function showMusicSearch(){
    
    if(document.getElementById("music_search").style.display == "inline"){
        document.getElementById("music_search").style.display = "none";  
        document.getElementById("search_results").style.display = "none";
        document.getElementById("toggle_musixmatch_search_button").innerHTML = "Add New favorite Albums"
        document.getElementById('search_results').innerHTML = ''
    }else{                
        document.getElementById("music_search").style.display = "inline";  
        document.getElementById("search_results").style.display = "inline";
        document.getElementById("toggle_musixmatch_search_button").innerHTML = "Close Musixmatch search"
    }
}

//function to show new profile form or search for music
function selectProfile(user_id, user_name){
    console.log(`Button Pressed: ${user_id}`);

    //active_user_id is a global variable
    active_user_id = user_id;

    if (user_id > 0){             
        document.getElementById("user_favorites").style.display = "inline";
        document.getElementById("registered_users").style.display = "none";

        const header = document.getElementById("user_favorites_h2");
        header.innerHTML= `${user_name}s favorite Albums`;

        showSelectedUserFavorites(user_id);

    }else{
        document.getElementById("registered_users").style.display = "none";
        document.getElementById("add_profile").style.display = "inline";                                        
    }
}
// function to show edit_profile div
const name_input =  document.getElementById("edit_user");
const id_input =  document.getElementById("edit_user_id");    

function editProfile(user_id, user_name){
    console.log(`Edit Button Pressed: ${user_id}, ${user_name}`);
    document.getElementById("edit_profile").style.display = "inline";
    document.getElementById("registered_users").style.display = "none";

    name_input.defaultValue = user_name;
    id_input.defaultValue = user_id;
}        

// functions and data structures for deleting profile/user
const deleteDialog = document.getElementById('delete-dialog'); 
const confirmDeleteButton = document.getElementById('confirm-delete');
const cancelDeleteButton = document.getElementById('cancel-delete');

cancelDeleteButton.addEventListener('click', function(){
    deleteDialog.close();
});                   

function deleteProfile(user_id, user_name){
    deleteDialog.show();
    //Function added this way, as adding event listner created multiple event listners and function being called many times
    confirmDeleteButton.setAttribute('onclick', `call_delete(${user_id}, "${user_name}")`);                
}

function call_delete(user_id, user_name){
    console.log(`Delete Button Pressed: ${user_id}, ${user_name}`);
    $.ajax(
        {
        "url":`api/user/${user_id}`,
        "method":"DELETE",
        "data": "",
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(response){
            console.log("User deleted successfully");                       
            runOnLoad()
        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )                
    deleteDialog.close();
}

//Function to add album to favorites
function addToFavorites(album_id){                
    $.ajax(
        {
        "url":`/api/addfav`,
        "method":"PUT",
        "data": JSON.stringify({user_id:active_user_id, album_id:album_id}),
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(response){
            console.log(`Add album nr${album_id} to user id ${active_user_id}`)    
            //refresh favirets displayed for this user
            showSelectedUserFavorites(active_user_id)                   
            //runOnLoad()
        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )                
}

//Function to display selected user Favorites
function showSelectedUserFavorites(user_id){
    var FavoritesDisplayArea = document.getElementById("fav_album_list");

    FavoritesDisplayArea.innerHTML = "Fetching data, please wait";
    $.ajax(
        {
        "url":`/api/userfavs/${user_id}`,
        "method":"GET",
        "data": "",
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(result){

            FavoritesDisplayArea.innerHTML = "";

            //Check if selected user has aby albums saved
            if(result.length>0){                
                //table to hold the buttons
                const table = document.createElement('table');

                table.className = "fav_table";

                const header = document.createElement('tr');
                const hcell1 = document.createElement('th');
                const hcell2 = document.createElement('th');
                const hcell3 = document.createElement('th');
                const hcell4 = document.createElement('th');
                const hcell5 = document.createElement('th');

                hcell1.innerHTML = "Artist";
                hcell2.innerHTML = "Album name";
                hcell3.innerHTML = "Label";
                hcell4.innerHTML = "Release Date";

                header.appendChild(hcell1);
                header.appendChild(hcell2);
                header.appendChild(hcell3);
                header.appendChild(hcell4);
                header.appendChild(hcell5);

                table.appendChild(header);
                

                for(const fav of result){
                    const row= document.createElement('tr');
                    const cell1= document.createElement('td');
                    const cell2= document.createElement('td');
                    const cell3= document.createElement('td');
                    const cell4= document.createElement('td');
                    const cell5= document.createElement('td');
                    
                    cell1.innerHTML = fav.artist_name;
                    cell2.innerHTML = fav.album_name;
                    cell3.innerHTML = fav.album_label;
                    cell4.innerHTML = fav.album_release_date;

                    var del_button = document.createElement('button');
                    del_button.innerHTML = "Remove";
                    del_button.setAttribute('class', 'del_button');
                    del_button.setAttribute('id', `del_button_uid${fav.id}`);
                    del_button.setAttribute('onclick', `removeFavorite(${fav.id})`);

                    cell5.appendChild(del_button);

                    row.appendChild(cell1);
                    row.appendChild(cell2);
                    row.appendChild(cell3);
                    row.appendChild(cell4);
                    row.appendChild(cell5);

                    table.appendChild(row);

                    //console.log(`User Favorites: ${fav.album_label}`)                       
                }

                FavoritesDisplayArea.appendChild(table);
        }
        },
        "error":function(xhr, status, error){
            FavoritesDisplayArea.innerHTML = "";
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )                   
}

//Function to remove Favorite form users list
function removeFavorite(fav_id){
    $.ajax(
        {
        "url":`/api/fav`,
        "method":"DELETE",
        "data": JSON.stringify({id:fav_id}),
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(response){
            console.log(`Album nr${fav_id} removed from user id ${active_user_id}`)    
            //refresh favorites displayed for this user
            showSelectedUserFavorites(active_user_id)                   
        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )           
}            

// Function onLoad() to be run at the start of the page
function runOnLoad(){
    document.getElementById("music_search").style.display = "none";  
    document.getElementById("toggle_musixmatch_search_button").innerHTML = "Add New favorite Albums";
    document.getElementById('search_results').innerHTML = '';     
    document.getElementById("registered_users").style.display = "inline";
    document.getElementById("add_profile").style.display = "none";
    document.getElementById("search_results").style.display = "none";
    document.getElementById("edit_profile").style.display = "none";
    document.getElementById("user_favorites").style.display = "none";
    document.getElementById("music_search").style.display = "none"
    $.ajax(
        {
            "url":`/api/users`,
            "method":"GET",
            "data":"",
            "dataType": "JSON",
            "contentType": "application/json; charset=utf-8",
            "success":function(result){
                var UsersDisplayArea = document.getElementById("registered_users");
                                                            
                UsersDisplayArea.innerHTML='<h2>Select your profile</h2> <br> ';
                
                //table to hold the buttons
                const table = document.createElement('table');

                table.className = "user_tbl";

                for (const user of result){
                    // Define table with user selection, edit and delete buttons
                    const row = document.createElement('tr');

                    const cell1 = document.createElement('td');
                    const cell2 = document.createElement('td');
                    const cell3 = document.createElement('td');

                    var user_button = document.createElement('button');
                    user_button.innerHTML = user.name;
                    user_button.setAttribute('class', 'user_button');
                    user_button.setAttribute('id', `button_uid${user.user_id}`);
                    user_button.setAttribute('onclick', `selectProfile(${user.user_id}, "${user.name}")`);

                    cell1.appendChild(user_button);
                    cell1.className= "user_tbl_user"

                    var edit_button = document.createElement('button');
                    edit_button.innerHTML = "Edit";
                    edit_button.setAttribute('class', 'edit_button');
                    edit_button.setAttribute('id', `edit_button_uid${user.user_id}`);
                    edit_button.setAttribute('onclick', `editProfile(${user.user_id}, "${user.name}")`);  
                    
                    cell2.appendChild(edit_button);
                    cell2.className= "user_tbl_edit"

                    var del_button = document.createElement('button');
                    del_button.innerHTML = "Delete";
                    del_button.setAttribute('class', 'del_button');
                    del_button.setAttribute('id', `del_button_uid${user.user_id}`);
                    del_button.setAttribute('onclick', `deleteProfile(${user.user_id}, "${user.name}")`);
                    
                    cell3.appendChild(del_button);   
                    cell3.className= "user_tbl_del"                             

                    row.appendChild(cell1);
                    row.appendChild(cell2);
                    row.appendChild(cell3);

                    table.appendChild(row);                                
                    
                }

                const row = document.createElement('tr');
                const cell1 = document.createElement('td');

                var user_button = document.createElement('button');
                user_button.innerHTML = "Add new Profile";
                user_button.setAttribute('class', 'user_button');
                user_button.setAttribute('id', `button_uid0`);
                user_button.setAttribute('onclick', `selectProfile(0, "")`);
                    
                // Add new user div to User Display Area
                cell1.appendChild(user_button);
                row.appendChild(cell1); 
                table.appendChild(row);                
                
                // Add table to the user display area
                UsersDisplayArea.appendChild(table);                            

            },
            "error":function(xhr, status, error){
                console.log("error: "+status+" msg: "+ error);
            }
        }
    )
}
//function to handle editing user/profile name
const formEdit = document.getElementById('edit_user_form');
formEdit.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(formEdit);
    const newName = formData.get('edit_user');
    const user_id = formData.get('edit_user_id');

    console.log(`newName=${newName}, user_id=${user_id}`);

    $.ajax(
        {
        "url":`api/user/${user_id}`,
        "method":"POST",
        "data": JSON.stringify({name: newName}),
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(response){
            console.log("User edited successfully");                       
            runOnLoad();
        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )
}
)//end of formEdit.addEventListener            


// function to handle adding new user/profile
const formAdd = document.getElementById('add_user_form');
formAdd.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(formAdd);
    const addUser = formData.get('add_user');

    const newUser = {name: addUser}
    console.log(newUser);
    $.ajax(
        {
        "url":`api/user`,
        "method":"PUT",
        "data": JSON.stringify(newUser),
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success": function(response){
            console.log("New user added successfully");                       
            runOnLoad()
        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )
}
)//end of formAdd.addEventListener


// Clear the table with artist albums
function close_artist(artist_id, artist_name){
    var artistcell = document.getElementById(`artist${artist_id}`);
    var expanderCell = document.getElementById(`expand${artist_id}`);

    artistcell.setAttribute('class', 'artist');
    artistcell.innerHTML = artist_name;    
    artistcell.setAttribute('onclick', `open_artist(${artist_id}, '${artist_name}')`);

    expanderCell.innerHTML = "[+]";
    expanderCell.setAttribute('onclick', `open_artist(${artist_id}, '${artist_name}')`);

}

// Populate the table with artist albums
function open_artist(artist_id, artist_name){

    var artistcell = document.getElementById(`artist${artist_id}`);
    var expanderCell = document.getElementById(`expand${artist_id}`);

    $.ajax(
        {
            "url":`api/mm/show.artist.albums/${artist_id}`,
            "method":"GET",
            "data":"",
            "dataType": "JSON",
            "contentType": "application/json; charset=utf-8",
            "success":function(result2){

                
                //reset parent artist div to prevent albums being added multiple times
                artistcell.innerHTML=artist_name;
                artistcell.setAttribute('class', 'artist_opened');
                artistcell.setAttribute('onclick', `close_artist(${artist_id}, '${artist_name}')`);

                expanderCell.innerHTML = "[-]";
                expanderCell.setAttribute('onclick', `close_artist(${artist_id}, '${artist_name}')`);                
                
                const table = document.createElement('table');

                table.className = "artist_albums_table";

                for (const album of result2){
                    const row = document.createElement('tr');
                    const cell1 = document.createElement('td');
                    const cell2 = document.createElement('td');
                    const cell3 = document.createElement('td');
                    const cell4 = document.createElement('td');                                                

                    //var album_div = document.createElement('div');
                    row.setAttribute('class', 'album');
                    row.setAttribute('id', album.album_id);

                    cell1.innerHTML = `${album.album_name}`;
                    cell2.innerHTML = `${album.album_label}`;
                    cell3.innerHTML = `${album.album_release_date}`;

                    var add_button = document.createElement('button');
                    add_button.innerHTML = "Add to Favorires";
                    add_button.setAttribute('class', 'add_button');
                    add_button.setAttribute('id', `add_button_uid${album.album_id}`);
                    add_button.setAttribute('onclick', `addToFavorites(${album.album_id})`);
                    
                    cell4.appendChild(add_button);

                    row.appendChild(cell4);
                    row.appendChild(cell1);      
                    row.appendChild(cell2);
                    row.appendChild(cell3);                                                                                            

                    table.appendChild(row)                                                
                }
                artistcell.appendChild(table);

            },
            "error":function(xhr, status, error){
                console.log("error: "+status+" msg: "+ error);
            }
        }
    )    
}

// Search for artists
const form = document.getElementById('search_artist');
form.addEventListener('submit', function(event){
    event.preventDefault();
    const formData = new FormData(form);
    const query = formData.get('query');
    $.ajax(
    {
        "url":`api/mm/find.artist/${query}`,
        "method":"GET",
        "data":"",
        "dataType": "JSON",
        "contentType": "application/json; charset=utf-8",
        "success":function(result){   
            //console.log(result)                         
            const searchResults = document.getElementById('search_results');
            searchResults.innerHTML = 'Artists matching your query: </br>';

            const table = document.createElement('table');
            table.className = "artist_table";

            // loop over results to list each artist found
            for (const artist of result) {
                const row = document.createElement('tr');
                const cell1 = document.createElement('td');
                const cell2 = document.createElement('td');

                //var div = document.createElement('div');
                cell1.setAttribute('class', 'artist');
                cell1.setAttribute('id', `artist${artist.artist_id}`);
                cell1.innerHTML = artist.artist_name;
                cell1.setAttribute('onclick', `open_artist(${artist.artist_id}, '${artist.artist_name}')`);

                cell2.setAttribute('class', 'artist');
                cell2.setAttribute('id', `expand${artist.artist_id}`);
                cell2.innerHTML = "[+]";                
                cell2.setAttribute('onclick', `open_artist(${artist.artist_id}, '${artist.artist_name}')`);  
                
                row.appendChild(cell1)
                row.appendChild(cell2)
                table.appendChild(row)                      
            }//end of for artist loop
            searchResults.appendChild(table);      

        },
        "error":function(xhr, status, error){
            console.log("error: "+status+" msg: "+ error);
        }
    }
    )
});        

window.addEventListener("load", runOnLoad);  