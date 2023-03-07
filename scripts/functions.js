function setSelectedValue(event){
    
    // element clicked
    var e = event.target;
    
    // parent custom-select div
    var p = e.parentElement.parentElement;
    
    //change text of custom-select-selected div input
    p.getElementsByClassName("custom-select-selected")[0].children[0].value = e.textContent;
}
