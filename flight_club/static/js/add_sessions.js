function addRow() {
      
    // Get the beer form
    var beer_form = $("#beer-form");
    var rows = beer_form.find("tr").length;

    // Get the elements
    var new_form_row = $("#beer-form-row").clone();
    new_form_row.attr("id", "beer-form-row-" + rows);
    
    // Edit all the rows
    new_form_row.find(".beer input").attr("name","beer_" + rows)
    new_form_row.find(".brewery input").attr("name","brewery_" + rows)
    new_form_row.find(".style input").attr("name","style_" + rows)
    new_form_row.find(".beer_abv input").attr("name","beer_abv_" + rows)
    new_form_row.find(".votes input").attr("name","votes_" + rows)
    new_form_row.find(".win input").attr("name","win_" + rows)
    new_form_row.find(".username input").attr("name","username_" + rows)

    // Add the row to the form
    beer_form.append(new_form_row);
}

function removeRow()  {

  // Get the beer for
  var last_row = $("#beer-form").find("tr").length - 1;
  var row_id = "beer-form-row-" + last_row;
  $('#'+row_id).remove();

}