function addPodcast(){
    form = el("podcasts-addpodcast");
    button = el("podcasts-addpodcast-show");
    if(form.style.display != "block"){
        form.style.display = "block";
        button.className = "fas fa-minus-circle";
    }
    else{
        form.style.display = "none";
        button.className = "fas fa-plus-circle";
    }
}

function deletePodcast(p_id){
    entry = el("delete-"+p_id);
    entry.style.width = "100px";
    var form = document.createElement("form");
    form.setAttribute('method',"post");
    form.setAttribute('action',"podcasts");

    var i = document.createElement("button"); //input element, text
    i.setAttribute('type',"submit");
    i.setAttribute('name',"del_podcast");
    i.setAttribute('value', p_id);
    i.innerText = "Delete";
    form.appendChild(i);

    entry.appendChild(form);
}

function updatePodcast(p_id, name, position, url){
    form = el("podcasts-modifypodcast");
    form.style.display = "block";

    form.elements["id"].value = p_id;
    form.elements["position"].value = position;
    form.elements["name"].value = name;
    form.elements["url"].value = url;
}