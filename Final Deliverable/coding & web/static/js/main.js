var formData = new FormData(); // Currently empty
var values = {};
var prios = {};
var except = [];
var food_context = 0;
var daily_intake = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 2100.0, 8: 15.0, 9: 4200.0, 10: 420.0, 11: 750.0, 12: 0, 13: 12.0, 14: 0.9, 15: 2.1, 16: 55.0, 17: 3.0, 18: 140.0, 19: 35.0, 20: 750.0, 21: 120.0, 22: 1.2, 23: 1.5, 24: 17.0, 25: 5.0, 26: 1.4, 27: 28.0, 28: 350.0, 29: 0, 30: 0, 31: 0, 32: 550.0, 33: 2.4, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 14.0, 42: 15.0, 43: 0, 44: 0, 45: 0, 46: 100.0, 47: 0, 48: 2.0, 49: 10.0};



$('#fill-daily').click(function(){
  for (const [key, value] of Object.entries(daily_intake)) {
    if (value != 0) {
      addParam(key-1, value);
    }
  };

});

$("#loader").hide();


$('#adv').prop('checked', false);

$('#adv').click(function() {
    $("#opts").toggle(this.checked);
});

function addParam(id, val=""){
  if (val === 0) {
    return;
  }
  if (val !== "") {
    val = Math.round(val);
  }
  var element = $(`#input-${id}`);
  if (element.length == 0)
  {
    formData.append(id, 0);
    var $tmp = $("#input-default").clone(true);
    $tmp.attr("style", "display:block;");
    $tmp.attr("id", `input-${id}`);
    $tmp.attr("__item", id);
    $tmp.children("button").first().click(function(){
      deleteParam(id);
    });
    $tmp.children("h2").first().text($(`#option-${id}`).text());
    $tmp.children("input").first().val(val);
    $tmp.children("input").eq(1).val(1);
    $tmp.insertBefore($('#drop'));
    $("#myDropdown").hide();
  }
}

function deleteParam(id){
  var obj = $(`#input-${Number(id)}`);
  obj.remove();
  formData.delete(id);
}

function setValue(id, value){
  values[id] = value;
}

function sendParams(){
  var children = $('#inputs').children();
  var error = false;
  if ($('#inputs').children().length < 3){
    $("#notification").text("Add atleast one element.");
    $("#notification").show();
    return false;
  }
  children.each(function(i) {
    if ($(this).attr("__item") != null){
      if ($(this).children("input").first().val() == ""){
        $("#notification").text("Please fill in all of the values.");
        $("#notification").show();
        error = true;
        return false;
      }
      setValue($(this).attr("__item"), parseInt($(this).children("input").first().val())+1);
      prios[$(this).attr("__item")] =  parseInt($(this).children("input").eq(1).val());
    }
  });

  if (error){
    return false;
  }
  $("#myDropdown").hide();

  formData.set("values", JSON.stringify(values));
  formData.set("except", JSON.stringify(except));
  formData.set("prios", JSON.stringify(prios));

  var request = new XMLHttpRequest();
  request.open("POST", "/data");
  request.send(formData);
  $("#loader").show();
  $("#xd").show();
  request.onreadystatechange = function() {
  if (request.readyState == XMLHttpRequest.DONE) {
      var resp = request.responseText;
      window.location = '/result?id='+resp;
  }

}

}

function ToggleFoodDropdown(ctx) {
  $("#food-dropdown").toggle();
  food_context = Number(ctx);
}

function deleteFood(id, ctx){
  food_context = ctx;

  var obj = $(`#${getPrefix()}-food-${Number(id)}`);

  switch (food_context) {
    case 0:
      var index = except.indexOf(id);
      if (index !== -1) {
        except.splice(index, 1);
      }
      break;
  }

  obj.remove();
}

function getPrefix() {
  var prefix = "";
  switch (food_context) {
    case 0:
      prefix = "ex";
      break;

    case 1:
      prefix = "in";
      break;
  }
  return prefix;
}


function addFood(id) {
  var prefix = getPrefix();
  var optid = `${prefix}-food-${id}`;

  var ctx = food_context;
  if ($("#" + optid).length == 0) {
    var $tmp = $("#food-default").clone(true);
    $tmp.attr("style", "display:block;");
    $tmp.attr("__item", id);
    $tmp.children("button").first().click(function(){
      deleteFood(id, ctx);
    });
    $tmp.children("h2").first().text($(`#food-${id}`).text());
    $tmp.attr("id", optid);
    $(`#${prefix}-foods`).prepend($tmp);
  }

  switch (food_context) {
    case 0:
      except.push(id);
      break;
  }

  $("#food-dropdown").hide();


  }
/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function ToggleDropdown() {
  $("#myDropdown").toggle();
  filterFunction();
}

function filterFunction() {
  var children = $('#inputs').children();
  var added = [];
  children.each(function(i) {
    const id = $(this).attr("__item");
    if ($(this).attr("__item") != null) {
        added.push($(`#option-${id}`).text());
    }
  });
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1 && added.indexOf(txtValue) == -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }

}
