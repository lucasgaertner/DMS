function SearchAndFilter() {
    var inputfield, filter, table, tr, td, x;
    inputfield = document.getElementById("UserInput");
    filter = inputfield.value;
    table = document.getElementById("elementList");
    tr = table.getElementsByClassName("element");
    vendorname = table.getElementsByClassName("content");
    for (x = 0; x < tr.length; x++) {
      td = vendorname[x].innerHTML;
      if (td) {
        if (td.indexOf(filter) > -1) {
          tr[x].style.display = "";
        }
        else {
          tr[x].style.display = "none";
        }
      }
    }
  }

function nsort(){
  table = document.getElementById("elementList");
  tr = table.getElementsByClassName("element");
  vendorname = table.getElementsByClassName("timestamp");
  var numericallyOrderedDivs = tr.sort(function (a, b) {
      return $(a).find(".timestamp").text() > $(b).find(".timestamp").text();
  });
  table.html(numericallyOrderedDivs);

}


  function sort(){
    var inputfield, filter, table, tr, td, x;
    inputfield = document.getElementById("UserInput");
    filter = inputfield.value;
    table = document.getElementById("elementList");
    tr = table.getElementsByClassName("element");
    var arr = Array.prototype.slice.call( tr )
    vendorname = table.getElementsByClassName("timestamp");
    var tarr = Array.prototype.slice.call( vendorname )
    console.log("tarr>" +tarr);
    var earr = [];
    for (i = 0; i < tarr.length; i++) {
      earr.push(tarr[i].innerHTML);
    }
    console.log("earr"+earr);

    var date_sort_asc = function (date1, date2) {
      if (date1 > date2) return 1;
      if (date1 < date2) return -1;
      return 0;
    };
    
    var date_sort_desc = function (date1, date2) {
      if (date1 > date2) return -1;
      if (date1 < date2) return 1;
      return 0;
    };
    console.log(earr.sort(date_sort_desc));

  }